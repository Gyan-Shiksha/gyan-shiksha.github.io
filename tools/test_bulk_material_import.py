#!/usr/bin/env python3
"""Test bulk import in isolated tempdir; never alter real published materials."""
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "import_materials_csv.py"
COLUMNS = [
    "title", "standard", "subject", "category", "description", "url",
    "rights_confirmed", "viewer_checked", "rights_basis", "board", "year"
]


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def run(csv_path, output):
    return subprocess.run([sys.executable, str(SCRIPT), str(csv_path), "--output", str(output)],
                          text=True, capture_output=True)


with tempfile.TemporaryDirectory(prefix="gyan-material-batch-test-") as tmp:
    folder = Path(tmp)
    input_csv = folder / "owner-import.csv"
    output_json = folder / "materials.json"
    output_json.write_text("[]\n", encoding="utf-8")
    row = {
        "title": "ધોરણ 6 ગુજરાતી વર્કશીટ પાનું",
        "standard": "6",
        "subject": "ગુજરાતી",
        "category": "Worksheet",
        "description": "વિદ્યાર્થીઓના મૂળભૂત ભાષા અભ્યાસ માટે તૈયાર કરેલી પ્રેક્ટિસ વર્કશીટ.",
        "url": "https://drive.google.com/file/d/OwnerApprovedTestFile_A1/view",
        "rights_confirmed": "yes",
        "viewer_checked": "yes",
        "rights_basis": "original",
        "board": "GSEB",
        "year": "2025"
    }
    write_csv(input_csv, [row])
    passed = run(input_csv, output_json)
    assert passed.returncode == 0, passed.stderr
    assert len(json.loads(output_json.read_text(encoding="utf-8"))) == 1
    assert json.loads(output_json.read_text(encoding="utf-8"))[0]["year"] == "2025"
    assert run(input_csv, output_json).returncode == 0, "duplicate should be skipped"
    assert len(json.loads(output_json.read_text(encoding="utf-8"))) == 1
    previous = output_json.read_bytes()

    tests = [
        {"url": "https://mega.nz/folder/LeakyMasterFolder#MasterKey"},
        {"url": "https://drive.google.com/drive/folders/PrivateFolder"},
        {"rights_confirmed": "no"},
        {"viewer_checked": "no"},
        {"rights_basis": "on_the_internet"},
        {"url": "https://mega.nz/file/FAKE#KEY", "category": "Textbook", "rights_basis": "authorized_link"},
        {"year": "202x"},
    ]
    for changes in tests:
        bad = {**row, **changes, "title": "અન્ય ફાઇલની સુરક્ષા પરીક્ષા"}
        write_csv(input_csv, [bad])
        assert run(input_csv, output_json).returncode != 0, f"Invalid CSV accepted: {changes}"
        assert output_json.read_bytes() == previous, "invalid input unexpectedly changed public output"

    # One invalid row should prevent publishing even the valid row in same batch.
    write_csv(input_csv, [{**row, "url": "https://mega.nz/file/SafeIndividualKey#FileKey"},
                          {**row, "url": "https://mega.nz/folder/PrivateCollection#Key"}])
    assert run(input_csv, output_json).returncode != 0
    assert output_json.read_bytes() == previous

print("PASS: bulk import, year/board metadata, duplicates, folder protection, rights claims, and atomic rejection.")
