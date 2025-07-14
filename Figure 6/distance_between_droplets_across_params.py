# %%
from scipy.stats import kstest
from scipy.integrate import cumtrapz
from matplotlib import cm
from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Rectangle
from scipy.stats import gaussian_kde
import ast
from itertools import combinations
import scipy.stats as ss
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
# %%

indir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting"
outdir = (
    f"{indir}/distance_between_droplets/"
)


def make_long_dist_df(indir, file):
    # dist = pd.read_csv(f"{indir}/distance_between_droplets.csv",converters={'distances': pd.eval})
    dist = pd.read_csv(f"{indir}/{file}", header=0)
    long_dist_df = pd.DataFrame(
        columns=["seed", "cpc", 'cohesin', 'time', 'distance']
        # columns=["cpc", "cohesin", "distance"]
    )

    for i, r in dist.iterrows():
        dist_list = str(r["distances"])[1:-2].split(" ")
        try:
            dist_list = [float(d) for d in dist_list]
            for d in dist_list:
                try:
                    random_seed = r["rand_ID"]
                except KeyError:
                    CPC_to_seed_dict = {0.125: 1, 0.1: 2, 0.12: 3, 0.15: 4,
                                        0.173: 5, 0.22: 6, 0.25: 7, 0.3: 8, 0.35: 9, 0.2: 10}
                    random_seed = CPC_to_seed_dict[r["cpc"]]
                long_dist_df = pd.concat(
                    [
                        long_dist_df,
                        pd.DataFrame(
                            {
                                "seed": [random_seed],
                                "time": [r["time"]],
                                "cpc": [r["cpc"]],
                                "cohesin": [r["cohesin"]],
                                "distance": [d],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
        except ValueError:
            pass
    return long_dist_df


# %%

# long_dist_df = make_long_dist_df(
#     indir,
#     "simulated_droplet_distributions/simulated_droplet_distances_e_0.01_noisy_cohesin_chr_lengths.csv",
# )
# sns.histplot(
#     data=long_dist_df,
#     x="distance",
#     palette=sns.color_palette("muted"),
#     binwidth=0.1,
#     stat="probability",
#     common_norm=False,
#     kde=True,
# )

# # sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()
# plt.savefig(f"{outdir}distances_between_droplets_swarmplot_0.0075.png")
# %%


# long_dist_df = make_long_dist_df(
#     indir,
#     file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0075_domain_0_2_chr_lengths.csv",
# )
# sns.histplot(
#     data=long_dist_df, x="distance", palette=sns.color_palette("muted"), bins=30
# )

# # sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()
# %%
# outdir = f"{indir}/radii_lineplots_kymographs/domain_0_1_eps_0.0075/"

# long_dist_df2 = make_long_dist_df(
#     indir,
#     file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0075_domain_0_1_chr_lengths.csv",
# )
# sns.histplot(
#     data=long_dist_df2, x="distance", palette=sns.color_palette("muted"), bins=30
# )

# # sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()

# %%

# long_dist_df2 = make_long_dist_df(
#     indir,
#     file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0075_noisy_cohesin_sd_0.11.csv",
# )
# %%
# outdir = f"{indir}/radii_lineplots_kymographs/domain_0_2_noisy_cohesin_sd_0.11"

# sns.histplot(
#     data=long_dist_df2,
#     x="distance",
#     palette=sns.color_palette("muted"),
#     binwidth=0.05,
#     stat="probability",
#     common_norm=False,
#     kde=True,
# )
# plt.xlabel("Distance (um)")
# plt.ylim(0, 0.16)
# plt.xlim(0, 3.2)
# # plt.tight_layout()
# # plt.savefig(f"{outdir}/sim_histplot_eps_0.0075_bin_0.05.pdf")
# plt.show()

# %%
# sns.swarmplot(
#     data=long_dist_df,
#     x="cohesin",
#     y="distance",
#     hue="cpc",
#     palette=sns.color_palette("muted"),
#     size=4,
# )
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.ylim(0, 0.16)
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()
# %%

# long_dist_df3 = make_long_dist_df(
#     indir,
#     file="simulated_droplet_distributions/simulated_droplet_distances_e_0.005_noisy_cohesin_chr_lengths.csv",
# )
# sns.histplot(
#     data=long_dist_df3,
#     x="distance",
#     palette=sns.color_palette("muted"),
#     binwidth=0.1,
#     stat="probability",
#     common_norm=False,
#     kde=True,
# )

# # sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()

# %%

# long_dist_df4 = make_long_dist_df(
#     indir,
#     file="simulated_droplet_distributions/simulated_droplet_distances_e_0.008_noisy_cohesin_chr_lengths.csv",
# )
# sns.histplot(
#     data=long_dist_df4,
#     x="distance",
#     palette=sns.color_palette("muted"),
#     binwidth=0.1,
#     stat="probability",
#     common_norm=False,
#     kde=True,
# )

# # sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()


# %%
long_dist_df5 = make_long_dist_df(
    indir,
    file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0067_noisy_cohesin_chr_lengths_HeLa_n_matched.csv",
)
sns.histplot(
    data=long_dist_df5,
    x="distance",
    palette=sns.color_palette("muted"),
    binwidth=0.1,
    stat="probability",
    common_norm=False,
    kde=True,
)

# sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
plt.title("Distances between droplets by CPC radius and Cohesin width")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
plt.tight_layout()
plt.show()

# %%
long_dist_df6 = make_long_dist_df(
    indir,
    file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0089_noisy_cohesin_chr_lengths_MCF10A_n_matched.csv",
)
sns.histplot(
    data=long_dist_df6,
    x="distance",
    palette=sns.color_palette("muted"),
    binwidth=0.1,
    stat="probability",
    common_norm=False,
    kde=True,
)

# sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
plt.title("Distances between droplets by CPC radius and Cohesin width")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
plt.tight_layout()
plt.show()
# %%
# %%
long_dist_df7 = make_long_dist_df(
    indir,
    file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0067_noisy_cohesin_chr_lengths_HeLa_n_matched_50sims.csv",
)
sns.histplot(
    data=long_dist_df7,
    x="distance",
    palette=sns.color_palette("muted"),
    binwidth=0.1,
    stat="probability",
    common_norm=False,
    kde=True,
)

# sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
plt.title("Distances between droplets by CPC radius and Cohesin width")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
plt.tight_layout()
plt.show()

# %%
long_dist_df8 = make_long_dist_df(
    indir,
    file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0089_noisy_cohesin_chr_lengths_MCF10A_n_matched_50sims.csv",
)
sns.histplot(
    data=long_dist_df8,
    x="distance",
    palette=sns.color_palette("muted"),
    binwidth=0.1,
    stat="probability",
    common_norm=False,
    kde=True,
)

# sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
plt.title("Distances between droplets by CPC radius and Cohesin width")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
plt.tight_layout()
plt.show()

# %%
long_dist_df9 = make_long_dist_df(
    indir,
    file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0067_noisy_cohesin_chr_lengths_HeLa_n_matched_20sims.csv",
)
sns.histplot(
    data=long_dist_df9,
    x="distance",
    palette=sns.color_palette("muted"),
    binwidth=0.1,
    stat="probability",
    common_norm=False,
    kde=True,
)

# sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
plt.title("Distances between droplets by CPC radius and Cohesin width")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
plt.tight_layout()
plt.show()

# %%
long_dist_df10 = make_long_dist_df(
    indir,
    file="simulated_droplet_distributions/simulated_droplet_distances_e_0.0089_noisy_cohesin_chr_lengths_MCF10A_n_matched_20sims.csv",
)
sns.histplot(
    data=long_dist_df10,
    x="distance",
    palette=sns.color_palette("muted"),
    binwidth=0.1,
    stat="probability",
    common_norm=False,
    kde=True,
)

# sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
plt.title("Distances between droplets by CPC radius and Cohesin width")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
plt.tight_layout()
plt.show()

# %% compare two simulation types
# outdir = f"{indir}/radii_lineplots_kymographs/domain_0_2_noisy_cohesin_sd_0.11"

binwidth = 0.05
# long_dist_df["Category"] = "eps = 0.01"
# long_dist_df2["Category"] = "eps = 0.0075"
# long_dist_df3["Category"] = "eps = 0.005"
# long_dist_df4["Category"] = "eps = 0.008"
long_dist_df5["Category"] = "eps = 0.0067"
long_dist_df6["Category"] = "eps = 0.0089"
long_dist_df7["Category"] = "eps = 0.0067 - 50 sims"
long_dist_df8["Category"] = "eps = 0.0089 - 50 sims"
long_dist_df9["Category"] = "eps = 0.0067 - 20 sims"
long_dist_df10["Category"] = "eps = 0.0089 - 20 sims"

long_dist_df = pd.concat(
    [
        # long_dist_df, long_dist_df2,  long_dist_df3,long_dist_df4,
        long_dist_df5, long_dist_df6, long_dist_df7, long_dist_df8, long_dist_df9, long_dist_df10], ignore_index=True
)
# sns.histplot(
#     data=long_dist_df,
#     x="distance",
#     hue="Category",
#     binwidth=binwidth,
#     stat="probability",
#     common_norm=False,
#     kde=True,
# )
# %%
sns.kdeplot(
    data=long_dist_df.loc[["eps = 0.0067" in i
                           for i in long_dist_df["Category"]]],
    x="distance",
    hue="Category",
    # stat="probability",
    common_norm=False,
)
# plt.savefig(f"{outdir}/distances_between_droplets_histplot_sims_kdes_v4.png")
plt.show()
sns.kdeplot(
    data=long_dist_df.loc[["eps = 0.0089" in i
                           for i in long_dist_df["Category"]]],
    x="distance",
    hue="Category",
    # stat="probability",
    common_norm=False,
)
# plt.savefig(f"{outdir}/distances_between_droplets_histplot_sims_kdes_v4.png")
plt.show()
# %%
# outdir = f"{indir}/radii_over_time_level_set_plots/domain_0_2_noisy_cohesin_sd_0.25/"

# long_dist_df = make_long_dist_df(
#     indir,
#     file="simulated_droplet_distances/simulated_droplet_distances_e_0.0075_noisy_cohesin_sd_0.25.csv",
# )
# sns.histplot(
#     data=long_dist_df, x="distance", palette=sns.color_palette("muted"), bins=30
# )

# # sns.swarmplot(data= long_dist_df, x = 'cohesin', y = 'distance', hue = 'cpc', palette=sns.color_palette("muted"), size = 4)
# plt.title("Distances between droplets by CPC radius and Cohesin width")
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0)
# plt.tight_layout()
# plt.show()

# %%

# the below code is pulled from distances_between_droplets.py in the CPC_condensate_images folder on Box.


def inter_droplet_distance(indir, image):
    distance_dict = {}
    tmp = pd.read_csv(
        f"{indir}/count_peaks_image{image}_.csv",
        header=0,
        index_col=0,
        converters={"IC_peaks": pd.eval,
                    "left_peaks": pd.eval, "right_peaks": pd.eval},
    )
    for i, r in tmp.iterrows():
        ic = list(r["IC_peaks"])
        left = list(r["left_peaks"])
        right = list(r["right_peaks"])
        [ic.extend(l) for l in (left, right)]
        all_peaks = sorted(ic)

        distances = []
        for j in range(len(all_peaks) - 1):
            d = (all_peaks[j + 1] - all_peaks[j]) * 0.06013
            distances.append(d)
        distance_dict[i] = distances
    return distance_dict


indir2 = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/analysis"
all_images = []
all_images_dict = {}
for image in range(10):
    distance_dict = inter_droplet_distance(indir2, image=image)
    # all_images_dict[image] = distance_dict
    all_ = []
    for k in distance_dict.keys():
        all_.extend(distance_dict[k])
    all_images_dict[f"{image}"] = all_
    all_images.extend(all_)

print(all_images_dict)

# %%

bootstrap_samples_file = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/manual_condensates/bootstrapped/remaining_no_replacement.txt"
bootstrap_samples = []
with open(bootstrap_samples_file, "r") as f:
    for line in f:
        # Strip newline characters and convert the string to a list
        bootstrap_samples.append(ast.literal_eval(line.strip()))

# make distributions
bootstrapped_df = pd.DataFrame(
    columns=["Category", "seed", "time", "cpc", "cohesin", "distance"])
for n, samples in enumerate(bootstrap_samples):
    print(n/len(bootstrap_samples))
    for s in samples:
        try:
            for d in all_images_dict[s]:
                bootstrapped_df = pd.concat(
                    [
                        bootstrapped_df,
                        pd.DataFrame(
                            {
                                "Category": [f"Bootstrap {n}"],
                                "seed": [0],
                                "time": [0],
                                "cpc": [0],
                                "cohesin": [0],
                                "distance": [d],
                            }
                        ),
                    ],
                    ignore_index=True,
                )
        except KeyError:
            pass

# %%
fig, axes = plt.subplots()
sns.kdeplot(
    data=bootstrapped_df,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("viridis", n_colors=100),
    ax=axes
)
sns.kdeplot(
    data=long_dist_df,
    x="distance",
    hue="Category",
    common_norm=False,
    # palette=sns.color_palette("Spectral", n_colors=100),
    ax=axes,
    linestyle="--",

)
plt.title(
    "Droplet Distance Distributions: HeLa Images (100 bootstraps) vs Simulations")
plt.xlabel("Distance (um)")
plt.ylabel("Density")
# plt.savefig(
# f"{outdir}/distances_between_droplets_kdeplot_HeLa_images_vs_sim_bootstrapped_v1.png")
plt.show()

# %%
#########################################################
# MCF10A bootstrapping
#########################################################


indir_MCF10A = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans/"
all_images_MCF10A = []
all_images_dict_MCF10A = {}
for image in range(1, 50):
    try:
        distance_dict = inter_droplet_distance(indir_MCF10A, image=image)
        # all_images_dict[image] = distance_dict
        all_ = []
        for k in distance_dict.keys():
            all_.extend(distance_dict[k])
        all_images_dict_MCF10A[f"{image}"] = all_
        all_images_MCF10A.extend(all_)
    except FileNotFoundError:
        print(f"File not found for image {image}.")

print(all_images_dict_MCF10A)

# %%
bootstrap_samples_file = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/bootstrapped/remaining_no_replacement.txt"
bootstrap_samples = []
with open(bootstrap_samples_file, "r") as f:
    for line in f:
        # Strip newline characters and convert the string to a list
        bootstrap_samples.append(ast.literal_eval(line.strip()))

# make distributions
bootstrapped_df_MCF10A = pd.DataFrame(
    columns=["Category", "seed", "time", "cpc", "cohesin", "distance"])
for n, samples in enumerate(bootstrap_samples):
    print(n/len(bootstrap_samples))
    for s in samples:
        # try:
        for d in all_images_dict_MCF10A[f"{s}"]:
            bootstrapped_df_MCF10A = pd.concat(
                [
                    bootstrapped_df_MCF10A,
                    pd.DataFrame(
                        {
                            "Category": [f"Bootstrap {n}"],
                            "seed": [0],
                            "time": [0],
                            "cpc": [0],
                            "cohesin": [0],
                            "distance": [d],
                        }
                    ),
                ],
                ignore_index=True,
            )
        # except KeyError:
            # pass

# %%
fig, axes = plt.subplots()
sns.kdeplot(
    data=bootstrapped_df_MCF10A,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("viridis", n_colors=101),
    ax=axes
)
sns.kdeplot(
    data=long_dist_df.loc[(long_dist_df["Category"] == "eps = 0.0089") | (
        long_dist_df["Category"] == "eps = 0.01") |
        (long_dist_df["Category"] == "eps = 0.0067")],
    x="distance",
    hue="Category",
    common_norm=False,
    # palette=sns.color_palette("Spectral", n_colors=100),
    ax=axes,
    linestyle="--",

)

plt.title(
    "Droplet Distance Distributions: MCF10A Images (100 bootstraps) vs Simulations")
plt.xlabel("Distance (um)")
plt.ylabel("Density")
# plt.savefig(
# f"{outdir}/distances_between_droplets_kdeplot_MCF10A_images_vs_sim_bootstrapped_v2.png")
plt.show()

# %%

fig, axes = plt.subplots(1, 1)
sns.kdeplot(
    data=bootstrapped_df_MCF10A,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("viridis", n_colors=101),
    ax=axes
)
sns.kdeplot(
    data=bootstrapped_df,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("Reds", n_colors=101),
    ax=axes
)
# %% # use without bootstrapping
# long_dist_df["Category"] = "Simulation"
# for d in all_images:
#     long_dist_df = pd.concat(
#         [
#             long_dist_df,
#             pd.DataFrame(
#                 {
#                     "Category": ["Experiment_HeLa"],
#                     "seed": [0],
#                     "time": [0],
#                     "cpc": [0],
#                     "cohesin": [0],
#                     "distance": [d],
#                 }
#             ),
#         ],
#         ignore_index=True,
#     )

# %% # use without bootstrapping
# indir3 = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/MCF10A"
# all_images = []
# for image in [10]:
#     distance_dict = inter_droplet_distance(indir3, image=image)

#     all_ = []
#     for k in distance_dict.keys():
#         all_.extend(distance_dict[k])
#     all_images.extend(all_)

# print(all_images)

# # long_dist_df["Category"] = "Simulation"
# for d in all_images:
#     long_dist_df = pd.concat(
#         [
#             long_dist_df,
#             pd.DataFrame(
#                 {
#                     "Category": ["Experiment_MCF10A"],
#                     "seed": [0],
#                     "time": [0],
#                     "cpc": [0],
#                     "cohesin": [0],
#                     "distance": [d],
#                 }
#             ),
#         ],
#         ignore_index=True,
#     )

# %%

# PLOTTING EXPERIMENT VS SIMULATION FIGURE 6
# KDE-based average distributions for HeLa and MCF10A


def compute_kde(bootstrapped_df):
    # df should be your DataFrame with "Category" and "distance"
    categories = bootstrapped_df["Category"].unique()

    # Common evaluation grid
    all_distances = bootstrapped_df["distance"].values
    x_eval = np.linspace(np.min(all_distances), np.max(all_distances), 500)

    # Compute KDE for each bootstrap category
    kde_vals = []

    for cat in categories:
        sample = bootstrapped_df[bootstrapped_df["Category"]
                                 == cat]["distance"].values
        kde = gaussian_kde(sample)
        kde_vals.append(kde(x_eval))

    kde_vals = np.array(kde_vals)  # shape: (n_bootstraps, 500)

    # Average the KDEs
    avg_kde = np.mean(kde_vals, axis=0)
    return x_eval, avg_kde


class HandlerVerticalGradient(HandlerBase):
    def __init__(self, cmap, n_segments=100, alpha=1.0, **kwargs):
        self.cmap = cmap
        self.n_segments = n_segments
        self.alpha = alpha
        super().__init__(**kwargs)

    def create_artists(self, legend, orig_handle, x0, y0, width, height, fontsize, trans):
        segments = []
        for i in range(self.n_segments):
            y = y0 + height * i / self.n_segments
            rgba = self.cmap(i / self.n_segments)
            rgba_with_alpha = rgba[:3] + (self.alpha,)
            rect = Rectangle(
                (x0, y),
                width,
                height / self.n_segments,
                facecolor=rgba_with_alpha,
                transform=trans,
                linewidth=0
            )
            segments.append(rect)
        return segments


# %%
# sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == 'eps = 0.0089'], x="distance",
#              stat='density', binwidth=0.05, common_norm=True, alpha=0.2,
#              label="Simulations (n = 10)", multiple='stack', hue="cpc")

# %% max and min number of chromosomes across bootstraps

MCF10A_peaks = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans/all_count_peaks.csv"
bootstrap_samples_MCF10A = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/bootstrapped/remaining_no_replacement.txt"


def count_chromosomes_per_bootstrap(bootstrap_samples_file, peaks_file):
    peaks = pd.read_csv(peaks_file,
                        header=0,
                        index_col=0,
                        )
    bootstrap_samples = []
    with open(bootstrap_samples_file, "r") as f:
        for line in f:
            # Strip newline characters and convert the string to a list
            bootstrap_samples.append(ast.literal_eval(line.strip()))
    num_images_per_bootstrap = len(bootstrap_samples[0])
    num_chromosomes_per_bootstrap = []
    for sample in bootstrap_samples:
        tmp = peaks.loc[peaks["image_num"].isin(sample)]
        if len(tmp.index) == 0:
            sample = [int(i) for i in sample]
            tmp = peaks.loc[peaks["image_num"].isin(sample)]
        num_chromosomes_per_bootstrap.append(len(tmp.index))
    return num_chromosomes_per_bootstrap, num_images_per_bootstrap


MCF10A_chr_n, MCF10A_image_n = (count_chromosomes_per_bootstrap(
    bootstrap_samples_MCF10A, MCF10A_peaks))

HeLa_peaks = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/analysis/all_count_peaks.csv"
bootstrap_samples_HeLa = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/manual_condensates/bootstrapped/remaining_no_replacement.txt"

HeLa_chr_n, HeLa_image_n = (count_chromosomes_per_bootstrap(
    bootstrap_samples_HeLa, HeLa_peaks))


# %%
outdir = (
    f"{indir}/distance_between_droplets/"
)

x_eval, avg_kde = compute_kde(bootstrapped_df_MCF10A)
n_chr_exp = 217
category = 'eps = 0.0089 - 50 sims'
n_chr_sim = len(
    long_dist_df.loc[long_dist_df["Category"] == category]['seed'].unique())
if n_chr_sim == 10:
    n_timepoints = int(np.floor(n_chr_exp / n_chr_sim))
else:
    n_timepoints = int(np.ceil(n_chr_exp / n_chr_sim))
sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == category], x="distance",
             stat='density', binwidth=0.05, common_norm=False,  color="gray", alpha=0.2, kde=True,
             label=f"Simulations (n = {n_chr_sim} chr, {n_timepoints} timepoints per chr)")

# sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == 'eps = 0.0089'], x="distance",
#  stat='density', binwidth=0.05, common_norm=True, alpha=0.5, multiple='stack', hue="cpc",
#  palette="tab10")

sns.kdeplot(
    data=bootstrapped_df_MCF10A,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("viridis", n_colors=101),
)

sns.lineplot(x=x_eval, y=avg_kde, color="navy",
             label=f"Average KDE for MCF10A Images")
plt.axvline(x=np.mean(bootstrapped_df_MCF10A['distance']), color="blue",
            linestyle="--", label=f"Ave Distance across MCF10A Bootstraps: {np.round(np.mean(bootstrapped_df_MCF10A['distance']), 4)}")
plt.axvline(x=np.mean(long_dist_df.loc[long_dist_df["Category"] == category]['distance']),
            color="black", linestyle="--", label=f"Ave Distance for Simulations: {np.round(np.mean(long_dist_df.loc[long_dist_df['Category'] == category]['distance']), 4)}")

plt.ylim(0, 2.8)
plt.xlim(0, 3)

plt.xlabel("Distance")
plt.ylabel("Density")
plt.title(
    f"MCF10A Images (n = {n_chr_exp} chromosomes) vs. Simulations (n = {int(n_chr_sim*n_timepoints)} timepoints),\neps = 0.0089")
# Use this to create a fake handle
gradient_patch = Rectangle((0, 0), 1, 1)  # dummy rectangle
handles, labels = plt.gca().get_legend_handles_labels()

# Add to the legend with custom handler
plt.legend(
    handles=[*handles, gradient_patch],
    labels=[
        *labels, f"Bootstrapped Distributions (n = {MCF10A_image_n} images, {np.round(np.mean(MCF10A_chr_n),1)} ± {np.round(np.std(MCF10A_chr_n),1)}chr)"],
    handler_map={gradient_patch: HandlerVerticalGradient(
        cm.get_cmap("viridis"), alpha=0.5)},
    loc='upper right')

plt.tight_layout()
plt.show()
# plt.savefig(
# f"{outdir}/MCF10A_images_bootstrapped_vs_0.0089_sim_n_chr_sim_{n_chr_sim}_with_ave.pdf")
# plt.close()

# %%
x_eval, avg_kde = compute_kde(bootstrapped_df)
n_chr_exp = 231
category = 'eps = 0.0067 - 50 sims'
n_chr_sim = len(
    long_dist_df.loc[long_dist_df["Category"] == category]['seed'].unique())
if n_chr_sim == 10:
    n_timepoints = int(np.floor(n_chr_exp / n_chr_sim))
else:
    n_timepoints = int(np.ceil(n_chr_exp / n_chr_sim))
sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == category], x="distance",
             stat='density', binwidth=0.05, common_norm=False,  color="gray", alpha=0.2, kde=True,
             label=f"Simulations (n = {n_chr_sim} chr, {n_timepoints} timepoints per chr)")

# sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == 'eps = 0.0067'], x="distance",
#              stat='density', binwidth=0.05, common_norm=True, alpha=0.5, multiple='stack', hue="cpc",
#              palette="tab10")

sns.kdeplot(
    data=bootstrapped_df,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("Reds", n_colors=101),
)

sns.lineplot(x=x_eval, y=avg_kde, color="DarkRed",
             label="Average KDE for HeLa Images")
plt.axvline(x=np.mean(bootstrapped_df['distance']), color="red",
            linestyle="--", label=f"Ave Distance across HeLa Bootstraps: {np.round(np.mean(bootstrapped_df['distance']), 4)}")
plt.axvline(x=np.mean(long_dist_df.loc[long_dist_df["Category"] == category]['distance']),
            color="black", linestyle="--", label=f"Ave Distance for Simulations: {np.round(np.mean(long_dist_df.loc[long_dist_df['Category'] == category]['distance']), 4)}")
plt.ylim(0, 2.8)
plt.xlim(0, 3)

plt.xlabel("Distance")
plt.ylabel("Density")
plt.title(
    f"HeLa Images (n = {n_chr_exp} chromosomes) vs. Simulations (n = {int(n_chr_sim*n_timepoints)} timepoints),\neps = 0.0067")

# Use this to create a fake handle
gradient_patch = Rectangle((0, 0), 1, 1)  # dummy rectangle
handles, labels = plt.gca().get_legend_handles_labels()

