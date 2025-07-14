# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as ss

plt.rcParams["font.family"] = "Arial"
plt.rcParams['pdf.use14corefonts'] = True
outdir = "./MCF10A/MCF10A_CPC_analysis"
# %%
appended_data = []

# MCF10A_prometa_85min_032325_Image47_Lng
for image in range(1, 50):
    try:
        tmp = pd.read_csv(
            f"{outdir}/MCF10A_prometa_85min_032325_Image{image}_Lng.csv",
            index_col=0,
            header=0,
        )

        tmp["image"] = image
        appended_data.append(tmp)
    except FileNotFoundError:
        print(f"File not found for image {image}")
df = pd.concat(appended_data)

# some of the droplets were mislabeled as "d"
df["IC"] = [{"N": 0, "Y": 1, "d": 0}[i] for i in df["IC"]]
df["KT"] = [{"N": 0, "Y": 1, "N ": 0}[i] for i in df["KT"]]

df = df.reset_index()

location = pd.from_dummies(df[["IC", "KT"]], default_category="nonIC")
df["location"] = location
print(df.head())
area_95p = round(df.loc[df["location"] == "nonIC"]["Area"].quantile(0.95), 6)
radius_95p = round(np.sqrt(area_95p / np.pi), 6)
df["Radius"] = round(np.sqrt(df["Area"] / np.pi), 6)
s, p = ss.kstest(
    np.array(df.loc[df["location"] == "IC"]["Radius"]),
    np.array(df.loc[df["location"] == "nonIC"]["Radius"]),
)

# %%
# %%
for i, r in df.iterrows():
    df.loc[i, 'id'] = str(r['chr_no'])+"_"+str(r['image'])

print("Number of chromosomes:", len(
    np.unique(df.loc[(df["location"] != "KT")].id)))
print("Number of condensates:", len(df.loc[(df["location"] != "KT")].index))
# %%
fig, ax = plt.subplots()
sns.histplot(
    data=df.loc[df["location"].isin(["nonIC"])],
    x="Radius",
    hue="location",
    bins=30,
)
# sns.histplot(data = df, x = 'Area', hue = 'location', palette = [sns.color_palette()[0],sns.color_palette()[2],sns.color_palette()[1]])
plt.title(
    f"Radius of 2D projection by condensate location \n 95% nonIC: Radius = {radius_95p}"
)
plt.axvline(x=radius_95p, linestyle="--", color="gray")
plt.text(
    0.01,
    0.99,
    # f"p = {p:.3e} \nn={len(df.loc[df['location'].isin(['nonIC'])].index)}",
    f"n={len(df.loc[df['location'].isin(['nonIC'])].index)}",
    ha="left",
    va="top",
    transform=ax.transAxes,
)
plt.show()


# %% top and bottom subplots FIGURE S4C
fig, axs = plt.subplots(2, 1, sharex=True)
sns.histplot(
    data=df.loc[df["location"].isin(["IC"])],
    x="Radius",
    color="#f26522",
    binwidth=0.005,
    ax=axs[1],
    # kde=True,
)
sns.histplot(
    data=df.loc[df["location"].isin(["nonIC"])],
    x="Radius",
    color="#a7a9ac",
    binwidth=0.005,
    ax=axs[0],
    # kde=True,
)
# sns.histplot(data = df, x = 'Area', hue = 'location', palette = [sns.color_palette()[0],sns.color_palette()[2],sns.color_palette()[1]])
# plt.title(
#     f"Radius of 2D projection by condensate location \n 95% nonIC: Radius = {radius_95p}"
# )
axs[0].set_ylim(0, 120)
axs[1].set_ylim(0, 10)
axs[1].set_title("Stable (IC) Condensate Radius")
axs[0].set_title("Transient (Non-IC) Condensate Radius")
axs[0].axvline(x=radius_95p, linestyle="--", color="gray")
axs[1].axvline(x=radius_95p, linestyle="--", color="gray")

