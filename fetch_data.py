import argparse
import base64
import json
import subprocess
import zipfile
from pathlib import Path

OWNER_REPO = "Stork343/llm-ranking-risk-data"
VERSION = "v1.0.0"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    destination = args.output_root.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    response = subprocess.run(["gh", "api", "repos/" + OWNER_REPO + "/contents/manifest.json?ref=" + VERSION],
                              check=True, capture_output=True, text=True)
    record = json.loads(response.stdout)
    manifest = json.loads(base64.b64decode(record["content"]))
    assert manifest["version"] == VERSION
    cache = destination / ".downloaded_inputs"
    cache.mkdir(exist_ok=True)
    archive_path = cache / "inputs-v1.zip"
    subprocess.run(["gh", "release", "download", VERSION, "--repo", OWNER_REPO,
                    "--pattern", "inputs-v1.zip", "--dir", str(cache), "--clobber"], check=True)
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
