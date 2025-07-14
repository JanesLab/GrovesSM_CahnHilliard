# Plotting for each individual alpha and epsilon. This will plot the radius over time to figure out what the critical radius for each epsilon is.
# After this, use the plot_inflection_pt.m code to find the inflection points, and record these in critical_radii_epsilon.csv.
###############################
#  FIGURE 3B and 3C, S3A and B
###############################
# %%
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap, BoundaryNorm
# indir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/radii_lineplots_kymographs/alt_IC_periodic_BC_split_droplet"

indir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output"
# #%%
# tmp = pd.read_csv(f"{indir}/from_Rivanna/radius_0.5_level_set_epsilon_0.015009.txt",header = 0, index_col=None)
# print(tmp.shape)
# # %%
# tmp['R0'].unique()

# #%%
# sns.lineplot(data = tmp, x = 'time', y = 'radius', hue = 'R0', palette = 'tab20')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.title("Epsilon = 0.015009")
# plt.savefig(f"{indir}/critical_radius_vs_epsilon_0.015009.pdf")

# plt.show()
# # %%
# tmp = pd.read_csv(f"{indir}/from_Rivanna/radius_0.5_level_set_epsilon_0.030019.txt",header = 0, index_col=None)
# print(tmp.shape)
# sns.lineplot(data = tmp, x = 'time', y = 'radius', hue = 'R0', palette = 'tab20')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.title("Epsilon = 0.030019")
# plt.savefig(f"{indir}/critical_radius_vs_epsilon_0.030019.pdf")
# # plt.show()
# # %%
# tmp = pd.read_csv(f"{indir}/from_Rivanna/radius_0.5_level_set_epsilon_0.060037.txt",header = 0, index_col=None)
# print(tmp.shape)
# #%%
# sns.lineplot(data = tmp, x = 'time', y = 'radius', hue = 'R0', palette = 'tab20')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.title("Epsilon = 0.060037")
# plt.savefig(f"{indir}/critical_radius_vs_epsilon_0.060037.pdf")
# # plt.show()
# %%
# Reuse this one
# alpha = "0.5"
plt.rcParams["font.family"] = "Arial"

# the default from Min-Jhe's code was to use phi = 0 or psi = 0.5, so for the plotting without alpha it will be 0.5
level_set_radius = "0.5"
Nx = 128
alpha = 0
# for epsilon in ["0.011257", "0.0037523","0.0056285", "0.0075047"]:#,"0.060037"]:#,"0.04","0.075047","0.090056"
for epsilon in [
    "0.011257"
    # "0.015009",
    # "0.030019",
    # "0.045028",
    # "0.0075046",
    # "0.075047",
    # "0.060037",
    # "0.090056",
]:
    # for epsilon in ["0.0037523", "0.0075046", "0.0018761", "0.015009"]:
    folder = f"critical_radius"
    indir_radius = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/radii_lineplots_kymographs/offcenter_IC_droplet/"
    tmp = pd.read_csv(
        # f"{indir}/{folder}/alpha_0.0/radius_{level_set_radius}_level_set_epsilon_{epsilon}_alpha_0.0.txt",
        f"{indir_radius}/radius_{level_set_radius}_level_set_epsilon_{epsilon}_128__periodic_offcenterphi.txt",
        header=0,
        index_col=None,
        sep=",",
        on_bad_lines="skip",
    )
    # tmp = pd.read_csv(
    # f"{indir}/{folder}/alpha_{alpha}/radius_{level_set_radius}_level_set_epsilon_{epsilon}.txt",
    # header=0,
    # index_col=None,
    # sep=",",
    # on_bad_lines='skip')

    # what to keep
    tmp = tmp.drop(
        tmp[
            ~tmp["R0"].isin(
                # [0.111, 0.11155, 0.113, 0.1116, 0.112, 0.114, 0.11675, 0.117]
                [0.09, 0.1, 0.105, 0.11, 0.12]
            )
        ].index
    )
    # tmp = tmp.drop(tmp[tmp["time"] > 0.011].index)
    print(tmp.shape)
    # tmp.fillna(0, inplace=True)

    tmp = tmp.sort_values("R0", ascending=False)
    meta = pd.read_csv(
        f"{indir}/{folder}/critical_radii_epsilon copy.csv", header=0, index_col=None
    )
    crit_rad = meta.loc[
        (meta["alpha"] == float(alpha))
        & (meta["epsilon"] == float(epsilon))
        & (meta["Nx"] == Nx)
    ]["critical equilibrium radius (min)"].iloc[0]
    crit_rad_init = meta.loc[
        (meta["alpha"] == float(alpha))
        & (meta["epsilon"] == float(epsilon))
        & (meta["Nx"] == Nx)
    ]["critical initial radius"].iloc[0]
    plt.axhline(crit_rad, linestyle="--", color="lightgrey")
    plt.axhline(crit_rad_init, linestyle="--", color="lightgrey")
    # sns.lineplot(data=tmp, x="time", y="radius", hue="R0", palette="tab20")
    for i, r in enumerate(np.unique(tmp["R0"])):
        tmp_r = tmp.loc[tmp["R0"] == r].sort_values("time")
        last = tmp_r["radius"].last_valid_index()
        print(last)
        tmp_r.loc[last + 1, "radius"] = 0
        plt.plot(
            tmp_r["time"],
            tmp_r["radius"],
            color=sns.color_palette()[i],
            label=r,
        )
    plt.legend(
        loc="center left",
        title="R0",
        bbox_to_anchor=(1, 0.5),
        fontsize="large",
        reverse=True,
    )
    plt.xscale("log")
    plt.title(f"Epsilon = {epsilon}")
    # plt.axhline(0.07, linestyle="--", color="gray")
    plt.ylim(0, 0.14)
    plt.xlim(1e-3, 1e1)
    plt.xlabel("Time (tchar)")
    plt.ylabel("Radius (R)")
    plt.tight_layout()
    # plt.savefig(
    #     f"{indir}/{folder}/alpha_0.0/critical_radius_vs_epsilon_{epsilon}_subset_log_v2.pdf"
    # )
    plt.savefig(
        f"{indir_radius}/critical_radius_vs_epsilon_{epsilon}_offcenter_log_v2.pdf")
    plt.close()
    # plt.show()