# axs[1].set_ylim(0, 8)
axs[1].text(
    0.99,
    0.99,
    f"n={len(df.loc[df['location'].isin(['IC'])].index)}\nmean = {np.mean(df.loc[df['location'].isin(['IC'])]['Radius']):.3g}\np = {p:.3e}",
    ha="right",
    va="top",
    transform=axs[1].transAxes,
)
axs[0].text(
    0.99,
    0.99,
    f"n={len(df.loc[df['location'].isin(['nonIC'])].index)}\nmean = {np.mean(df.loc[df['location'].isin(['nonIC'])]['Radius']):.3g}\n95% = {radius_95p:.3g}",
    ha="right",
    va="top",
    transform=axs[0].transAxes,
)
# convert um to nm
plt.xlabel("Radius (nm)")
plt.xticks(
    plt.xticks()[0][1:-1],
    [int(j * 1000) for j in plt.xticks()[0][1:-1]],
    fontsize=8,
)
# plt.savefig(
#     f"{outdir}/analysis/IC_vs_nonIC_manual_condensates_subplots_ALL_IMAGES_nm.pdf"
# )
plt.show()
# plt.close()


# %%
# plotting two swarmplots connected by lines
images_list = df["image"].unique()
# make pairs for lines
set1 = []
set2 = []
images = []
chr_nos = []
for image in images_list:
    tmp = df.loc[df["image"] == image]
    for chr_no in tmp["chr_no"].unique():
        tmp_small = tmp.loc[tmp["chr_no"] == chr_no]
        try:
            nonIC = tmp_small.loc[tmp_small["location"]
                                  == "nonIC"]["Radius"].values
            IC = tmp_small.loc[tmp_small["location"] == "IC"]["Radius"].values
            for n in nonIC:
                for i in IC:
                    set1.append(n)
                    set2.append(i)
                    images.append(image)
                    chr_nos.append(chr_no)
        except KeyError:
            pass

# %%
# Put into dataframe
df_sets = pd.DataFrame(
    {"nonIC": set1, "IC": set2, "image": images, "chr_no": chr_nos})
data = pd.melt(df_sets, id_vars=[
               "image", "chr_no"], value_vars=["nonIC", "IC"])
# %%

median_comparison = df_sets.groupby(["image", "chr_no"]).median()
# testing x is less than y with Wilcoxon Signed rank for paired samples
stat, p_signrank = ss.wilcoxon(
    x=median_comparison["nonIC"].values,
    y=median_comparison["IC"].values,
    alternative="less",
)

print(stat, p_signrank)
# %%
nonIC = df.loc[df["location"] == "nonIC"]["Radius"].values
IC = df.loc[df["location"] == "IC"]["Radius"].values
# testing x is less than y with Ranked sum for unpaired samples
stat, p_ranksum = ss.ranksums(x=nonIC, y=IC, alternative="less")
print(stat, p_ranksum)
# %%
# %%
# Plot
fig, ax = plt.subplots()
sns.swarmplot(data=data, x="variable", y="value", ax=ax)

# Now connect the dots
# Find idx0 and idx1 by inspecting the elements return from ax.get_children()
# ... or find a way to automate it
idx0 = 0
idx1 = 1
locs1 = ax.get_children()[idx0].get_offsets()
locs2 = ax.get_children()[idx1].get_offsets()

# before plotting, we need to sort so that the data points
# correspond to each other as they did in "set1" and "set2"
sort_idxs1 = np.argsort(set1)
sort_idxs2 = np.argsort(set2)

# revert "ascending sort" through sort_idxs2.argsort(),
# and then sort into order corresponding with set1
locs2_sorted = locs2[sort_idxs2.argsort()][sort_idxs1]

for i in range(locs1.shape[0]):
    x = [locs1[i, 0], locs2_sorted[i, 0]]
    y = [locs1[i, 1], locs2_sorted[i, 1]]
    ax.plot(x, y, color="black", alpha=0.05)
