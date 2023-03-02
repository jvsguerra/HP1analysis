import os

import matplotlib.pyplot as plt
import numpy
import pandas
import toml

COLORBLIND = [
    "#377eb8",
    "#ff7f00",
    "#4daf4a",
    "#f781bf",
    "#a65628",
    "#984ea3",
    "#999999",
    "#e41a1c",
    "#dede00",
]

# Get structures in bound and unbound states
bounded = sorted(os.listdir("../data/bounded"))
unbounded = sorted(os.listdir("../data/unbounded"))


# Get properties of HIV-1 protease active site
properties = []

for pdb in bounded:
    data = toml.load(
        os.path.join(
            "..", "results", "bounded", pdb[:-4], f"{pdb[:-4]}.KVFinder.results.toml"
        )
    )
    properties.append(
        [
            "Bounded"
            if pdb[:-4] not in ["1jp5", "2hrp"]
            else "Bounded (Alternative conformation)",
            data["RESULTS"]["VOLUME"]["KAA"],
            data["RESULTS"]["AREA"]["KAA"],
            data["RESULTS"]["AVG_DEPTH"]["KAA"],
            data["RESULTS"]["MAX_DEPTH"]["KAA"],
            data["RESULTS"]["AVG_HYDROPATHY"]["KAA"],
        ]
    )

for pdb in unbounded:
    data = toml.load(
        os.path.join(
            "..", "results", "unbounded", pdb[:-4], f"{pdb[:-4]}.KVFinder.results.toml"
        )
    )
    properties.append(
        [
            "Unbounded",
            data["RESULTS"]["VOLUME"]["KAA"],
            data["RESULTS"]["AREA"]["KAA"],
            data["RESULTS"]["AVG_DEPTH"]["KAA"],
            data["RESULTS"]["MAX_DEPTH"]["KAA"],
            data["RESULTS"]["AVG_HYDROPATHY"]["KAA"],
        ]
    )


# Prepare data to pandas
data = pandas.DataFrame(
    properties,
    columns=[
        "State",
        "Volume",
        "Area",
        "Average depth",
        "Maximum depth",
        "Average hydropathy",
    ],
)
colors = {
    "Bounded": COLORBLIND[0],
    "Unbounded": COLORBLIND[1],
    "Bounded (Alternative conformation)": COLORBLIND[2],
}
data["Color"] = data["State"].map(colors)

## Plot violinplot
fig, ax = plt.subplots(1, 1, figsize=(6, 10), clear=True, tight_layout=True)
vp = ax.violinplot(
    [
        data["Volume"][data["State"] == "Bounded"],
        data["Volume"][data["State"] == "Unbounded"],
    ],
    positions=[1, 1.5],
    showmeans=False,
    showmedians=False,
    showextrema=False,
    widths=0.3,
)

for pc, color in zip(vp["bodies"], COLORBLIND):
    pc.set_facecolor(color)
    pc.set_edgecolor("black")

bp = ax.boxplot(
    [
        data["Volume"][data["State"] == "Bounded"],
        data["Volume"][data["State"] == "Unbounded"],
    ],
    notch=False,
    positions=[1, 1.5],
    showmeans=True,
    labels=["Bounded", "Unbounded"],
    patch_artist=True,
    flierprops=dict(
        marker="o",
        markerfacecolor="white",
        markeredgecolor="black",
        markersize=7,
        linewidth=0.1,
        alpha=0.5,
    ),
    medianprops=dict(linestyle="-", linewidth=1, color="tab:red"),
    meanprops=dict(
        marker="o",
        linewidth=0.1,
        markeredgecolor="black",
        markerfacecolor="tab:red",
        markersize=7,
    ),
    widths=0.1,
)
# Conditional coloring
for patch, color in zip(bp["boxes"], COLORBLIND):
    patch.set_facecolor(color)

ax.set_ylabel("Volume (Å³)", size=20)
ax.set_xlabel(None)
ax.set_ylim(0, 2500)
ax.set_xlim(0.75, 1.75)
ax.set_yticks(numpy.arange(0, 2400, step=250))
ax.tick_params(axis="x", labelsize=15)
ax.tick_params(axis="y", labelsize=15)
ax.grid(which="major", axis="both", linestyle="-", alpha=0.75)
ax.grid(which="minor", axis="both", linestyle="-", alpha=0.2)

plt.savefig("../results/volume-per-state.png", dpi=300)

# plt.show()