# Add to the legend with custom handler
plt.legend(
    handles=[*handles, gradient_patch],
    labels=[
        *labels, f"Bootstrapped Distributions (n = {HeLa_image_n} images, {np.round(np.mean(HeLa_chr_n),1)} ± {np.round(np.std(HeLa_chr_n),1)}chr)"],
    handler_map={gradient_patch: HandlerVerticalGradient(
        cm.get_cmap("Reds"), alpha=0.5)},
    loc='upper right'
)

plt.tight_layout()
plt.show()
# plt.savefig(
# f"{outdir}/HeLa_images_bootstrapped_vs_0.0067_sim_n_chr_sim_{n_chr_sim}_with_ave.pdf")

plt.close()
# %%

# MCF10A bootstraps
x_eval, avg_kde = compute_kde(bootstrapped_df_MCF10A)

sns.kdeplot(
    data=bootstrapped_df_MCF10A,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("viridis", n_colors=101),
)

sns.lineplot(x=x_eval, y=avg_kde, color="navy",
             label=f"Average KDE for MCF10A Images")


# HeLa bootstraps
x_eval, avg_kde = compute_kde(bootstrapped_df)
sns.kdeplot(
    data=bootstrapped_df,
    x="distance",
    hue="Category",
    common_norm=False,
    alpha=0.1,
    legend=False,
    palette=sns.color_palette("Reds", n_colors=101),
)