plt.title("Radius of CPC Condensates by Chromosome Location")
plt.xlabel("Location")
plt.ylabel("Radius (um)")

plt.tight_layout()
plt.annotate(
    text=f"P-val (Signed Rank Test): {p_signrank:.3e}\nP-val (Ranked Sum Test): {p_ranksum:.3e}\nAlt H: nonIC < IC",
    xy=(-0.35, 0.65),
)
# plt.savefig(
#     f"{outdir}/analysis/swarmplot_nonIC_vs_IC_matched.pdf"
# )
plt.show()

# %% Bootstrapping
################################################################################################
# Bootstrapping the 95% calculation across 10 images by choosing 5 images without replacement
# leaving the remaining 5 for Haspin linescans
################################################################################################

color_dict = {
    image: color for image, color in zip(images_list, sns.color_palette("tab20"))
}
outdir_b = f"{outdir}/analysis/bootstrapped"
radii_95 = []
plot = True
replace = True
if replace:
    name = "_with"
else:
    name = "_no"

num_plot = 5
num_bootstrap = df["image"].nunique() // 2
for it in range(100):
    sample = np.random.choice(images_list, num_bootstrap, replace=replace)
    remaining = [value for value in images_list if value not in sample]
    with open(f"{outdir_b}/sample{name}_replacement.txt", "a") as f:
        f.write(str(sample))
        f.write("\n")
    with open(f"{outdir_b}/remaining{name}_replacement.txt", "a") as f:
        f.write(str(remaining))
        f.write("\n")
    r = df.loc[(df["image"].isin(sample) & (
        df["location"] == "nonIC"))]["Radius"]
    r_95 = r.quantile(0.95)
    radii_95.append(r_95)
    if plot:
        if it < num_plot:
            ax = sns.kdeplot(r)
            plural = num_plot > 1
            plt.title(
                f"{num_plot} bootstrapped sample{({True:'s',False:''}[plural])} of nonIC Radii \n Each line shows 5 images (out of 10)"
            )
            kdeline = ax.lines[0]
            xs = kdeline.get_xdata()
            ys = kdeline.get_ydata()
            f = np.interp(r_95, xs, ys)
            plt.annotate(
                text=f"{r_95:.4f}",
                xy=(r_95 * 1.01, f + 0.02),
                fontsize=8,
            )
            ax.vlines(
                # , color=color_dict[image]
                r_95, 0, f, linestyle="--", linewidth=0.5
            )
# plt.savefig(
#     f"{outdir_b}/bootstrap_sample_distributions{name}_replacement.pdf"
# )

plt.close()
plt.show()
sns.histplot(radii_95, kde=True)
plt.annotate(
    text=f"Mean = {np.mean(radii_95):.4f}um\n25% = {np.percentile(radii_95, 25):.4f}um, 75% = {np.percentile(radii_95, 75):.4f}um\nSEM = {ss.sem(radii_95):.4f}um",
    xy=(0.13, 0.75),
    xycoords="figure fraction",
)
plt.title("Bootstrapped 95th percentile of nonIC Radius Distribution")
# plt.savefig(
# f"{outdir_b}/bootstrap_95%_radius{name}_replacement.pdf"
# )
plt.close()
plt.show()

# %%
ax = sns.kdeplot(r)
plt.title("Single bootstrapped sample of nonIC Radii \n 5 images (out of 50)")
# x, y = ax.get_lines()[0].get_data()
kdeline = ax.lines[0]
xs = kdeline.get_xdata()
ys = kdeline.get_ydata()
f = np.interp(r_95, xs, ys)
plt.annotate(
    text=str(r_95),
    xy=(r_95 * 1.01, f + 0.02),
    fontsize=8,
)
# , color=color_dict[image])
ax.vlines(r_95, 0, f, linestyle="--", linewidth=0.5)
plt.show()
# %%
