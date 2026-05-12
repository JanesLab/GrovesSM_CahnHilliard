# %% FIGURE 1 COMPARISONS
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib import font_manager
from matplotlib import rcParams

# for f in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
#     if 'arial' in f.lower():
#         print(f)


# arial_path = "/System/Library/Fonts/Supplemental/Arial.ttf"  # e.g., from Step 1
# arial_font = font_manager.FontProperties(fname=arial_path)
# rcParams["font.family"] = arial_font.get_name()
plt.rcParams['pdf.use14corefonts'] = True

boundary = "periodic"
outdir = f"/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_MATLAB-{boundary}"
indir_MG = f"/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_MATLAB-{boundary}"
indir_SAV = f"/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_MATLAB-{boundary}"

# %% LOAD NMG
# phi_name_NMG = "NMG_MATLAB_2000_dt_5.50e-06_Nx_128_n_relax_4_dtout_1_phi.csv"
# indir_MG = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output/spinodal_smooth_relax_function/output"
# phi_name_MG = "MG_2000_dt_5.5e-6_Nx_128_n_relax_4_eps_0.015009369912862116_phi.txt"

phi_name_NMG = "/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_julia/NMG_Julia_6000_dt_5.50e-06_Nx_128_n_relax_4_phi.csv"

phi_MG = np.genfromtxt(
    f"{phi_name_NMG}",
    delimiter=",",
)

phi_MG = phi_MG.reshape(-1, 128, 128).transpose(1, 2, 0)

# %% LOAD SAV
phi_name_SAV = "SAV_MATLAB_2000_dt_5.50e-06_Nx_128_n_relax_4_dtout_1_phi.csv"
# indir_SAV = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/SAV/output/spinodal_smooth_relax_function"
# phi_name_SAV = "SAV_MATLAB_2000_dt_5.50e-06_Nx_128_n_relax_4_phi.csv"

phi_SAV = np.genfromtxt(f"{indir_SAV}/{phi_name_SAV}", delimiter=",")

phi_SAV = phi_SAV.reshape(-1, 128, 128).transpose(1, 2, 0)

# %% LOAD FD IE
indir_FD = "/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_MATLAB-neumann_FD_IE"
phi_name_FD = "FD_IE_MATLAB_2000_dt_5.50e-06_Nx_128_n_relax_4_dtout_1_phi.csv"

phi_FD = np.genfromtxt(f"{indir_FD}/{phi_name_FD}", delimiter=",")
phi_FD = phi_FD.reshape(-1, 128, 128).transpose(1, 2, 0)


# %% save individual plots: FD_IE
###############################################


# timepoints = [40, 60]
timepoints = [1, 2, 40, 100, 200]

# timepoints = [200, 400]
dt_out = 10
dt = 5.5e-6
for timepoint in timepoints:
    normalize_phis = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1, vmax=1)
    s = sns.heatmap(
        phi_FD[:, :, timepoint],
        square=True,
        cmap=cm.RdBu_r,
        norm=normalize_phis,
        cbar=False,
        linewidths=0.0,
    )
    plt.xticks(ticks=[], labels=[])
    plt.yticks(ticks=[], labels=[])
    # plt.title(f"Time= {timepoint*dt}")
    plt.tight_layout()
    plt.savefig(
        f"{indir_FD}/FD_IE_2000_dt_5.5e-6_t_{timepoint*dt*dt_out:.2e}_neumann.png",
        bbox_inches="tight",
        pad_inches=0,
        dpi=300,
    )
    plt.show()

    plt.close()

###############################################
# %% comparing energy and mass
###############################################

# FIGURE S1


def get_energy(indir, phi_name, dt, dt_out, variable="energy", suffix="csv", title=""):
    e_name = "_".join(phi_name.split("_")[:-1])
    e_name = e_name + f"_{variable}.{suffix}"
    print(e_name)
    e = pd.read_csv(f"{indir}/{e_name}", header=None, index_col=None)
    l = [x * dt * dt_out for x in range(len(e.iloc[:, 0]))]
    e.columns = [title]
    e["time"] = l
    return e


# %%

e_NMG = get_energy(
    indir_MG, phi_name_MG, dt=5.5e-6, dt_out=1, suffix="csv", title="NMG"
)
e_SAV = get_energy(indir_SAV, phi_name_SAV, dt=5.5e-6,
                   dt_out=1, title="SAV")

e_FD = get_energy(indir_FD, phi_name_FD, dt=5.5e-8, dt_out=1, title="FD")
e_FD_big = get_energy(indir_FD, phi_name_FD_big,
                      dt=5.5e-7, dt_out=1, title="FD_big")