sns.lineplot(x=x_eval, y=avg_kde, color="DarkRed",
             label="Average KDE for HeLa Images")
plt.axvline(x=np.mean(bootstrapped_df['distance']), color="DarkRed",
            linestyle="--", label=f"Ave Distance across HeLa Bootstraps: {np.round(np.mean(bootstrapped_df['distance']), 4)}")
plt.axvline(x=np.mean(bootstrapped_df_MCF10A['distance']), color="navy",
            linestyle="--", label=f"Ave Distance across MCF10A Bootstraps: {np.round(np.mean(bootstrapped_df_MCF10A['distance']), 4)}")
plt.ylim(0, 2.8)
plt.xlim(0, 3)
n_chr_exp_HeLa = 231
n_chr_exp_MCF10A = 217
plt.xlabel("Distance")
plt.ylabel("Density")
plt.title(
    f"HeLa Images (n = {n_chr_exp_HeLa} chromosomes) vs. MCF10A Images (n = {n_chr_exp_MCF10A}")

# Use this to create a fake handle
gradient_patch = Rectangle((0, 0), 1, 1)  # dummy rectangle
gradient_patch2 = Rectangle((0, 0), 1, 1)  # dummy rectangle

handles, labels = plt.gca().get_legend_handles_labels()

# Add to the legend with custom handler
plt.legend(
    handles=[*handles, gradient_patch, gradient_patch2],
    labels=[
        *labels, f"Bootstrapped Distributions (n = {HeLa_image_n} images, {np.round(np.mean(HeLa_chr_n),1)} ± {np.round(np.std(HeLa_chr_n),1)}chr)",
        f"Bootstrapped Distributions (n = {MCF10A_image_n} images, {np.round(np.mean(MCF10A_chr_n),1)} ± {np.round(np.std(MCF10A_chr_n),1)}chr)"],
    handler_map={gradient_patch: HandlerVerticalGradient(
        cm.get_cmap("Reds"), alpha=0.5), gradient_patch2: HandlerVerticalGradient(
        cm.get_cmap("viridis"), alpha=0.5)},
    loc='upper right'
)
plt.show()


# %%
category89 = 'eps = 0.0089 - 50 sims'
n_chr_sim89 = len(
    long_dist_df.loc[long_dist_df["Category"] == category89]['seed'].unique())
if n_chr_sim89 == 10:
    n_timepoints89 = int(np.floor(n_chr_exp / n_chr_sim89))
else:
    n_timepoints89 = int(np.ceil(n_chr_exp / n_chr_sim89))
sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == category89], x="distance",
             stat='density', binwidth=0.05, common_norm=False,  color="navy", alpha=0.2, kde=True,
             label=f"Simulations (n = {n_chr_sim89} chr, {n_timepoints89} timepoints per chr)")
plt.axvline(x=np.mean(long_dist_df.loc[long_dist_df["Category"] == category89]['distance']),
            color="navy", linestyle="--", label=f"Ave Distance for e=0.0089 Simulations: {np.round(np.mean(long_dist_df.loc[long_dist_df['Category'] == category89]['distance']), 4)}")

category67 = 'eps = 0.0067 - 50 sims'
n_chr_sim67 = len(
    long_dist_df.loc[long_dist_df["Category"] == category67]['seed'].unique())
if n_chr_sim67 == 10:
    n_timepoints67 = int(np.floor(n_chr_exp / n_chr_sim67))
else:
    n_timepoints67 = int(np.ceil(n_chr_exp / n_chr_sim67))
