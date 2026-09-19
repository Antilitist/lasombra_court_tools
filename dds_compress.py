"""Compress large mod DDS files to BC1/DXT1 for CK3 (Paradox Clausewitz engine)."""
import os
import shutil
import subprocess
import sys


def texconv_path():
    found = shutil.which("texconv")
    if found:
        return found
    raise FileNotFoundError(
        "texconv not found on PATH. Install with: winget install Microsoft.DirectXTex.Texconv"
    )


def compress_dds_dxt1(dds_path):
    """Re-encode a DDS (or overwrite in place) as opaque BC1/DXT1."""
    dds_path = os.path.normpath(dds_path)
    out_dir = os.path.dirname(dds_path)
    subprocess.run(
        [texconv_path(), "-f", "DXT1", "-m", "1", "-y", "-o", out_dir, dds_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def finalize_activity_icon_dds(dds_path):
    """CK3 activity map/HUD icons need a full RGBA mipmap chain (80x80)."""
    dds_path = os.path.normpath(dds_path)
    out_dir = os.path.dirname(dds_path)
    subprocess.run(
        [texconv_path(), "-f", "B8G8R8A8_UNORM", "-m", "0", "-y", "-o", out_dir, dds_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def finalize_activity_title_icon_dds(dds_path):
    """CK3 running-activity title bar uses ActivityType.GetHeaderIcon (164x164)."""
    finalize_activity_icon_dds(dds_path)


def finalize_activity_header_dds(dds_path):
    """CK3 activity planner header art needs RGBA + full mipmaps (not single-mip DXT1)."""
    finalize_activity_icon_dds(dds_path)


def finalize_event_type_icon_dds(dds_path):
    """CK3 event-type icons need a full RGBA mipmap chain (148x148)."""
    finalize_activity_icon_dds(dds_path)


def compress_large_gfx_dds(gfx_root, min_bytes=400_000):
    converted = 0
    for root, _, files in os.walk(gfx_root):
        for name in files:
            if not name.lower().endswith(".dds"):
                continue
            path = os.path.join(root, name)
            if os.path.getsize(path) < min_bytes:
                continue
            with open(path, "rb") as handle:
                header = handle.read(128)
            if len(header) >= 88 and header[84:88] in (b"DXT1", b"DXT5"):
                continue
            compress_dds_dxt1(path)
            converted += 1
            print(f"compressed {path}")
    return converted


if __name__ == "__main__":
    mod = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "lasombra_court"))
    gfx = os.path.join(mod, "gfx")
    count = compress_large_gfx_dds(gfx)
    print(f"done — {count} file(s) compressed")
    sys.exit(0)