"""Render research/results/long_context_multilingual.json as assets/long_context_table.png."""
import json, sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

src = Path(sys.argv[1] if len(sys.argv) > 1 else "research/results/long_context_multilingual.json")
out = Path(sys.argv[2] if len(sys.argv) > 2 else "assets/long_context_table.png")
d = json.loads(src.read_text())
rows = {}
for r in d["rows"]:
    rows.setdefault(r["pad_tokens"], {})[r["limit"]] = r
limits = sorted({r["limit"] for r in d["rows"]})
lo, hi = limits[0], limits[-1]

header = ["Request placed after", "Default limit (%s)" % f"{lo:,}", "Limit %s" % f"{hi:,}", "Time at %s" % f"{hi:,}"]
cells, colors = [], []
GOOD, WARN, BAD, PLAIN = "#d9f2e0", "#fff1cc", "#fbdada", "#ffffff"
for pad in sorted(rows):
    a, b = rows[pad][lo], rows[pad][hi]
    label = "short input" if pad == 0 else "~%s tokens" % f"{pad:,}"
    cells.append([label, "%d / %d" % (a["correct"], a["n"]), "%d / %d" % (b["correct"], b["n"]), "%.2f s" % b["median_latency_s"]])
    acc_b = b["correct"] / b["n"]
    cb = GOOD if acc_b >= 0.8 else WARN if acc_b >= 0.5 else BAD
    ca = GOOD if a["correct"] / a["n"] >= 0.8 else WARN if a["correct"] / a["n"] >= 0.5 else BAD
    colors.append([PLAIN, ca, cb, PLAIN])

fig, ax = plt.subplots(figsize=(10.5, 0.42 * (len(cells) + 1)), dpi=160)
ax.axis("off")
t = ax.table(cellText=cells, colLabels=header, cellColours=colors, cellLoc="center",
             colColours=["#1f2937"] * 4, bbox=[0, 0, 1, 1])
t.auto_set_font_size(False); t.set_fontsize(12)
for (r, c), cell in t.get_celld().items():
    cell.set_edgecolor("#d1d5db")
    if r == 0:
        cell.get_text().set_color("white"); cell.get_text().set_weight("bold")
ax.set_title("laya-multilingual on long documents: accuracy on 20 support requests (8 languages)\n"
             "with the request placed at the end of a document of unrelated text",
             fontsize=13, weight="bold", pad=12)
fig.text(0.5, -0.06,
         "Green: 80%%+ correct. Amber: 50 to 79%%. Red: under 50%%. Time is the median per request on %s (%s). "
         "Reproduce: research/scripts/bench_long_context.py" % ("an Apple GPU" if d["device"] == "mps" else d["device"], "laya " + d["laya"]),
         ha="center", fontsize=9, color="#4b5563")
fig.savefig(out, bbox_inches="tight", facecolor="white")
print("wrote", out)
