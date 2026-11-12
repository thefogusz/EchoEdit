"""Scan this machine for every way to do each job in the Data Echooo video pipeline (tools/providers.json).
Checks API keys (env vars / config files: only whether they exist, never their values), CLIs on PATH or known
install folders, Python packages and local library folders. MCP connectors cannot be seen from Python: the agent
compares the printed `mcp_tools` names with its own tool list and adds those options.
usage: python tools/capabilities.py [type1|type2|type3] [--json]"""
import glob, importlib.util, json, os, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
P = json.loads((ROOT / "tools/providers.json").read_text(encoding="utf-8"))
home = pathlib.Path.home()
exp = lambda p: str(p).replace("~", str(home))

def check(o):
    """-> (status, detail). status: yes | no | mcp(agent checks) ."""
    if o["kind"] == "mcp": return "mcp", "agent: look for " + ", ".join(o.get("mcp_tools", []))
    found, missing = [], []
    for e in o.get("env", []):
        (found if os.environ.get(e) else missing).append(f"env {e}")
    for f in o.get("files", []):
        ok = pathlib.Path(exp(f)).exists()
        if ok and f.endswith(".env"):  # a key file counts only if it has a non-empty KEY= line (value never printed)
            ok = any("=" in l and l.split("=", 1)[1].strip() for l in pathlib.Path(exp(f)).read_text(encoding="utf-8", errors="ignore").splitlines() if not l.startswith("#"))
        (found if ok else missing).append(f"file {f}")
    for c in o.get("cli", []):
        hit = shutil.which(c) or any(glob.glob(exp(g)) for g in o.get("globs", [])) or (c == "earshot" and pathlib.Path("C:/earshot").exists())
        (found if hit else missing).append(f"cli {c}")
    for m in o.get("python", []):
        (found if importlib.util.find_spec(m) else missing).append(f"py {m}")
    for p in o.get("paths", []):
        hit = glob.glob(str(ROOT / p)) or glob.glob(exp(p))
        (found if hit else missing).append(f"path {p}")
    keys_or_files = [x for x in found if x.startswith(("env", "file"))]
    if o["kind"] == "api":  # an API option needs at least one key source
        ok = bool(keys_or_files)
    else:
        ok = not missing or (bool(found) and not any(x.startswith(("cli", "py")) for x in missing))
    return ("yes" if ok else "no"), ("found: " + ", ".join(found) if found else "") + ("  missing: " + ", ".join(missing) if missing else "")

report = {}
for cap, spec in P["capabilities"].items():
    report[cap] = {"label": spec["label"], "options": []}
    for o in spec["options"]:
        st, det = check(o)
        report[cap]["options"].append({"id": o["id"], "kind": o["kind"], "cost": o["cost"], "status": st, "detail": det, "note": o.get("note", ""), "run": o.get("run", "")})

if "--json" in sys.argv:
    print(json.dumps(report, ensure_ascii=False, indent=1)); sys.exit()
mark = {"yes": "✅", "no": "❌", "mcp": "❓"}
cost = {"free": "ฟรี", "plan": "ในแผนที่มี", "paid": "เสียเงิน"}
for cap, r in report.items():
    print(f"\n## {r['label']} ({cap})")
    for o in r["options"]:
        print(f"  {mark[o['status']]} {o['id']:<18} [{o['kind']}, {cost[o['cost']]}]  {o['detail']}")
# bundles: for the asked type, list what each needed capability can use here (pick the fewest tools)
typ = next((a for a in sys.argv[1:] if a.startswith("type")), None)
if typ and typ in P.get("bundles", {}):
    print(f"\n## ชุดเครื่องมือสำหรับ {typ}: ทางที่ใช้ได้ในเครื่องนี้ต่องาน (เลือกชุดที่ใช้เครื่องมือน้อยที่สุด)")
    for cap, ids in P["bundles"][typ]["needs"].items():
        ok = [o["id"] for o in report[cap]["options"] if o["id"] in ids and o["status"] != "no"]
        print(f"  {report[cap]['label']}: " + (" / ".join(ok) if ok else "❌ ไม่มีทางไหนเลย"))
    print("  ตัวอย่างชุด: " + "; ".join(f"{b['id']} = {' + '.join(b['tools'])}" for b in P["bundles"]["examples"]))
    print("  กฎของเจ้าของ: " + P["bundles"]["owner_rule"])
print("\n❓ = MCP: the agent checks its connected tools; ✅/❌ = checked on this machine. Offer the ✅/❓ options to the user, cheapest first; paid ones need a yes with the price.")
