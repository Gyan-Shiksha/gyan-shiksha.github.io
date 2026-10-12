#!/usr/bin/env python3
"""Isolated smoke tests: never publish sample material to the actual website."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "add_material.py"
BASE = {
    "GITHUB_REPOSITORY": "Gyan-Shiksha/gyan-shiksha.github.io",
    "INPUT_TITLE": "ધોરણ 7 ગુજરાતી ચિત્ર અને નોંધ",
    "INPUT_STANDARD": "7",
    "INPUT_SUBJECT": "ગુજરાતી",
    "INPUT_CATEGORY": "Image",
    "INPUT_DESCRIPTION": "ગુજરાતી વિષય માટે શિક્ષણમાં ઉપયોગી ચિત્ર અને સંક્ષિપ્ત મૂળ નોંધ.",
    "INPUT_URL": "https://drive.google.com/file/d/TestIndividualFile_A1/view",
    "INPUT_RIGHTS_CONFIRMED": "true",
}


def run(root, **overrides):
    values = dict(os.environ)
    values.update(BASE)
    values.update(overrides)
    return subprocess.run([sys.executable, str(root / "tools/add_material.py")],
                          cwd=root, env=values, text=True, capture_output=True)


with tempfile.TemporaryDirectory(prefix="gyan-materials-test-") as name:
    root = Path(name)
    (root / "data").mkdir()
    (root / "tools").mkdir()
    shutil.copyfile(SOURCE, root / "tools/add_material.py")
    data = root / "data/materials.json"
    data.write_text("[]\n", encoding="utf-8")

    good = run(root)
    assert good.returncode == 0, good.stderr
    records = json.loads(data.read_text(encoding="utf-8"))
    assert len(records) == 1 and records[0]["standard"] == "7"
    assert records[0]["category"] == "Image" and records[0]["rights_verified"] is True

    assert run(root).returncode != 0, "duplicate file must fail"
    assert run(root, INPUT_URL="https://drive.google.com/drive/folders/PrivateFolder_A",
               INPUT_TITLE="Private Folder Link").returncode != 0, "Drive folder must fail"
    assert run(root, INPUT_URL="https://mega.nz/folder/AbC123#FolderKey",
               INPUT_TITLE="MEGA Folder Link").returncode != 0, "MEGA folder must fail"
    assert run(root, INPUT_URL="https://drive.google.com.evil.invalid/file/d/X/view",
               INPUT_TITLE="Spoofed Drive Domain").returncode != 0, "spoofed host must fail"
    assert run(root, INPUT_RIGHTS_CONFIRMED="false",
               INPUT_URL="https://mega.nz/file/SafeIndividualFile#FileKey").returncode != 0, "copyright checkbox must fail"
    assert run(root, INPUT_URL="javascript:alert(1)",
               INPUT_TITLE="Unsafe JS Link").returncode != 0, "unsafe scheme must fail"

    mega = run(root, INPUT_URL="https://mega.nz/file/SafeIndividualFile#FileKey",
               INPUT_CATEGORY="PDF", INPUT_STANDARD="College", INPUT_TITLE="College PDFs and Notes")
    assert mega.returncode == 0, mega.stderr
    docs = run(root, INPUT_URL="https://docs.google.com/presentation/d/Slides_A2/edit",
               INPUT_CATEGORY="Presentation", INPUT_STANDARD="Teacher", INPUT_TITLE="Teachers presentation guide")
    assert docs.returncode == 0, docs.stderr
    drive_open = run(root, INPUT_URL="https://drive.google.com/open?id=DriveFileView_A3",
                     INPUT_CATEGORY="Audio", INPUT_STANDARD="General", INPUT_TITLE="General Study Audio Guide")
    assert drive_open.returncode == 0, drive_open.stderr

print("PASS: any grade/category, individual Drive/Docs/MEGA files, duplicate protection, rights verification, folder & URL safety.")
