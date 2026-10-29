"""Build a reproducible, installable extension ZIP using only runtime files."""
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_FILES = ("manifest.json", "script.js", "icon.png")


def main():
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    if not re.fullmatch(r"\d+(?:\.\d+){0,3}", version):
        raise ValueError("Manifest version must contain one to four numeric components")
    if manifest.get("manifest_version") != 3:
        raise ValueError("Expected Manifest V3")
    referenced = set(manifest.get("icons", {}).values())
    icon = manifest.get("action", {}).get("default_icon")
    referenced.update(icon.values() if isinstance(icon, dict) else [icon] if icon else [])
    for content_script in manifest.get("content_scripts", []):
        referenced.update(content_script.get("js", []))
        referenced.update(content_script.get("css", []))
    if not referenced <= set(RUNTIME_FILES):
        raise ValueError(f"Update the package allowlist for: {referenced - set(RUNTIME_FILES)}")
    for name in RUNTIME_FILES:
        if not (ROOT / name).is_file():
            raise FileNotFoundError(name)
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / f"TCDD-Koltuk-Bulucu-v{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for name in RUNTIME_FILES:
            entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            package.writestr(entry, (ROOT / name).read_bytes())
    with zipfile.ZipFile(archive) as package:
        if package.namelist() != list(RUNTIME_FILES) or package.testzip() is not None:
            raise ValueError("Invalid extension archive")
        for name in RUNTIME_FILES:
            if package.read(name) != (ROOT / name).read_bytes():
                raise ValueError(f"Archive content mismatch: {name}")
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "SHA256SUMS.txt").write_text(f"{checksum}  {archive.name}\n", encoding="ascii")
    print(f"Created {archive.name} ({archive.stat().st_size:,} bytes)")
    print(f"SHA256: {checksum}")


if __name__ == "__main__":
    main()
