#!/usr/bin/env python3
"""Create deterministic RIME trit glyph artifacts using only Python's standard library."""

from __future__ import annotations

import hashlib
import os
import shutil
import struct
import subprocess
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "cloud-glyph-results"
STATES = ("-", "0", "+")
FLASHLIGHTS = ("RED", "BLUE", "GREEN")
VALUES = {"-": 0, "0": 127, "+": 255}
MIRROR_PATH = {"-": 1, "0": 2, "+": 3}
FONT = {
    " ": (0, 0, 0, 0, 0, 0, 0), "+": (0, 4, 4, 31, 4, 4, 0), "-": (0, 0, 0, 31, 0, 0, 0), "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14), "2": (14, 17, 1, 2, 4, 8, 31), "3": (30, 1, 1, 14, 1, 1, 30), "7": (31, 1, 2, 4, 8, 8, 8),
    "A": (14, 17, 17, 31, 17, 17, 17), "B": (30, 17, 17, 30, 17, 17, 30), "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30), "E": (31, 16, 16, 30, 16, 16, 31), "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 14), "H": (17, 17, 17, 31, 17, 17, 17), "I": (31, 4, 4, 4, 4, 4, 31),
    "L": (16, 16, 16, 16, 16, 16, 31), "M": (17, 27, 21, 17, 17, 17, 17), "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14), "P": (30, 17, 17, 30, 16, 16, 16), "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30), "T": (31, 4, 4, 4, 4, 4, 4), "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4), "X": (17, 17, 10, 4, 10, 17, 17), "Y": (17, 17, 10, 4, 4, 4, 4),
}


def gpu_backend() -> str:
    """Return a usable compute backend only when its device/runtime is present."""
    if shutil.which("nvidia-smi") and Path("/dev/nvidiactl").exists():
        return "CUDA"
    if Path("/dev/kfd").exists():
        return "OpenCL-or-ROCm"
    if list(Path("/dev/dri").glob("renderD*")):
        return "Vulkan-or-OpenCL"
    return "UNAVAILABLE"


