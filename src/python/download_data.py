from pathlib import Path
import kagglehub
import shutil

PROJECT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT / "data"

DATA_DIR.mkdir(exist_ok=True)

print("[+] Downloading Santa 2026 competition data...")

source = Path(
    kagglehub.competition_download("santa-2026")
)

print(f"[+] KaggleHub cache: {source}")

print("[+] Inspecting downloaded files...")

for item in sorted(source.rglob("*")):
    if item.is_file():
        relative = item.relative_to(source)
        destination = DATA_DIR / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not destination.exists():
            shutil.copy2(item, destination)

        print(f"    {relative}")

print("\n[+] Download completed.")
print(f"[+] Local data directory: {DATA_DIR}")