sns.histplot(data=long_dist_df.loc[long_dist_df["Category"] == category67], x="distance",
             stat='density', binwidth=0.05, common_norm=False,  color="DarkRed", alpha=0.2, kde=True,
             label=f"Simulations (n = {n_chr_sim67} chr, {n_timepoints67} timepoints per chr)")

plt.axvline(x=np.mean(long_dist_df.loc[long_dist_df["Category"] == category67]['distance']),
            color="DarkRed", linestyle="--", label=f"Ave Distance for e=0.0067 Simulations: {np.round(np.mean(long_dist_df.loc[long_dist_df['Category'] == category67]['distance']), 4)}")
plt.legend()
plt.ylim(0, 2.8)
plt.xlim(0, 3)
plt.title(
    f"Simulations eps = 0.0067 (n = {int(n_chr_sim67*n_timepoints67)} timepoints) vs Simulations e = 0.0089 (n = {int(n_chr_sim89*n_timepoints89)} timepoints)")
plt.tight_layout()
plt.show()

# %% CDF plots sims
plt.rcParams["font.family"] = "Arial"
plt.rcParams['pdf.use14corefonts'] = True
plt.figure(figsize=(4, 3))
ax = sns.kdeplot(data=long_dist_df.loc[long_dist_df["Category"] == category89], x="distance",
                 color="DarkRed",
                 # binwidth=0.05, common_norm=False,  alpha=0.2, kde=True,stat='density',
                 label=f"Simulations e = 0.0089 (n = {n_chr_sim89} chr, {n_timepoints89} timepoints per chr)", cumulative=True)
sns.kdeplot(data=long_dist_df.loc[long_dist_df["Category"] == category67], x="distance",
            color="DarkRed", linestyle="--",
            # binwidth=0.05, common_norm=False,   alpha=0.2, kde=True,stat='density',
            label=f"Simulations e = 0.0067 (n = {n_chr_sim67} chr, {n_timepoints67} timepoints per chr)", cumulative=True)
ax.spines[['right', 'top']].set_visible(False)

plt.legend()
plt.xlim(0, 3.5)
plt.ylim(0, 1)
plt.title("Simulations")
plt.show()
# plt.savefig(f"{outdir}/simulation_CDFs.pdf")

kstest(long_dist_df.loc[long_dist_df["Category"] == category89]['distance'].values,
       long_dist_df.loc[long_dist_df["Category"] == category67]['distance'].values)

# %%

# %% CDF plots experiments
plt.figure(figsize=(4, 3))

x_eval, avg_kde = compute_kde(bootstrapped_df)
cdf = cumtrapz(avg_kde, x_eval, initial=0)
# Normalize to ensure CDF ends at 1
cdf /= cdf[-1]
ax = sns.lineplot(x=x_eval, y=cdf, color="grey", linestyle="--",
                  label="Average KDE for HeLa Images")
x_eval, avg_kde = compute_kde(bootstrapped_df_MCF10A)
cdf = cumtrapz(avg_kde, x_eval, initial=0)
# Normalize to ensure CDF ends at 1
cdf /= cdf[-1]
sns.lineplot(x=x_eval, y=cdf, color="grey",
             label="Average KDE for MCF10A Images")
plt.xlim(0, 3.5)
plt.ylim(0, 1)
ax.spines[['right', 'top']].set_visible(False)

plt.legend()
# plt.savefig(f"{outdir}/HeLa_vs_MCF10A_bootstrapped_CDFs.pdf")
plt.show()

# %%
# ks test for each bootstrap
stats = []
ps = []
n_samples_hela = []
n_samples_mcf10a = []
for b in bootstrapped_df['Category'].unique():
    print(b)
    hela_tmp = bootstrapped_df.loc[bootstrapped_df['Category']
                                   == b]['distance'].values
    # print(len(hela_tmp))
    mcf10a_tmp = bootstrapped_df_MCF10A.loc[bootstrapped_df_MCF10A['Category']
                                            == b]['distance'].values
    s, p = kstest(hela_tmp, mcf10a_tmp)
    stats.append(s)
    ps.append(p)
    n_samples_hela.append(len(hela_tmp))
    n_samples_mcf10a.append(len(mcf10a_tmp))

print("Mean(ks stat)+/- SEM:", np.mean(stats), ss.sem(stats))
print("Mean(ks P)+/- SEM:", np.mean(ps), ss.sem(ps))
print("Mean number of samples per bootstrap", np.mean(
    n_samples_hela), np.mean(n_samples_mcf10a))

# average values

# kstest(bootstrapped_df_MCF10A['distance'].values,
#        bootstrapped_df['distance'].values)

# %% CDF plots: median with CI / IQR plotted


def get_percentile_bs(bootstrapped_df, perc=50):
    df = pd.DataFrame(
        {
            "Category": bootstrapped_df['Category'].unique(),
            "ks_statistic": stats,
            "p_value": ps,
            "n_samples_hela": n_samples_hela,
            "n_samples_mcf10a": n_samples_mcf10a,
        }
    )

    df.sort_values(by="p_value", inplace=True)
    ind = int(perc / 100 * len(df)) - 1
    print(df.iloc[ind])
    return df.iloc[ind]


def compute_kde_CI(bootstrapped_df, percentiles=[2.5, 97.5]):
    # df should be your DataFrame with "Category" and "distance"
    categories = bootstrapped_df["Category"].unique()

    # Common evaluation grid
    all_distances = bootstrapped_df["distance"].values
    x_eval = np.linspace(np.min(all_distances), np.max(all_distances), 500)

    # Compute KDE for each bootstrap category
    kde_vals = []

    for cat in categories:
        sample = bootstrapped_df[bootstrapped_df["Category"]
                                 == cat]["distance"].values
        kde = gaussian_kde(sample)
        kde_vals.append(kde(x_eval))

    kde_vals = np.array(kde_vals)  # shape: (n_bootstraps, 500)

    # percentiles of the KDEs
    lb_kde = np.percentile(kde_vals, percentiles[0], axis=0)
    ub_kde = np.percentile(kde_vals, percentiles[1], axis=0)
    return x_eval, ub_kde, lb_kde


median_bs = get_percentile_bs(bootstrapped_df)
median_bs_cat = median_bs['Category']

plt.figure(figsize=(4, 3))
#################
# HELA
ax = sns.kdeplot(data=bootstrapped_df.loc[bootstrapped_df['Category'] == median_bs_cat], x="distance",
                 color="grey", linestyle="--",
                 # binwidth=0.05, common_norm=False,   alpha=0.2, kde=True,stat='density',
                 label=f"HeLa", cumulative=True)

x_eval, ub_kde, lb_kde = compute_kde_CI(bootstrapped_df)
ub_cdf = cumtrapz(ub_kde, x_eval, initial=0)
# Normalize to ensure CDF ends at 1
ub_cdf /= ub_cdf[-1]
# ax = sns.lineplot(x=x_eval, y=ub_cdf, color="lightgrey", linestyle="--",
#   label="UB KDE for HeLa Images")
lb_cdf = cumtrapz(lb_kde, x_eval, initial=0)
# Normalize to ensure CDF ends at 1
lb_cdf /= lb_cdf[-1]
# ax = sns.lineplot(x=x_eval, y=lb_cdf, color="lightgrey", linestyle="--",
#   label="LB KDE for HeLa Images")

plt.fill_between(x_eval, ub_cdf, lb_cdf, color="lightgrey", alpha=0.5,
                 label="KDE CI for HeLa Images")


#################
# MCF10A
sns.kdeplot(data=bootstrapped_df_MCF10A.loc[bootstrapped_df_MCF10A['Category'] == median_bs_cat], x="distance",
            color="blue",
            # binwidth=0.05, common_norm=False,   alpha=0.2, kde=True,stat='density',
            label=f"MCF10A", cumulative=True)
