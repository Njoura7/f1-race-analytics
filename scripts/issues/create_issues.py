#!/usr/bin/env python3
"""Create the project labels, milestones and issues, and assign people by GitHub username.

Usernames live in scripts/issues/assignees.json. Add or fix a username there and run again.
Running twice is safe: issues whose title already exists are skipped.

Usage:
  python3 scripts/issues/create_issues.py OWNER/REPO --dry-run   # show what would happen
  python3 scripts/issues/create_issues.py OWNER/REPO             # create everything

It can also run from GitHub: Actions, "Create project issues", Run workflow.
"""
import json, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
repo = sys.argv[1]
dry = "--dry-run" in sys.argv
issues = json.load(open(os.path.join(here, "issues.json")))
handles = json.load(open(os.path.join(here, "assignees.json")))

def gh(*a, write=True):
    cmd = ["gh", *a]
    if dry and write:
        print("DRY:", " ".join(cmd)[:150]); return ""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        if "already" not in r.stderr:
            print("WARNING:", r.stderr.strip()[:200])
        return None if not write else ""
    return r.stdout.strip()

# Who can be assigned? Only people who accepted the invitation.
raw = gh("api", f"repos/{repo}/collaborators", "--paginate", "--jq", ".[].login", write=False)
collab = {x.lower() for x in raw.split()} if raw else None
print("Accounts:")
for name, h in handles.items():
    if not h:
        status = "no username yet"
    elif collab is None:
        status = "could not check access"
    elif h.lower() in collab:
        status = "has access"
    else:
        status = "NO ACCESS YET (invitation not accepted?) - will not be assigned"
    print(f"  {name:8} {h or '-':18} {status}")

def can_assign(name):
    h = handles.get(name, "")
    return bool(h) and (collab is None or h.lower() in collab)

for k, c in {"data":"1d76db","tyres":"d93f0b","pit":"fbca04","speed":"0e8a16","eval":"5319e7","all":"c5def5","lead":"bfd4f2"}.items():
    gh("label", "create", f"workstream: {k}", "--color", c, "--repo", repo)
for k, c in [("type: study","c2e0c6"),("type: apply","fef2c0"),("type: admin","e4e669"),("type: stretch","ededed"),("blocked","b60205")]:
    gh("label", "create", k, "--color", c, "--repo", repo)
for m in sorted({i["milestone"] for i in issues}):
    gh("api", f"repos/{repo}/milestones", "-f", f"title={m}")

existing = set()
raw = gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "500", "--json", "title", "--jq", ".[].title", write=False)
if raw: existing = set(raw.split("\n"))

BODY = """**Owner(s):** {assignees}
**Reviewer:** {reviewer}
**Phase:** {milestone}
**Depends on:** {depends}

## What this is
{title}

## Description (owner fills in)
Write 2 to 4 lines: what exactly you will do and what you will deliver.

## Your estimate in hours (owner fills in)
Our starting estimate is **{hours} h per person**. Change it if you think it is wrong, and say why.

## Your plan or suggestions (owner fills in)
Anything you would do differently, a better idea, or a risk you see.

## Done when
- [ ] {done_when}

**Definition of done:** reviewed by another member, notebook or tests run end to end, docstring written, docs updated if behaviour changed.

Please fill in the three sections above before the next sync.
"""
ALL = [n for n in handles if n != "Aziz"]
made = skipped = 0
for i in issues:
    title = f"[{i['id']}] {i['title']}"
    if title in existing:
        skipped += 1; continue
    body = BODY.format(**{**i, "depends": i["depends_on"] or "none"})
    args = ["issue","create","--repo",repo,"--title",title,"--body",body,"--milestone",i["milestone"],
            "--label",f"workstream: {i['workstream']}","--label",f"type: {i['type']}"]
    owners = ALL + ["Aziz"] if i["assignees"] == "Everyone" else [x.strip() for x in i["assignees"].split(",")]
    for n in owners:
        if can_assign(n):
            args += ["--assignee", handles[n]]
        else:
            print(f"  note: {n} not assigned on {i['id']}")
    gh(*args); made += 1
print(f"done: {made} created, {skipped} already existed" + (" (dry run)" if dry else ""))
