#!/usr/bin/env python3
"""Create and keep in sync the project issues, and assign people by GitHub username.

Source of truth: scripts/issues/issues.json (tasks) and scripts/issues/assignees.json (usernames).

What it does, every run:
  - creates issues that do not exist yet (matched by the ID in the title, for example [D0])
  - for issues that already exist and are open: fixes the title, phase (milestone), labels and
    assignees if they differ from issues.json, and prints every change
  - never touches closed issues
  - never rewrites an issue body, because owners write their description and estimate there.
    To refresh the body of specific issues on purpose: --update-body D0,D7  (or --update-body all)
  - assigns only people who have access to the repo (accepted the invitation)

Usage:
  python3 scripts/issues/create_issues.py OWNER/REPO --dry-run
  python3 scripts/issues/create_issues.py OWNER/REPO
  python3 scripts/issues/create_issues.py OWNER/REPO --update-body D0
  python3 scripts/issues/create_issues.py OWNER/REPO --create-only      # skip updating existing issues
It also runs from GitHub: Actions, "Create project issues", Run workflow.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARGS = sys.argv[1:]
REPO = ARGS[0]
DRY = "--dry-run" in ARGS
CREATE_ONLY = "--create-only" in ARGS
UPD = ""
if "--update-body" in ARGS:
    UPD = ARGS[ARGS.index("--update-body") + 1]
UPDATE_BODY = {x.strip() for x in UPD.split(",") if x.strip()}

ISSUES = json.load(open(os.path.join(HERE, "issues.json")))
HANDLES = json.load(open(os.path.join(HERE, "assignees.json")))

def gh(*a, write=True):
    cmd = ["gh", *a]
    if DRY and write:
        print("   DRY:", " ".join(cmd)[:140]); return ""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        if "already" not in r.stderr:
            print("WARNING:", r.stderr.strip()[:200])
        return None if not write else ""
    return r.stdout.strip()

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

def accounts():
    raw = gh("api", f"repos/{REPO}/collaborators", "--paginate", "--jq", ".[].login", write=False)
    collab = {x.lower() for x in raw.split()} if raw else None
    print("Accounts:")
    for name, h in HANDLES.items():
        if not h: s = "no username yet"
        elif collab is None: s = "could not check access"
        elif h.lower() in collab: s = "has access"
        else: s = "NO ACCESS YET (invitation not accepted?), will not be assigned"
        print(f"  {name:8} {h or '-':18} {s}")
    return collab

def owners_of(i):
    if i["assignees"] == "Everyone":
        return list(HANDLES)
    return [x.strip() for x in i["assignees"].split(",")]

def wanted_handles(i, collab):
    out = []
    for n in owners_of(i):
        h = HANDLES.get(n, "")
        if h and (collab is None or h.lower() in collab): out.append(h)
        else: print(f"   note: {n} cannot be assigned on {i['id']} yet")
    return out

def ensure_labels_and_milestones():
    for k, c in {"data":"1d76db","tyres":"d93f0b","pit":"fbca04","speed":"0e8a16","eval":"5319e7","all":"c5def5","lead":"bfd4f2"}.items():
        gh("label", "create", f"workstream: {k}", "--color", c, "--repo", REPO)
    for k, c in [("type: study","c2e0c6"),("type: apply","fef2c0"),("type: admin","e4e669"),("type: stretch","ededed"),("blocked","b60205")]:
        gh("label", "create", k, "--color", c, "--repo", REPO)
    for m in sorted({i["milestone"] for i in ISSUES}):
        gh("api", f"repos/{REPO}/milestones", "-f", f"title={m}")

def existing_issues():
    raw = gh("issue", "list", "--repo", REPO, "--state", "all", "--limit", "500", "--json",
             "number,title,state,labels,milestone,assignees", write=False)
    if not raw: return {}
    out = {}
    for it in json.loads(raw):
        m = re.match(r"\[(\w+)\]", it["title"])
        if m: out[m.group(1)] = it
    return out

def body_for(i):
    return BODY.format(**{**i, "depends": i["depends_on"] or "none"})

def main():
    collab = accounts()
    ensure_labels_and_milestones()
    existing = existing_issues()
    created = updated = same = skipped_closed = 0
    for i in ISSUES:
        title = f"[{i['id']}] {i['title']}"
        want_labels = {f"workstream: {i['workstream']}", f"type: {i['type']}"}
        want_users = wanted_handles(i, collab)
        cur = existing.get(i["id"])
        if cur is None:
            args = ["issue","create","--repo",REPO,"--title",title,"--body",body_for(i),
                    "--milestone",i["milestone"]]
            for l in sorted(want_labels): args += ["--label", l]
            for u in want_users: args += ["--assignee", u]
            print(f"CREATE [{i['id']}]"); gh(*args); created += 1; continue
        if CREATE_ONLY: same += 1; continue
        if cur["state"] != "OPEN":
            skipped_closed += 1; continue
        edit = []; notes = []
        if cur["title"] != title:
            edit += ["--title", title]; notes.append("title")
        cur_ms = (cur.get("milestone") or {}).get("title")
        if cur_ms != i["milestone"]:
            edit += ["--milestone", i["milestone"]]; notes.append(f"phase {cur_ms} -> {i['milestone']}")
        cur_labels = {l["name"] for l in cur["labels"]}
        managed = {l for l in cur_labels if l.startswith(("workstream:", "type:"))}
        for l in sorted(want_labels - cur_labels): edit += ["--add-label", l]; notes.append(f"+{l}")
        for l in sorted(managed - want_labels): edit += ["--remove-label", l]; notes.append(f"-{l}")
        cur_users = {a["login"] for a in cur["assignees"]}
        for u in sorted(set(want_users) - cur_users): edit += ["--add-assignee", u]; notes.append(f"+@{u}")
        for u in sorted(cur_users - set(want_users)):
            if collab is None or u.lower() in collab: edit += ["--remove-assignee", u]; notes.append(f"-@{u}")
        if "all" in UPDATE_BODY or i["id"] in UPDATE_BODY:
            edit += ["--body", body_for(i)]; notes.append("body rewritten")
        if edit:
            print(f"UPDATE [{i['id']}]: " + ", ".join(notes))
            gh("issue", "edit", str(cur["number"]), "--repo", REPO, *edit); updated += 1
        else:
            same += 1
    print(f"done: {created} created, {updated} updated, {same} unchanged, {skipped_closed} closed and left alone" + (" (dry run)" if DRY else ""))

if __name__ == "__main__":
    main()