x_eval, ub_kde, lb_kde = compute_kde_CI(bootstrapped_df_MCF10A)
ub_cdf = cumtrapz(ub_kde, x_eval, initial=0)
# Normalize to ensure CDF ends at 1
ub_cdf /= ub_cdf[-1]
# ax = sns.lineplot(x=x_eval, y=ub_cdf, color="lightgrey", linestyle="--",
#   label="UB KDE for HeLa Images")
lb_cdf = cumtrapz(lb_kde, x_eval, initial=0)
# Normalize to ensure CDF ends at 1
lb_cdf /= lb_cdf[-1]
# ax = sns.lineplot(x=x_eval, y=lb_cdf, color="lightgrey", linestyle="--",
#                   label="LB KDE for HeLa Images")

plt.fill_between(x_eval, ub_cdf, lb_cdf, color="lightblue", alpha=0.5,
                 label="KDE CI for HeLa Images")

##################
# Annotate plot
plt.annotate(xy=(0, 0), xytext=(2.5, .3),
             text=f"Median Bootstrap: {median_bs_cat}\n95% CI for each cell line\nKS Statistic: {np.round(median_bs['ks_statistic'], 4)}\np-value: {np.round(median_bs['p_value'], 4)}\nSamples HeLa: {int(median_bs['n_samples_hela'])}\nSamples MCF10A: {int(median_bs['n_samples_mcf10a'])}",
             ha='center', va='center', fontsize=10, bbox=dict(boxstyle="round", fc="w"))
ax.spines[['right', 'top']].set_visible(False)
plt.xlim(0, 3.5)
plt.ylim(0, 1)
# plt.show()
plt.savefig(f"{outdir}/HeLa_vs_MCF10A_bootstrapped_CDFs_medians_with_CI.pdf")

# %% check what CDF plots of each bootstrap look like
for cat in bootstrapped_df['Category'].unique():
    sns.kdeplot(
        data=bootstrapped_df.loc[bootstrapped_df['Category'] == cat], x="distance", cumulative=True)
# plt.show()

# %%
highest_bs = get_percentile_bs(bootstrapped_df, perc=100)
highest_ind = highest_bs['Category']

sns.kdeplot(data=bootstrapped_df.loc[bootstrapped_df['Category'] == highest_ind], x="distance",
            color="grey", linestyle="--",
            # binwidth=0.05, common_norm=False,   alpha=0.2, kde=True,stat='density',
            label=f"HeLa", cumulative=True)

sns.kdeplot(data=bootstrapped_df_MCF10A.loc[bootstrapped_df_MCF10A['Category'] == highest_ind], x="distance",
            color="blue",
            # binwidth=0.05, common_norm=False,   alpha=0.2, kde=True,stat='density',
            label=f"MCF10A", cumulative=True)
plt.title(f"Highest P Value Bootstrap = {round(highest_bs['p_value'], 3)}")

# %%
# %% HELA vs SIMS 0.0067 histogram with CI


def exp_hist_vs_sim_kde_CI(bootstrapped_df, long_dist_df, category, n_chr_sim, n_timepoints, title=None, bin_num=40, save=False, outdir="", bin_centers=[], xmax=3.5, ymax=3, bins=[]):
    # Assume df has columns: "Bootstrap" and "Value"
    boot_ids = bootstrapped_df["Category"].unique()
    all_values = bootstrapped_df["distance"].values
    if len(bin_centers) != 0:
        pass
    elif bin_num != None:
        bins = np.histogram_bin_edges(all_values, bins=bin_num)
        bin_centers = (bins[:-1] + bins[1:]) / 2
    else:
        print("Must set either bin_num or bin_centers")

    # Compute histogram for each bootstrap
    histograms = []
    # plt.figure(figsize=(10, 6))

    for b in boot_ids:
        values = bootstrapped_df[bootstrapped_df["Category"]
                                 == b]["distance"].values
        counts, _ = np.histogram(values, bins=bins, density=True)
        histograms.append(counts)
        # plt.plot(bin_centers, counts, color="gray", alpha=0.1)
    # plt.show()

    hist_array = np.array(histograms)  # shape: (n_bootstraps, n_bins)

    # Compute mean and standard deviation across bootstraps
    mean_density = hist_array.mean(axis=0)
    median_density = np.median(hist_array, axis=0)
    lower_ci = np.percentile(hist_array, 2.5, axis=0)
    upper_ci = np.percentile(hist_array, 97.5, axis=0)

    ci = np.array([lower_ci, upper_ci])
    # make sure to turn ci into error bars (i.e. distance from mean to lower and upper ci)
    y_err = np.abs(ci - median_density)
    plt.figure(figsize=(6, 4))

    sns.kdeplot(data=long_dist_df.loc[long_dist_df["Category"] == category], x="distance",
                color="navy",
                label=f"Simulations (n = {n_chr_sim} chr, {n_timepoints} timepoints per chr)")
    # Plot mean histogram with error bars
    plt.bar(
        bin_centers,
        median_density,
        width=np.diff(bins),
        align='center',
        alpha=0.4,
        color='gray',
        edgecolor='black',
        label="Experimental Median Density (Bootstraps)",
    )
    plt.errorbar(
        bin_centers,
        median_density,
        yerr=y_err,
        fmt='none',
        ecolor='black',
        capsize=2,
        label="Bootstrap CI"
    )
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    plt.xlabel("Distance")
    plt.ylabel("Density")
    if title == None:
        plt.title(
            f"Simulations vs. Bootstrapped Experiments with CI, bins = {bin_num}")
    else:
        plt.title(title)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(f"{outdir}/{title}.pdf")
        plt.close()
    else:
        plt.show()
    return bins, bin_centers


def exp_hist_vs_sim_kde(bootstrapped_df, long_dist_df, category, n_chr_sim, n_timepoints, title=None, bin_num=40):
    # Assume df has columns: "Bootstrap" and "Value"
    boot_ids = bootstrapped_df["Category"].unique()
    all_values = bootstrapped_df["distance"].values
    bins = np.histogram_bin_edges(all_values, bins=bin_num)
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Compute histogram for each bootstrap
    histograms = []

    for b in boot_ids:
        values = bootstrapped_df[bootstrapped_df["Category"]
                                 == b]["distance"].values
        counts, _ = np.histogram(values, bins=bins, density=True)
        histograms.append(counts)

    hist_array = np.array(histograms)  # shape: (n_bootstraps, n_bins)

    # Compute mean and standard deviation across bootstraps
    mean_density = hist_array.mean(axis=0)
    std_density = hist_array.std(axis=0)

    plt.figure(figsize=(8, 5))

    sns.kdeplot(data=long_dist_df.loc[long_dist_df["Category"] == category], x="distance",
                color="navy",
                label=f"Simulations (n = {n_chr_sim} chr, {n_timepoints} timepoints per chr)")
    # Plot mean histogram with error bars
    plt.bar(
        bin_centers,
        mean_density,
        width=np.diff(bins),
        align='center',
        alpha=0.4,
        color='gray',
        edgecolor='black',
        label="Experimental Mean Density (Bootstraps)",
    )
    plt.errorbar(
        bin_centers,
        mean_density,
        yerr=std_density,
        fmt='none',
        ecolor='black',
        capsize=2,
        label="Bootstrap Std Dev"
    )

    plt.xlabel("Distance")
    plt.ylabel("Density")
    if title == None:
        plt.title(
            f"Simulations vs. Bootstrapped Experiments with Error Bars, bins = {bin_num}")
    else:
        plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# exp_hist_vs_sim_kde_CI(bootstrapped_df, long_dist_df, category67,
