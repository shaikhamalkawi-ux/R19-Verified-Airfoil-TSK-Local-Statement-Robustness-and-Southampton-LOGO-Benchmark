#!/usr/bin/env python3
"""Verify the 40 R21R8-EP11 new-state archives from public files only.

This checks bytes, ZIP CRC, journal coverage and member SHA-256. It does not
refit models or compare with unavailable original historical fitted-state bytes.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import zipfile

FAILURES = {("F5_fold00_compact", "relearn", 141),
            ("F5_fold02_reference", "relearn", 115)}

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def verify_one(name, archive_dir, checksums, certificate):
    task = name.removesuffix("_NEW_STATES_AND_AUDIT.zip")
    path = archive_dir / name
    expected = certificate[task]
    assert path.is_file() and path.stat().st_size == expected["bytes"], name
    digest = sha256(path)
    assert digest == expected["sha256"] == checksums[name], name
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) and z.testzip() is None, name
        assert all(not n.startswith("/") and ".." not in PurePosixPath(n).parts for n in names), name
        allowed = {task + "_journal.jsonl", task + "_summary.json"}
        state_re = re.compile(r"NEW_STATE/" + re.escape(task) + r"_(fixed|relearn)_rep\d{3}\.npz")
        assert all(n in allowed or state_re.fullmatch(n) for n in names), name
        summary = json.loads(z.read(task + "_summary.json"))
        journal = [json.loads(line) for line in z.read(task + "_journal.jsonl").splitlines() if line.strip()]
        assert len(journal) == 700, name
        seen, successes, failures = set(), 0, 0
        for row in journal:
            branch, rep = row["branch"], int(row["replicate"])
            assert branch in ("fixed", "relearn") and 0 <= rep < (500 if branch == "fixed" else 200), name
            assert (branch, rep) not in seen and row["verified_historical_result"] is True, name
            seen.add((branch, rep))
            if row["status"] == "FAILED":
                assert (task, branch, rep) in FAILURES and not row.get("new_state_file"), name
                failures += 1
            else:
                assert row["status"] == "success" and row["all_pass"] is True and all(row["checks"].values()), name
                member = "NEW_STATE/" + row["new_state_file"]
                assert member in names and hashlib.sha256(z.read(member)).hexdigest() == row["new_state_SHA256"], name
                successes += 1
        assert len(seen) == 700 and successes + failures == 700, name
        assert sum(n.startswith("NEW_STATE/") for n in names) == successes, name
        assert summary["task"] == task and summary["verified_attempts"] == 700, name
        assert summary["successful_replays"] == successes and summary["reproduced_historical_fcm_failures"] == failures, name
        assert summary["full_task_complete"] is True and "NEWLY computed" in summary["claim_boundary"], name
    return {"file": name, "bytes": path.stat().st_size, "sha256": digest,
            "attempts": 700, "new_states": successes, "failures": failures}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archives", type=Path, default=Path("."))
    parser.add_argument("--manifest", type=Path, default=Path("SHA256SUMS.txt"))
    parser.add_argument("--certificate", type=Path, default=Path("R21R8_FULL40_Completion_Certificate.json"))
    args = parser.parse_args()
    checksums = {}
    for line in args.manifest.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        checksums[name.strip()] = digest.lower()
    source = json.loads(args.certificate.read_text())
    certificate = {row["task"]: row for row in source["completed_task_archives"]}
    names = sorted(task + "_NEW_STATES_AND_AUDIT.zip" for task in certificate)
    assert len(names) == 40 and all(name in checksums for name in names)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(lambda name: verify_one(name, args.archives, checksums, certificate), names))
    result = {"archives": len(rows), "bytes": sum(row["bytes"] for row in rows),
              "attempts": sum(row["attempts"] for row in rows),
              "new_states": sum(row["new_states"] for row in rows),
              "reproduced_failures": sum(row["failures"] for row in rows)}
    assert result == {"archives": 40, "bytes": 773361055, "attempts": 28000,
                      "new_states": 27998, "reproduced_failures": 2}
    print("PASS", json.dumps(result))

if __name__ == "__main__":
    main()

