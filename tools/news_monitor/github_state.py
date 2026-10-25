#!/usr/bin/env python3
"""Durable official-source state on a separate branch; optimistic writes only."""
import argparse
import base64
import gzip
import json
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

BRANCH = "news-monitor-state"
FILE = "tools/news_monitor/runtime-state.json"


def encode_state(data):
    state = json.loads(data)
    # fields/whatsapp duplicate the same content already present in the mail body.
    for event in state.get("outbox", {}).values():
        event.pop("fields", None)
        event.pop("whatsapp", None)
    packed = gzip.compress(json.dumps(state, ensure_ascii=False, separators=(",", ":")).encode(), mtime=0)
    return json.dumps({"encoding": "gzip+base64", "data": base64.b64encode(packed).decode()}, separators=(",", ":")).encode()


def decode_state(data):
    value = json.loads(data)
    if value.get("encoding") == "gzip+base64":
        unpacked = gzip.decompress(base64.b64decode(value["data"]))
        json.loads(unpacked)
        return unpacked
    return data


def api(path, method="GET", data=None):
    repo = os.environ["GITHUB_REPOSITORY"]
    if not repo or len(repo.split("/")) != 2:
        raise ValueError("Invalid repository")
    request = Request("https://api.github.com/repos/" + repo + path,
                      data=None if data is None else json.dumps(data).encode(), method=method,
                      headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"], "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"})
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except HTTPError as exc:
        if exc.code == 404:
            return None
        raise RuntimeError("GitHub state API returned HTTP " + str(exc.code)) from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["pull", "push"])
    parser.add_argument("--state", type=Path, required=True)
    args = parser.parse_args()
    meta = args.state.with_suffix(".meta.json")
    endpoint = "/contents/" + FILE
    if args.command == "pull":
        branch = api("/git/ref/heads/" + BRANCH)
        args.state.parent.mkdir(parents=True, exist_ok=True)
        if branch is None:
            # A missing branch is a first install. Missing file on an existing branch is damage.
            args.state.unlink(missing_ok=True)
            meta.write_text(json.dumps({"new_branch": True, "sha": None}))
            return
        result = api(endpoint + "?ref=" + BRANCH)
        if result is None or result.get("encoding") != "base64":
            raise RuntimeError("State branch exists but its state file is missing/unreadable")
        data = decode_state(base64.b64decode(result["content"]))
        args.state.write_bytes(data)
        meta.write_text(json.dumps({"new_branch": False, "sha": result["sha"]}))
        return
    status = json.loads(meta.read_text())
    if status["new_branch"]:
        # Publish a complete first state atomically with the branch ref. An interrupted
        # bootstrap cannot leave a visible empty branch that resembles lost state.
        parent = os.environ["GITHUB_SHA"]
        commit = api("/git/commits/" + parent)
        tree = api("/git/trees", "POST", {"base_tree": commit["tree"]["sha"], "tree": [
            {"path": FILE, "mode": "100644", "type": "blob", "content": encode_state(args.state.read_bytes()).decode()}
        ]})
        new_commit = api("/git/commits", "POST", {"message": "chore(monitor): establish first durable baseline", "tree": tree["sha"], "parents": [parent]})
        created = api("/git/refs", "POST", {"ref": "refs/heads/" + BRANCH, "sha": new_commit["sha"]})
        if created is None:
            raise RuntimeError("State branch creation was not acknowledged")
        first = api(endpoint + "?ref=" + BRANCH)
        if first is None or not first.get("sha"):
            raise RuntimeError("Initial state readback failed; delivery must not start")
        meta.write_text(json.dumps({"new_branch": False, "sha": first["sha"]}))
        return
    body = {"message": "chore(monitor): persist baseline, health and pending deliveries", "branch": BRANCH,
            "content": base64.b64encode(encode_state(args.state.read_bytes())).decode()}
    if status["sha"]:
        body["sha"] = status["sha"]
    result = api(endpoint, "PUT", body)
    if result is None or "content" not in result:
        raise RuntimeError("State write failed; delivery must not start")
    meta.write_text(json.dumps({"new_branch": False, "sha": result["content"]["sha"]}))


if __name__ == "__main__":
    main()
