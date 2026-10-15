import argparse
import json
import zipfile
from pathlib import Path

import requests


BASE_URL = "https://raw.githubusercontent.com/Stork343/llm-ranking-risk-data/v1.0.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    destination = args.output_root.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    response = requests.get(BASE_URL + "/manifest.json", timeout=(15, 120))
    response.raise_for_status()
    manifest = response.json()
    assert manifest["version"] == "v1.0.0"
    cache = destination / ".downloaded_inputs"
    cache.mkdir(exist_ok=True)
    archive_path = cache / "inputs-v1.zip"
    with requests.get(manifest["archive"]["download_url"], stream=True, timeout=(15, 120)) as response:
        response.raise_for_status()
        with archive_path.open("wb") as stream:
            for block in response.iter_content(1024 * 1024):
                stream.write(block)
    assert archive_path.stat().st_size == manifest["archive"]["bytes"]
    expected = {item["path"]: item["bytes"] for item in manifest["files"]}
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(expected)
        for item in archive.infolist():
            assert item.file_size == expected[item.filename]
            target = (destination / item.filename).resolve()
            assert target.is_relative_to(destination)
            if target.exists():
                assert target.read_bytes() == archive.read(item), item.filename
            else:
                archive.extract(item, destination)
    print(json.dumps({"complete": True, "version": manifest["version"], "files": len(expected),
                      "output_root": str(destination)}))


if __name__ == "__main__":
    main()