# updated code returns unnormalized energy
e_SAV['SAV'] = e_SAV['SAV'] / e_SAV['SAV'].iloc[0]
e_NMG['NMG'] = e_NMG['NMG'] / e_NMG['NMG'].iloc[0]


# %% four separate energy figures
for i, e in enumerate([e_NMG, e_SAV]):  # , e_FD, e_FD_big]):
    plt.figure(figsize=(4, 3))
    ax = sns.lineplot(x=np.log10(e["time"]+1e-8), y=e.iloc[:, 0],
                      markers=True, c=sns.color_palette()[i])
    plt.ylabel("Normalized Energy")
    plt.xlabel(r"Time ($log_{10}(t_{char})$)")
    plt.ylim(0.0, 1)
    # ax.set(xscale="log")
    # ax.set(xticks = np.arange(0, 0.012, 0.002))
    # plt.title("Normalized (Modified) Energy for Spinodal Decomposition")
    if e.iloc[:, 0].name == "FD":
        title = "FD, dt = 5.5e-8"
        plt.title(title)
        plt.xlim(-8, -2)

    elif e.iloc[:, 0].name == "FD_big":
        title = "FD, dt = 5.5e-7"
        plt.title(title)
        plt.xlim(-8, -2)

    else:
        title = f"{e.iloc[:, 0].name}, dt=5.5e-6"
        plt.title(title)
        plt.xlim(-8, -2)
    plt.ticklabel_format(style="plain", axis="x")
    plt.tight_layout()
    # plt.show()

    plt.savefig(f"{outdir}/{title}_energy_{boundary}_log.pdf")

# %%

# %% all-in-one energy figure
outdir = "/Users/smgroves/Documents/GitHub/CHsolvers_package/output/energy_mass_comparisons"

plt.figure(figsize=(8, 3))

for i, e in enumerate([e_NMG, e_SAV]):  # , e_FD, e_FD_big]):

    plt.ylabel("Normalized Energy")
    plt.xlabel(r"Time ($t_{char}$)")
    plt.ylim(1e-8, 1)
    # ax.set(xscale="log")
    # ax.set(xticks = np.arange(0, 0.012, 0.002))
    # plt.title("Normalized (Modified) Energy for Spinodal Decomposition")
    if e.iloc[:, 0].name == "FD":
        sns.lineplot(x=e["time"], y=e.iloc[:, 0],
                     markers=True, c=sns.color_palette()[i], label="FD, dt = 5.5e-8")
    elif e.iloc[:, 0].name == "FD_big":
        sns.lineplot(x=e["time"], y=e.iloc[:, 0],
                     markers=True, c=sns.color_palette()[i], label="FD, dt = 5.5e-7")

    else:
        g = sns.lineplot(x=e["time"], y=e.iloc[:, 0],
                         markers=True, c=sns.color_palette()[i], label=f"{e.iloc[:, 0].name}, dt=5.5e-6")
    plt.xlim(0, 0.00011)
    plt.ticklabel_format(style="plain", axis="x")

    plt.tight_layout()

plt.savefig(f"{outdir}/all_solvers_T_0.00011_energy_periodic.pdf")
plt.show()


# %%
for e in [e_NMG, e_FD, e_SAV]:
    sns.lineplot(x=e["time"], y=e.iloc[:, 0], label=e.columns[0], alpha=0.6)
plt.xlim(0.01, 0.0111)
plt.ylim(0.255, 0.27)
plt.ylabel("")
plt.xlabel("")
# plt.title("Normalized (Modified) Energy for Spinodal Decomposition")
# plt.savefig(f"{outdir}/FD_NMG_SAV_energy_zoom_end.pdf")
plt.show()
# %% MASS COMPARISONS

m_NMG = get_energy(indir_MG, phi_name_MG, dt=5.5e-6, dt_out=1, variable="mass_uncentered", title="NMG",
                   )
m_SAV = get_energy(indir_SAV, phi_name_SAV, dt=5.5e-6, variable="mass_uncentered", dt_out=1, title="SAV"
                   )
# m_FD = get_energy(indir_FD, phi_name_FD, dt=5.5e-8, variable="mass", dt_out=1, title="FD"
#                   )
# m_FD_big = get_energy(indir_FD, phi_name_FD_big, dt=5.5e-7, variable="mass", dt_out=1, title="FD_big"
#                       )

# %%

# %%%
# m_FD["FD"] = m_FD["FD"] - m_FD["FD"].iloc[0]
# m_FD_big["FD_big"] = m_FD_big["FD_big"] - m_FD_big["FD_big"].iloc[0]

m_NMG["NMG"] = m_NMG["NMG"] - m_NMG["NMG"].iloc[0]
m_SAV["SAV"] = m_SAV["SAV"] - m_SAV["SAV"].iloc[0]