def run_gpu_coordinate_kernel(backend: str, tuples: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    """Only dispatch a GPU kernel when a verified backend is available.

    This environment has no accelerator runtime; a backend-equipped deployment must
    replace this explicit adapter with its backend's real coordinate kernel.
    """
    if backend == "UNAVAILABLE":
        return tuples
    raise RuntimeError("a detected accelerator requires a configured RIME kernel adapter")


class Canvas:
    def __init__(self, width: int, height: int, color: tuple[int, int, int]):
        self.width, self.height = width, height
        self.pixels = bytearray(color * (width * height))

    def rect(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]):
        for yy in range(max(0, y), min(self.height, y + height)):
            start = (yy * self.width + max(0, x)) * 3
            self.pixels[start:start + max(0, min(self.width, x + width) - max(0, x)) * 3] = bytes(color) * max(0, min(self.width, x + width) - max(0, x))

    def circle(self, cx: int, cy: int, radius: int, color: tuple[int, int, int]):
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if 0 <= x < self.width and 0 <= y < self.height and (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                    i = (y * self.width + x) * 3
                    self.pixels[i:i + 3] = bytes(color)

    def text(self, x: int, y: int, value: str, color=(245, 245, 245), scale=2):
        for char in value:
            glyph = FONT.get(char, FONT[" "])
            for row, bits in enumerate(glyph):
                for col in range(5):
                    if bits & (1 << (4 - col)):
                        self.rect(x + col * scale, y + row * scale, scale, scale, color)
            x += 6 * scale

    def png(self, path: Path):
        raw = b"".join(b"\0" + self.pixels[y * self.width * 3:(y + 1) * self.width * 3] for y in range(self.height))
        def chunk(name: bytes, value: bytes) -> bytes:
            return struct.pack(">I", len(value)) + name + value + struct.pack(">I", zlib.crc32(name + value) & 0xffffffff)
        path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def label(t: tuple[str, str, str]) -> str:
    return "R%s B%s G%s" % t


def mirror_label(t: tuple[str, str, str]) -> str:
    return "M%d M%d M%d" % tuple(MIRROR_PATH[state] for state in t)


def projection_rgb(t: tuple[str, str, str]) -> tuple[int, int, int]:
    red, blue, green = t
    return VALUES[red], VALUES[green], VALUES[blue]


def glyph_sheet(tuples: list[tuple[str, str, str]]):
    image = Canvas(960, 720, (13, 18, 31))
    image.text(24, 18, "RIME 27 MIRROR SIGNATURES", (255, 220, 155), 3)
    image.text(24, 50, "2-COLOR 2D SOURCE PROBED BY R B G FLASHLIGHTS", (180, 220, 255), 2)
    for index, item in enumerate(tuples):
        column, row = index % 3, index // 3
        x, y = 24 + column * 312, 82 + row * 70
        rgb = projection_rgb(item)
        image.rect(x, y, 288, 58, (35, 43, 61))
        image.rect(x + 8, y + 8, 42, 42, rgb)
        image.text(x + 62, y + 12, label(item), (255, 255, 255), 2)
        image.text(x + 62, y + 32, mirror_label(item), (170, 190, 215), 1)
    image.png(OUT / "rime-27-glyph-sheet.png")


def sphere_slices(tuples: list[tuple[str, str, str]]):
    image = Canvas(1200, 760, (10, 15, 26))
    image.text(28, 20, "RIME 27 MIRROR VIEWS", (255, 220, 155), 3)
    image.text(28, 52, "2D 2-COLOR SOURCE + R B G LIGHTS + MIRRORS 1 2 3", (180, 220, 255), 2)
    for slice_index, red in enumerate(STATES):
        cx = 205 + slice_index * 395
        image.circle(cx, 250, 150, (24, 35, 57))
        image.circle(cx, 250, 145, (17, 25, 43))
        image.text(cx - 72, 82, "RED LIGHT M%d" % MIRROR_PATH[red], (255, 120, 120), 2)
        group = [item for item in tuples if item[0] == red]
        for point, item in enumerate(group):
            px, py = cx - 84 + (point % 3) * 84, 174 + (point // 3) * 52
            image.circle(px, py, 16, projection_rgb(item))
            image.text(px - 34, py + 22, label(item), (240, 240, 240), 1)
    for index, item in enumerate(tuples):
        x, y = 25 + (index % 9) * 130, 465 + (index // 9) * 78
        image.rect(x, y, 118, 65, tuple(max(28, value // 3) for value in projection_rgb(item)))
        image.text(x + 8, y + 12, label(item), (255, 255, 255), 1)
        image.text(x + 8, y + 35, mirror_label(item), (220, 225, 235), 1)
    image.png(OUT / "rime-27-sphere-slices.png")


def main():
    tuples = [(red, blue, green) for red in STATES for blue in STATES for green in STATES]
    backend = gpu_backend()
    prepared = run_gpu_coordinate_kernel(backend, tuples)
    if len(prepared) != 27 or len(set(prepared)) != 27:
        raise RuntimeError("RIME requires exactly 27 distinct RGB-flashlight/mirror signatures")
    OUT.mkdir(exist_ok=True)
    glyph_sheet(prepared)
    sphere_slices(prepared)
    glyph_path = OUT / "rime-27-glyph-sheet.png"
    sphere_path = OUT / "rime-27-sphere-slices.png"
    glyph_digest = hashlib.sha256(glyph_path.read_bytes()).hexdigest()
    sphere_digest = hashlib.sha256(sphere_path.read_bytes()).hexdigest()
    gpu_execution = 1 if backend != "UNAVAILABLE" else 0
    receipt = "\n".join((
        "RIME-GPU-RECEIPT|schema=RIME-CLOUD-MIRROR-V2|source_dimensions=2|starting_colors=2|source_color_names=operator_inputs|view_count=27",
        "PROBE|flashlights=red,blue,green|mirror_paths=1,2,3|states=-,0,+|trit_map=1:-,2:0,3:+",
        "GPU-PROBE|cuda_device=%d|kfd_device=%d|render_device=%d|compute_backend=%s|gpu_execution=%d" % (Path("/dev/nvidiactl").exists(), Path("/dev/kfd").exists(), bool(list(Path("/dev/dri").glob("renderD*"))), backend, gpu_execution),
        "COORDINATES|" + ";".join(label(item).replace(" ", "") for item in prepared),
        "ARTIFACTS|glyph_sheet=rime-27-glyph-sheet.png|glyph_sha256=%s|sphere_slices=rime-27-sphere-slices.png|sphere_sha256=%s|deterministic=1" % (glyph_digest, sphere_digest),
        "INTERPRETATION|anti_and_anti_anti_verses=OPERATOR_DESIGN|physical_mapping=UNVERIFIED",
        "VERDICT|status=PASS|gpu_execution=%d" % gpu_execution,
        "",
    ))
    receipt_path = OUT / "gpu-runtime-receipt.hbp"
    receipt_path.write_text(receipt, encoding="ascii", newline="\n")
    digest = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
    (OUT / "gpu-runtime-receipt.hbp.sha256").write_text("%s  gpu-runtime-receipt.hbp\n" % digest, encoding="ascii", newline="\n")


if __name__ == "__main__":
    main()
