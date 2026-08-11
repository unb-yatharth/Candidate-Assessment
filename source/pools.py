# -*- coding: utf-8 -*-
"""Builds one global question bank tagged by category + difficulty, then derives
a per-level pool. Levels draw only from their permitted difficulty tiers."""
import random
import testbank as T
import extra_junior as EJ
import extra_senior as ES
import extra_cat as EC
import taxonomy as TX

ALL_AUTO = (list(T.INTERN_AUTO) + list(T.ASSOC_AUTO) + list(T.MGR_AUTO) + list(T.SR_AUTO)
            + list(EJ.INTERN_EXTRA) + list(EJ.ASSOC_EXTRA)
            + list(ES.MGR_EXTRA) + list(ES.SR_EXTRA) + list(EC.NEW))

ALL_WRITTEN = {
    "intern":    list(T.INTERN_WRITTEN) + list(EJ.INTERN_WRITTEN_EXTRA),
    "associate": list(T.ASSOC_WRITTEN) + list(EJ.ASSOC_WRITTEN_EXTRA),
    "manager":   list(T.MGR_WRITTEN) + list(ES.MGR_WRITTEN_EXTRA),
    "senior":    list(T.SR_WRITTEN) + list(ES.SR_WRITTEN_EXTRA),
}

LABEL = {"intern": "Intern", "associate": "Associate", "manager": "Manager", "senior": "Sr. Manager"}
DIFF_LABEL = {"intern": "Foundational", "associate": "Intermediate",
              "manager": "Intermediate to advanced", "senior": "Advanced"}


def tag_all():
    """Attach category + difficulty to every question. Fails loudly on anything untagged."""
    missing = []
    for q in ALL_AUTO:
        t = TX.MAP.get(q["id"])
        if not t:
            missing.append(q["id"]); continue
        q["cat"], q["diff"] = t
        q["sec"] = t[0]                       # section IS the category now
    if missing:
        raise SystemExit("UNTAGGED QUESTIONS: " + ", ".join(missing))
    ids = [q["id"] for q in ALL_AUTO]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit("DUPLICATE IDS: " + ", ".join(sorted(dupes)))
    return ALL_AUTO


def build():
    tag_all()
    out = {}
    for key in ("intern", "associate", "manager", "senior"):
        allowed = TX.LEVEL_DIFF[key]
        pools = {}
        for cat in TX.CATEGORIES:
            if cat not in TX.SLOTS[key]:
                continue
            pools[cat] = [q for q in ALL_AUTO if q["cat"] == cat and q["diff"] in allowed]
        out[key] = {
            "label": LABEL[key],
            "difficulty": DIFF_LABEL[key],
            "minutes": TX.MINUTES[key],
            "slots": TX.SLOTS[key],
            "wslots": TX.WRITTEN_SLOTS[key],
            "pools": pools,
            "written": ALL_WRITTEN[key],
        }
    return out


def rebalance(levels, seed=20260810):
    """Spread correct answers evenly across option positions in the stored bank."""
    counts = {}
    seen = set()
    for i, q in enumerate(ALL_AUTO):
        if q["type"] != "mcq" or q["id"] in seen:
            continue
        seen.add(q["id"])
        n = len(q["opts"]); target = i % n
        shift = (target - q["a"]) % n
        if shift:
            q["opts"] = q["opts"][-shift:] + q["opts"][:-shift]
            q["a"] = target
        counts[chr(65 + q["a"])] = counts.get(chr(65 + q["a"]), 0) + 1
    return counts


def audit(levels):
    lines = []
    for key, lv in levels.items():
        tot = sum(lv["slots"].values())
        lines.append(f"{key.upper():10s} {tot} questions  ·  {lv['difficulty']}  ·  "
                     f"{lv['minutes']} min  ·  {lv['wslots']} written (pool {len(lv['written'])})")
        for cat, n in lv["slots"].items():
            have = len(lv["pools"][cat]); need = n * 2
            ratio = have / need if need else 0
            flag = "OK  " if have >= need else "SHORT"
            bar = "*" * int(min(ratio, 4) * 6)
            lines.append(f"   {cat:26s} {n:2d} asked  need {need:2d}  pool {have:3d}  {ratio:4.2f}x {flag} {bar}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    L = build()
    print(audit(L))
    print("answer positions after rebalance:", rebalance(L))
    print("total questions in bank:", len(ALL_AUTO))
    from collections import Counter
    c = Counter((q["cat"], q["diff"]) for q in ALL_AUTO)
    print("\nbank composition:")
    for cat in TX.CATEGORIES:
        row = "  ".join(f"{d}:{c[(cat,d)]:3d}" for d in ("low", "mid", "high"))
        print(f"   {cat:26s} {row}   total {sum(c[(cat,d)] for d in ('low','mid','high'))}")