# %%

# %%
# for m in [m_NMG, m_FD, m_SAV]:
#     sns.lineplot(x=m["time"], y=m.iloc[:, 0], label=m.columns[0], alpha=0.6)
# plt.ylabel("Normalized Average Mass")
# plt.xlabel(r"Time ($t_{char}$)")
# plt.title("Normalized Average Mass for Spinodal Decomposition")
# # plt.savefig(f"{outdir}/FD_NMG_SAV_mass.pdf")
# plt.show()
# %%
for i, e in enumerate([m_NMG, m_SAV]):  # , m_FD, m_FD_big]):
    plt.figure(figsize=(4, 3))
    plt.axhline(y=0, c="gray", linewidth=.75)

    ax = sns.lineplot(x=np.log10(e["time"]+1e-8),
                      y=e.iloc[:, 0], c=sns.color_palette()[i])
    ax.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

    plt.axhline(y=1e-5, xmin=0, xmax=1,  c='gray',
                linestyle="--", linewidth=.75)
    plt.axhline(y=-1e-5, xmin=0, xmax=1,  c='gray',
                linestyle="--", linewidth=.75)
    plt.ylabel("M - M[0]")
    plt.xlabel(r"Time ($log_{10}(t_{char})$)")
    # ax.set(xscale="log")
    # ax.set(xticks = np.arange(0, 0.012, 0.002))
    # plt.title("Normalized (Modified) Energy for Spinodal Decomposition")
    if e.iloc[:, 0].name == "FD":
        title = "FD, dt = 5.5e-8"
        plt.title(title)
        plt.xlim(-8, -2)

    elif e.iloc[:, 0].name == "FD_big":
        title = "FD, dt = 5.5e-7"
        plt.title(title)
        plt.xlim(-8, -2)

    else:
        title = f"{e.iloc[:, 0].name}, dt=5.5e-6"
        plt.title(title)
        plt.xlim(-8, -2)    # ax.set(xscale="log")
    # ax.set(xticks = np.arange(0, 0.012, 0.002))
    # plt.title("Normalized (Modified) Energy for Spinodal Decomposition")

    plt.ylim(-1e-4, 1e-4)
    # plt.title(f"{e.iloc[:, 0].name}")
    # plt.ticklabel_format(style="plain", axis="x")
    plt.tight_layout()
    # plt.show()

    plt.savefig(f"{outdir}/{title}_mass_{boundary}_log.pdf")
    plt.close()


# %%
plt.figure(figsize=(8, 3))

for i, e in enumerate([m_NMG, m_SAV, m_FD, m_FD_big]):

    plt.ylabel("Mass - Mass[0]")
    plt.xlabel(r"Time ($t_{char}$)")
    plt.ylim(1e-8, 1)
    # ax.set(xscale="log")
    # ax.set(xticks = np.arange(0, 0.012, 0.002))
    # plt.title("Normalized (Modified) Energy for Spinodal Decomposition")
    if e.iloc[:, 0].name == "FD":
        sns.lineplot(x=e["time"], y=e.iloc[:, 0],
                     markers=True, c=sns.color_palette()[i], label="FD, dt = 5.5e-8")
    elif e.iloc[:, 0].name == "FD_big":
        sns.lineplot(x=e["time"], y=e.iloc[:, 0],
                     markers=True, c=sns.color_palette()[i], label="FD, dt = 5.5e-7")

    else:
        g = sns.lineplot(x=e["time"], y=e.iloc[:, 0],
                         markers=True, c=sns.color_palette()[i], label=f"{e.iloc[:, 0].name}, dt=5.5e-6")
    plt.xlim(0, 0.011)
    plt.ylim(-1e-5, 1e-5)

    plt.ticklabel_format(style="plain", axis="x")

    plt.tight_layout()

plt.savefig(f"{outdir}/all_solvers_T_0.011_mass_neumann.pdf")
plt.show()
# %%
l2err_t = []
for t in range(phi_MG.shape[2]):
    l2err_t.append(np.sum(np.sum((phi_MG[:, :, t]-phi_SAV[:, :, t])**2)))

plt.plot(range(len(l2err_t)), l2err_t, label="NMG vs SAV")
plt.show()

# %%
# average mass checks
# redblue colormap centered at 0
cmap = cm.RdBu_r
normalize = mcolors.TwoSlopeNorm(vcenter=0)
# plot the difference between the two methods
sns.heatmap(phi_MG[:, :, 1] - phi_SAV[:, :, 1],
            cmap=cmap, norm=normalize, cbar=True, square=True)
plt.show()
# %%