#                        n_chr_sim67, n_timepoints67, title="Simulations (0.0067) vs. HeLa Bootstraps, 40 bins", outdir=outdir, save=True)
# exp_hist_vs_sim_kde_CI(bootstrapped_df_MCF10A, long_dist_df,
#                        category89, n_chr_sim89, n_timepoints89, title="Simulations (0.0089) vs. MCF10A Bootstraps, 40 bins", outdir=outdir, save=True)
# exp_hist_vs_sim_kde_CI(bootstrapped_df, long_dist_df, category67,
#                        n_chr_sim67, n_timepoints67, title="Simulations (0.0067) vs. HeLa Bootstraps, 20 bins", bin_num=20, outdir=outdir, save=True)
# exp_hist_vs_sim_kde_CI(bootstrapped_df_MCF10A, long_dist_df,
#                        category89, n_chr_sim89, n_timepoints89, title="Simulations (0.0089) vs. MCF10A Bootstraps, 20 bins", outdir=outdir, bin_num=20, save=True)
# exp_hist_vs_sim_kde_CI(bootstrapped_df, long_dist_df, category67,
#                        n_chr_sim67, n_timepoints67, title="Simulations (0.0067) vs. HeLa Bootstraps, 30 bins", bin_num=30, outdir=outdir, save=True)
# exp_hist_vs_sim_kde_CI(bootstrapped_df_MCF10A, long_dist_df,
#                        category89, n_chr_sim89, n_timepoints89, title="Simulations (0.0089) vs. MCF10A Bootstraps, 30 bins", outdir=outdir, bin_num=30, save=True)
# share bins
bins_MCF10A, bin_centers_MCF10A = exp_hist_vs_sim_kde_CI(bootstrapped_df_MCF10A, long_dist_df,
                                                         category89, n_chr_sim89, n_timepoints89, title="Simulations (0.0089) vs. MCF10A Bootstraps, 55 bins,median", outdir=outdir, bin_num=55, save=True)
exp_hist_vs_sim_kde_CI(bootstrapped_df, long_dist_df, category67,
                       n_chr_sim67, n_timepoints67, title="Simulations (0.0067) vs. HeLa Bootstraps, 55 MCF10A bins,median", bin_centers=bin_centers_MCF10A, bins=bins_MCF10A, outdir=outdir, save=True)