# %%


# %%

# %% With a linear color mapping
alpha = "0.0"
level_set_radius = "0.5"
Nx = 128
for epsilon in [
    # "0.0037523",
    # "0.0075047",
    # "0.0075046",
    # "0.0018761",
    "0.015009",
    # "0.030019",
]:  # ,"0.060037"]:#,"0.04","0.075047","0.090056"
    # for epsilon in [
    # "0.015009",
    #     "0.030019",
    #     "0.045028",
    #     "0.0075046",
    #     # "0.075047",
    #     "0.090056",
    # ]:

    # for epsilon in ["0.015009", "0.030019", "0.0075046", "0.0018761", "0.0037523"]:
    meta = pd.read_csv(
        f"{indir}/{folder}/critical_radii_epsilon copy.csv", header=0, index_col=None
    )
    crit_rad = meta.loc[
        (meta["alpha"] == float(alpha))
        & (meta["epsilon"] == float(epsilon))
        & (meta["Nx"] == Nx)
    ]["critical equilibrium radius (min)"].iloc[0]
    folder = f"critical_radius"
    tmp = pd.read_csv(
        # f"{indir}/{folder}/alpha_{alpha}/radius_{level_set_radius}_level_set_{Nx}_epsilon_{epsilon}_alpha_{alpha}.txt",
        f"{indir}/{folder}/alpha_{alpha}/radius_{level_set_radius}_level_set_epsilon_{epsilon} copy.txt",
        header=0,
        index_col=None,
        sep=",",
        on_bad_lines="skip",
    )
    # tmp = pd.read_csv(
    # f"{indir}/{folder}/alpha_{alpha}/radius_{level_set_radius}_level_set_epsilon_{epsilon}.txt",
    # header=0,
    # index_col=None,
    # sep=",",
    # on_bad_lines='skip')
    # tmp = tmp.drop(tmp[tmp["R0"].isin([0.1,0.11, 0.1111, 0.1112, 0.1113, 0.1114, 0.1115])].index)
    print(tmp.shape)
    tmp = tmp.sort_values("R0")
    color_values = tmp["R0"]
    norm = Normalize(vmin=np.min(color_values), vmax=np.max(color_values))
    # norm = Normalize(vmin=0, vmax=0.2)

    colormap = cm.jet
    tmp.fillna(0, inplace=True)
    for r in np.unique(tmp["R0"]):
        tmp_r = tmp.loc[tmp["R0"] == r].sort_values("time")
        color = colormap(norm(r))
        plt.plot(tmp_r["time"], tmp_r["radius"], color=color)
    # plt.ylim(0, 0.2)
    # sns.lineplot(data=tmp, x="time", y="radius", hue="hue")
    # plt.legend(loc="center left",
    #            title="R0",
    #            bbox_to_anchor=(1, 0.5),
    #            fontsize="small")
    sm = cm.ScalarMappable(cmap=colormap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, label=f"R0 Value")
    ticks = np.unique(tmp["R0"])
    # tick_positions = norm(ticks)
    cbar.set_ticks(ticks)
    # plt.clim(np.min(color_values), np.max(color_values))
    plt.axhline(crit_rad, linestyle="--", color="lightgrey")
    plt.title(f"Epsilon = {epsilon}, alpha = {alpha}")
    # plt.axhline(0.07, linestyle="--", color="gray")
    plt.tight_layout()
    plt.show()
    plt.savefig(
        f"{indir}/{folder}/alpha_{alpha}/critical_radius_vs_epsilon_{epsilon}_alpha_{alpha}_nx_{Nx}_radius_{level_set_radius}_.pdf"
    )
    # plt.close()


