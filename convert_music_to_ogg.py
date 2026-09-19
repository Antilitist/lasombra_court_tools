"""Convert source MP3s into OGG tracks for the Court of Shadows mod."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:
    import imageio_ffmpeg
except ImportError:
    print("Install imageio-ffmpeg first: python -m pip install imageio-ffmpeg")
    sys.exit(1)

MOD_ROOT = (Path(__file__).resolve().parents[1] / "lasombra_court")
DEFAULT_SOURCE = Path(r"X:\Users\USER\Downloads\Music\New Songs")
OUTPUT_DIR = MOD_ROOT / "music" / "lasombra_court"

TRACKS = {
    "Ashen Banner.mp3": "lasombra_court_ashen_banner.ogg",
    "Black Chapel Bells.mp3": "lasombra_court_black_chapel_bells.ogg",
    "Black Velvet Throne.mp3": "lasombra_court_black_velvet_throne.ogg",
    "Court of Shadows.mp3": "lasombra_court_court_of_shadows.ogg",
    "Coven Night.mp3": "lasombra_court_coven_night.ogg",
    "Into the Night.mp3": "lasombra_court_into_the_night.ogg",
    "Lasombra Kiss.mp3": "lasombra_court_lasombra_kiss.ogg",
    "Lasombra Rise.mp3": "lasombra_court_lasombra_rise.ogg",
    "Lay Down.mp3": "lasombra_court_lay_down.ogg",
    "Lead Me To Embrace.mp3": "lasombra_court_lead_me_to_embrace.ogg",
    "Long Dark Light.mp3": "lasombra_court_long_dark_light.ogg",
    "Love's Rush.mp3": "lasombra_court_loves_rush.ogg",
    "Raven Chapel.mp3": "lasombra_court_raven_chapel.ogg",
    "Sappho's Candle.mp3": "lasombra_court_sapphos_candle.ogg",
    "Sappho's Dark Hush.mp3": "lasombra_court_sapphos_dark_hush.ogg",
    "Too Long Coming.mp3": "lasombra_court_too_long_coming.ogg",
    "Umbral Rite.mp3": "lasombra_court_umbral_rite.ogg",
    "Veiled Pursuit.mp3": "lasombra_court_veiled_pursuit.ogg",
    "Velvet Shadows.mp3": "lasombra_court_velvet_shadows.ogg",
}


def convert(source_dir: Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for src_name, dst_name in TRACKS.items():
        src = source_dir / src_name
        dst = OUTPUT_DIR / dst_name
        if not src.exists():
            raise FileNotFoundError(src)
        subprocess.run(
            [
                ffmpeg, "-y", "-i", str(src),
                "-vn", "-map_metadata", "-1",
                "-codec:a", "libvorbis", "-qscale:a", "6",
                str(dst),
            ],
            check=True,
        )
        print(f"Wrote {dst.name} ({dst.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    convert(source)