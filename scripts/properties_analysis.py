# %%
import os
import toml
import pandas

COLORBLIND = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

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
                "bounded",
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
            "unbounded",
            data["RESULTS"]["VOLUME"]["KAA"],
            data["RESULTS"]["AREA"]["KAA"],
            data["RESULTS"]["AVG_DEPTH"]["KAA"],
            data["RESULTS"]["MAX_DEPTH"]["KAA"],
            data["RESULTS"]["AVG_HYDROPATHY"]["KAA"],
        ]
    )


# Prepare data to pandas
data = pandas.DataFrame(properties, columns=['State', 'Volume', 'Area', 'Average depth', 'Maximum depth', 'Average hydropathy'])
colors = {'bounded': COLORBLIND[0], 'unbounded': COLORBLIND[1]}
data['Color'] = data['State'].map(colors)
# %%
data.plot.scatter(x='Volume', y='Average depth', c='Color')
# %%
data.boxplot('Volume', by='State')
# %%
data.boxplot('Average depth', by='State')