# %% # Testing periodic NMG
##########################
indir_MATLAB = "/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_MATLAB-periodic"
indir_Julia = "/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_julia"
phi_name_TEST_NMG = "periodic_NMG_testv2_phi.csv"

phi_TEST_NMG = np.genfromtxt(
    f"{indir_Julia}/{phi_name_TEST_NMG}",
    delimiter=",",
)

phi_TEST_NMG = phi_TEST_NMG.reshape(-1, 64, 64).transpose(1, 2, 0)

phi_name_TEST_SAV = "periodic_SAV_test_phi.csv"

phi_TEST_SAV = np.genfromtxt(
    f"{indir_MATLAB}/{phi_name_TEST_SAV}",
    delimiter=",",
)

phi_TEST_SAV = phi_TEST_SAV.reshape(-1, 64, 64).transpose(1, 2, 0)
# %%
# phi0(1,10) = 2;
# phi0(32, 1) = 6;
# phi0(32,32) = 10;
# phi0(50, 64) = 8;
# phi0(64,25) = 4;

# for t in range(phi_TEST_SAV.shape[2]):
#     plt.subplot(1, 2, 1)
#     plt.imshow(phi_TEST_NMG[:, :, t], cmap="viridis", vmin=0, vmax=10)
#     plt.title(f"NMG, Time = {t}")
#     plt.subplot(1, 2, 2)
#     plt.imshow(phi_TEST_SAV[:, :, t], cmap="viridis", vmin=0, vmax=10)
#     plt.title(f"SAV, Time = {t}")
#     plt.colorbar()
#     plt.tight_layout()
#     plt.show()

# %%
# # RdBu map centered at 0
cmap = cm.RdBu_r
normalize = mcolors.TwoSlopeNorm(vcenter=0)
# plt.figure(figsize=(10, 5))
# plt.subplot(1, 2, 1)
# sns.heatmap(phi_TEST_SAV[:, :, 0]-phi_TEST_SAV[:, :, 1],
#             cmap=cmap, norm=normalize, cbar=True,)
# plt.title("SAV, Time = 0 - 1")
# plt.subplot(1, 2, 2)
sns.heatmap(phi_TEST_NMG[:, :, 0]-phi_TEST_NMG[:, :, 1],
            cmap=cmap, norm=normalize, cbar=True,)
plt.title("NMG, Time = 0 - 1")
plt.tight_layout()
plt.show()

# %%
cmap = cm.RdBu_r
# normalize = mcolors.TwoSlopeNorm(vcenter=0)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.heatmap(phi_TEST_SAV[:, :, 1],)
# cmap=cmap, norm=normalize, cbar=True,)
plt.title("SAV, Time = 1")
plt.subplot(1, 2, 2)
sns.heatmap(phi_TEST_NMG[:, :, 1],)
# cmap=cmap, norm=normalize, cbar=True,)
plt.title("NMG, Time = 1")
plt.tight_layout()
plt.show()
# %%
range_x = 4
range_y = 4
timepoint = 1
# check the mass in a 3x3 box around the initial conditions
inits = np.array([[0, 9, 2], [63, 24, 4], [31, 0, 6],
                 [49, 63, 8], [31, 31, 10]])

for c in inits:
    print("Location:", c[0], c[1])
    print("Initial mass:", c[2])
    mass = 0
    centered_array = np.zeros((range_x * 2 + 1, range_y * 2 + 1))
    # loop through the range around the initial condition
    # and sum the mass in that range
    for i, x in enumerate(range(c[0]-range_x, c[0]+range_x+1)):
        for j, y in enumerate(range(c[1]-range_y, c[1]+range_y+1)):
            if x < 0:
                x = 64 + x
            if y < 0:
                y = 64 + y
            if x > 63:
                x = x - 64
            if y > 63:
                y = y - 64
            # print(x, y, phi_TEST_NMG[x, y, 1])
            mass += phi_TEST_NMG[x, y, 0]
            centered_array[i, j] = phi_TEST_NMG[x, y, timepoint]

    print("Total mass:", mass)
    sns.heatmap(centered_array, cmap="viridis", annot=True, fmt=".2f",)
    # plt.colorbar()
    # change axis labels to be centered around the initial condition
    plt.yticks(ticks=range(0, range_x * 2 + 1),
               labels=[l % 64 for l in range(c[0]-range_x, c[0]+range_x + 1)])
    plt.xticks(ticks=range(0, range_y * 2 + 1),
               labels=[l % 64 for l in range(c[1]-range_y, c[1]+range_y + 1)])
    plt.title(f"Centered Mass around {c[0]},{c[1]} at t={timepoint}")
    plt.show()


# %%