# %% Choosing bin width for bootstrap histogram based on average experimental KDE
def choose_bins_exp_hist_CI(bootstrapped_df, bin_nums=[40]):
    num_col = 4
    num_row = int(np.ceil(len(bin_nums) / num_col))
    fig, axes = plt.subplots(num_row, num_col, figsize=(20, 5 * num_row))
    for i, bin_num in enumerate(bin_nums):
        # Assume df has columns: "Bootstrap" and "Value"
        boot_ids = bootstrapped_df["Category"].unique()
        all_values = bootstrapped_df["distance"].values
        bins = np.histogram_bin_edges(all_values, bins=bin_num)
        bin_centers = (bins[:-1] + bins[1:]) / 2

        # Compute histogram for each bootstrap
        histograms = []
        # plt.figure(figsize=(10, 6))

        for b in boot_ids:
            values = bootstrapped_df[bootstrapped_df["Category"]
                                     == b]["distance"].values
            counts, _ = np.histogram(values, bins=bins, density=True)
            histograms.append(counts)

        hist_array = np.array(histograms)  # shape: (n_bootstraps, n_bins)

        # Compute mean and standard deviation across bootstraps
        mean_density = hist_array.mean(axis=0)
        lower_ci = np.percentile(hist_array, 2.5, axis=0)
        upper_ci = np.percentile(hist_array, 97.5, axis=0)

        ci = np.array([lower_ci, upper_ci])
        # make sure to turn ci into error bars (i.e. distance from mean to lower and upper ci)
        y_err = np.abs(ci - mean_density)

        x_eval, avg_kde = compute_kde(bootstrapped_df)
        sns.lineplot(x=x_eval, y=avg_kde, color="navy",
                     label=f"Average KDE for Images", ax=axes[i//num_col, i % num_col])
        # Plot mean histogram with error bars
        axes[i//num_col, i % num_col].bar(
            bin_centers,
            mean_density,
            width=np.diff(bins),
            align='center',
            alpha=0.4,
            color='gray',
            edgecolor='black',
            label="Experimental Mean Density (Bootstraps)",
        )
        axes[i//num_col, i % num_col].errorbar(
            bin_centers,
            mean_density,
            yerr=y_err,
            fmt='none',
            ecolor='black',
            capsize=2,
            label="Bootstrap CI",
        )

        # axes[i//num_col, i % num_col].xlabel("Distance")
        # axes[i//num_col, i % num_col].ylabel("Density")
        axes[i//num_col, i % num_col].set_title(f"bins = {bin_num}")
        axes[i//num_col, i % num_col].legend()
    plt.tight_layout()
    plt.show()


choose_bins_exp_hist_CI(bootstrapped_df_MCF10A, bin_nums=[
                        20, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80])

# %%
sns.histplot(data=bootstrapped_df, x="distance", hue="Category", element='poly', bins=30, fill=False,
             alpha=0.1,
             legend=False)

# %%
########################
# Earth movers distance
########################
# Including averaged bootstrapped distribution for MCF10A and HeLa


long_dist_df_with_cells = pd.concat(
    [long_dist_df, bootstrapped_df_MCF10A.loc[bootstrapped_df_MCF10A['Category']
                                              == "Bootstrap 0"], bootstrapped_df.loc[bootstrapped_df['Category']
                                                                                     == "Bootstrap 1"]], ignore_index=True
)

for i, r in long_dist_df_with_cells.iterrows():
    if r['Category'] == "Bootstrap 0":
        long_dist_df_with_cells.loc[i, 'Category'] = "Experiment_MCF10A"
    elif r['Category'] == "Bootstrap 1":
        long_dist_df_with_cells.loc[i, 'Category'] = "Experiment_HeLa"


def plot_earth_movers(df):
    num_cat = len(df["Category"].unique())
    distances = pd.DataFrame(
        np.zeros((num_cat, num_cat)),
        index=df["Category"].unique(),
        columns=df["Category"].unique(),
    )

    for i, j in list(combinations(df["Category"].unique(), 2)):
        i_dist = df.loc[df["Category"] == i]["distance"].values
        j_dist = df.loc[df["Category"] == j]["distance"].values

        distance = ss.wasserstein_distance(i_dist, j_dist)
        distances.loc[j, i] = distance

    mask = np.triu(np.ones_like(distances))

    # plotting a triangle correlation heatmap
    dataplot = sns.heatmap(distances, cmap="viridis_r", annot=True, mask=mask)
    plt.tight_layout()
    plt.show()


plot_earth_movers(long_dist_df_with_cells)
# plt.savefig(f"{outdir}/wasserstein_distance_image_vs_sim_wMCF10A.png")
# plt.show()
# %%
# dist_df = pd.DataFrame(columns=['distance', 'chr'])
binwidth = 0.05
sns.histplot(
    data=long_dist_df,
    x="distance",
    hue="Category",
    binwidth=binwidth,
    stat="probability",
    common_norm=False,
    kde=True,
)

# num_sim_timepoints = len(long_dist_df[['seed', 'cpc', 'cohesin', 'time']].value_counts().reset_index().index) -1
num_sim_timepoints = (
    (len(long_dist_df["seed"].unique()) - 1)
    * (len(long_dist_df["cpc"].unique()) - 1)
    * (len(long_dist_df["cohesin"].unique()) - 1)
    * 254
)
# num_sim_timepoints = 33
plt.title(
    f"Distances between droplets: 7 Images (n = {len(long_dist_df.loc[long_dist_df['Category']=='Experiment'].index)}) \nvs {num_sim_timepoints} Simulation Timepoints ($n_{{0.01}}$ = {len(long_dist_df.loc[long_dist_df['Category']=='eps = 0.01'].index)},$n_{{0.0075}}$ = {len(long_dist_df.loc[long_dist_df['Category']!='eps = 0.0075'].index)})"
)

plt.xlabel("Distance (um)")
plt.xlim(0, 3.2)
plt.ylim(0, 0.2)
# plt.savefig(
#     f"{outdir}/distances_between_droplets_histplot_image_vs_sim_{binwidth}_v3.png"
# )
plt.show()
# plt.close()

# sns.histplot(
#     data=long_dist_df.loc[long_dist_df["Category"] == "Experiment"],
#     x="distance",
#     bins=30,
#     stat="probability",
#     binwidth=binwidth,
#     common_norm=False,
#     color=sns.color_palette()[1],
#     kde=True,
# )
# plt.xlim(0, 3.2)
# # plt.ylim(0, 0.16)
# plt.title(
#     f"Distances between droplets\n 7 Images, median = {round(long_dist_df.loc[long_dist_df['Category']== 'exp']['distance'].median(),3)}"
# )
# plt.xlabel("Distance (um)")
# # plt.savefig(f"{outdir}distances_between_droplets_histplot_image_{binwidth}.png")
# plt.show()
# %%
# sns.kdeplot(
#     data=long_dist_df,
#     x="distance",
#     hue="Category",
#     common_norm=False,
# )
# plt.show()

# %%
# outdir = f"{indir}/radii_lineplots_kymographs/domain_0_2_noisy_cohesin_sd_0.11"

# sns.kdeplot(
#     data=long_dist_df,
#     x="distance",
#     hue="Category",
#     common_norm=False,
# )
# plt.savefig(
#     f"{outdir}/distances_between_droplets_kde_image_vs_sim_{binwidth}_withMCF10A.png"
# )


# plt.show()


# %%
# Plot images by location of distance (IC-neighbor distance, outside IC-outside IC distance, or IC-IC distance)
# def inter_droplet_distance_with_meta(indir, image):
#     tmp = pd.read_csv(
#         f"{indir}/count_peaks_image{image}_.csv",
#         header=0,
#         index_col=0,
#         converters={"IC_peaks": pd.eval,
#                     "left_peaks": pd.eval, "right_peaks": pd.eval},
#     )
#     distances = pd.DataFrame(columns=["distance", "i"])
#     for i, r in tmp.iterrows():
#         ic = list(r["IC_peaks"])
#         left = list(r["left_peaks"])
#         right = list(r["right_peaks"])
#         [ic.extend(l) for l in (left, right)]
#         all_peaks = sorted(ic)

#         for j in range(len(all_peaks) - 1):
#             d = (all_peaks[j + 1] - all_peaks[j]) * 0.06013
#             if (all_peaks[j + 1] in r["IC_peaks"]) and (all_peaks[j] in r["IC_peaks"]):
#                 IC_distance = "inner-IC distance"
#             elif (all_peaks[j + 1] in r["IC_peaks"]) or (all_peaks[j] in r["IC_peaks"]):
#                 IC_distance = "IC distance"
#             else:
#                 IC_distance = "Outside IC"
#             distances = pd.concat(
#                 [
#                     distances,
#                     pd.DataFrame(
#                         {"distance": [d], "IC_distance": [
#                             IC_distance], "i": [i]}
#                     ),
#                 ],
#                 ignore_index=True,
#             )
#     return distances


# indir2 = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/"
# all_distances = pd.DataFrame(columns=["distance", "IC_distance", "i"])
# for image in [0, 1, 2, 5, 7, 8, 9]:
#     all_distances = pd.concat(
#         [all_distances, inter_droplet_distance_with_meta(indir2, image=image)],
#         ignore_index=True,
#     )

# for i, d in long_dist_df.iterrows():
#     all_distances = pd.concat(
#         [
#             all_distances,
#             pd.DataFrame({"distance": d["distance"],
#                          "IC_distance": ["sim"], "i": 0}),
#         ],
#         ignore_index=True,
#     )


# means = all_distances.groupby("IC_distance").distance.mean()

# print(means)
# sns.kdeplot(data=all_distances, x="distance",
#             hue="IC_distance", common_norm=True)
# # plt.axvline(x=means.loc['IC distance'], c=sns.color_palette("deep")[1], linestyle="--")
# # plt.axvline(x = means.loc['Outside IC'], c=sns.color_palette("deep")[0], linestyle = "--")
# # plt.axvline(x = means.loc['inner-IC distance'], c=sns.color_palette("deep")[2], linestyle = "--")

# plt.title(
#     f"Distances between droplets\n All condensates from 7 images, separated by proximity to inner centromere"
# )
# plt.xlabel("Distance (um)")
# plt.ylabel("Frequency")
# # plt.show()
# plt.savefig(
#     f"{outdir}distances_between_droplets_kdeplot_image_vs_sim_grouped.png")

# %% aggregated bootstraps percent above 1.5um
percent_above_threshold = 100 * \
    sum(bootstrapped_df["distance"].values > 1.5) / \
    len(bootstrapped_df["distance"].values)
percent_above_threshold_MCF10A = 100 * \
    sum(bootstrapped_df_MCF10A["distance"].values > 1.5) / \
    len(bootstrapped_df_MCF10A["distance"].values)
print(
    f"Percent of distances above 1.5 um for HeLa bootstraps: {percent_above_threshold}")
print(
    f"Percent of distances above 1.5 um for MCF10A bootstraps: {percent_above_threshold_MCF10A}")

# %% ave with interval bootstraps percent above 1.5um
percent = []
for b in bootstrapped_df["Category"].unique():
    percent.append(100 * sum(
        bootstrapped_df.loc[bootstrapped_df["Category"] == b]['distance'].values > 1.5) / len(bootstrapped_df.loc[bootstrapped_df["Category"] == b]['distance'].values))
print(
    f"Percent of distances above 1.5 um for HeLa bootstraps by category:")
print("Mean:", np.mean(percent))
print("SEM:", np.std(percent) / np.sqrt(len(percent)))
print("95% CI:", np.percentile(percent, 2.5),
      np.percentile(percent, 97.5))
# MCF10A bootstraps percent above 1.5um
percent_MCF10A = []
for b in bootstrapped_df_MCF10A["Category"].unique():
    percent_MCF10A.append(100 * sum(
        bootstrapped_df_MCF10A.loc[bootstrapped_df_MCF10A["Category"] == b]['distance'].values > 1.5) / len(bootstrapped_df_MCF10A.loc[bootstrapped_df_MCF10A["Category"] == b]['distance'].values))
print(
    f"Percent of distances above 1.5 um for MCF10A bootstraps by category:")
print("Mean:", np.mean(percent_MCF10A))
print("SEM:", np.std(percent_MCF10A) / np.sqrt(len(percent_MCF10A)))
print("95% CI:", np.percentile(percent_MCF10A, 2.5),
      np.percentile(percent_MCF10A, 97.5))


# %% simulations percent above 1.5um
percent_above_threshold_67 = 100 * \
    sum(long_dist_df.loc[long_dist_df["Category"] == category67]['distance'].values > 1.5) / \
    len(long_dist_df.loc[long_dist_df["Category"]
        == category67]['distance'].values)
percent_above_threshold_89 = 100 * \
    sum(long_dist_df.loc[long_dist_df["Category"] == category89]['distance'].values > 1.5) / \
    len(long_dist_df.loc[long_dist_df["Category"]
        == category89]['distance'].values)
print(
    f"Percent of distances above 1.5 um for 0.0067 Sims: {percent_above_threshold_67}")
print(
    f"Percent of distances above 1.5 um for 0.0089 Sims: {percent_above_threshold_89}")
# %% count chromosomes


def count_chromosomes(indir, image):
    tmp = pd.read_csv(
        f"{indir}/count_peaks_image{image}_.csv",
        header=0,
        index_col=0,
        converters={"IC_peaks": pd.eval,
                    "left_peaks": pd.eval, "right_peaks": pd.eval},
    )
    return len(tmp.index)


indir_MCF10A = "/Users/smgroves/Library/CloudStorage/Box-Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans/"
num_chr = 0
for image in range(50):
    try:
        print(image)
        num_chr += count_chromosomes(indir_MCF10A, image=image)
    except FileNotFoundError:
        print(f"File not found for image {image}.")


print("MCF10A chromosome number", num_chr)

# %%