# %%
epsilon = "0.030019"
radius = 0.0148
tmp = pd.read_csv(
    f"{indir}/from_Rivanna/radius_0.5_level_set_epsilon_{epsilon}.txt",
    header=0,
    index_col=None,
)
tmp_old = pd.read_csv(
    f"{indir}/from_Rivanna_old/radius_0.5_level_set_epsilon_{epsilon}.txt",
    header=0,
    index_col=None,
)
tmp = tmp.loc[tmp["R0"] == 0.148].dropna()
tmp_old = tmp_old.loc[tmp_old["R0"] == 0.148].dropna()
plt.plot(tmp["time"].values, tmp["radius"].values, label="new IC")
plt.plot(tmp_old["time"].values, tmp_old["radius"].values, label="old IC")
plt.legend()
plt.title("R0 = 0.148 for epsilon 0.033019")
plt.xlabel("Time")
plt.ylabel("Radius")
plt.savefig(f"{indir}/r0_{radius}_new_old_IC.pdf")

# %%
# from scipy.ndimage import gaussian_filter1d

# data = tmp.loc[tmp['R0']==0.133].dropna()['radius'].values
# data = data/np.max(data)

# smooth = gaussian_filter1d(data, 100)
# smooth_d1 = (np.gradient(data))

# # compute second derivative
# smooth_d2 = np.diff(np.diff(data))
# print(smooth_d2)
# # find switching points
# infls = np.where(np.diff(np.sign(smooth_d2)))[0]

# # plot results
# plt.plot(data, label='Data')
# plt.show()
# # plot results
# plt.plot(smooth_d1, label='Data')
# plt.ylim(-0.005,0.01)

# plt.show()
# plt.plot(smooth_d2, label='Second Derivative (scaled)')
# for i, infl in enumerate(infls, 1):
#     plt.axvline(x=infl, color='k', label=f'Inflection Point {i}')
# plt.ylim(-0.005,0.01)
# plt.legend(bbox_to_anchor=(1.55, 1.0))
# %%
epsilon = np.array([0.015009, 0.030019, 0.060037])
critical_radius = np.array([0.07, 0.095, 0.14])
plt.plot(epsilon, critical_radius, marker="o", label="Data")

x = epsilon.reshape((-1, 1))
y = critical_radius
model = LinearRegression().fit(x, y)
y_pred = model.intercept_ + model.coef_ * x
plt.plot(epsilon, y_pred, linestyle="--", label="Regression")
plt.legend(bbox_to_anchor=(1.55, 1.0))
eps = ((0.108 - model.intercept_) / model.coef_)[0]
plt.annotate(
    f"Eps($R_c$= .108)={np.round(eps,6)}",
    xy=(eps, 0.108),
    xytext=(1.1 * eps, 0.108),
    va="center",
    ha="left",
    arrowprops=dict(arrowstyle="-|>"),
)
plt.title("Epsilon versus critical radius for single droplet")
plt.savefig(f"{indir}/epsilon_vs.critical_radius.pdf")

# %%
#############################################
# Troubleshooting the problems with e= 0.045
#############################################
alpha = "-0.5"

epsilon = "0.045028"
folder = f"critical_radius/"
tmp = pd.read_csv(
    f"{indir}/{folder}/radius_0.5_level_set_epsilon_{epsilon}_alpha_{alpha}.txt",
    header=0,
    index_col=None,
    sep=",",
    on_bad_lines="warn",
)
print(tmp.shape)
# USE WARN TO DELETE THOSE ROWS

# %%
g = sns.lineplot(data=tmp, x="time", y="radius", hue="R0", palette="tab20")
g.set_xticks([tmp["time"].min(), tmp["time"].max()])
g.set_yticks([tmp["radius"].min(), tmp["radius"].max()])

plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small")
plt.title(f"Epsilon = {epsilon}, alpha = {alpha}")
plt.tight_layout()
plt.savefig(
    f"{indir}/{folder}/critical_radius_vs_epsilon_{epsilon}_alpha_{alpha}.pdf")
plt.close()
# %%
for i, r in tmp.iterrows():
    try:
        f = float(r["time"])
    except:
        print(i)
        print(r)

# OUTPUT FOR TIME
# 34654 X
# radius       NaN
# time      5..061
# R0           NaN
# Name: 34654, dtype: object
# 35695 X
# radius          NaN
# time      6.717.061
# R0              NaN
# Name: 35695, dtype: object

# OUTPUT FOR RADIUS
# 34134 X
# radius     NaaN
# time       0.62
# R0        0.061
# Name: 34134, dtype: object
# 34907 X
# radius    Na3725
# time        0.06
# R0           NaN
# Name: 34907, dtype: object
# 38034 X
# radius    N5.67
# time      0.061
# R0          NaN
# Name: 38034, dtype: object

# OUTPUT FOR R0
# 36737 X
# radius        NaN
# time       8.0625
# R0        0.0.061
# Name: 36737, dtype: object

# %%
