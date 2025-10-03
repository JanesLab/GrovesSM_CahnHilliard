import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.colors as mcolors

# Figure 5 snapshots


def read_specific_lines(file_path, line_numbers):
    result = []
    with open(file_path, "r") as file:
        for current_line_number, line in enumerate(file):
            if current_line_number in line_numbers:
                digits = [float(i) for i in line.strip("\n").split(" ")]
                result.append(digits)
            if current_line_number > max(line_numbers):
                break
    result = np.array(result)
    return result



# def muted_redblue_cmap(n_colors=1001):
#     """Mimic the MATLAB redbluecmap with muted tones."""
#     n = int(n_colors)
#     bottom = np.array([0.5, 0.5, 1.0])  # muted blue
#     middle = np.array([1.0, 1.0, 1.0])  # white
#     top = np.array([1.0, 0.5, 0.5])     # muted red

#     half = n // 2
#     if n % 2 == 0:
#         # even number of colors
#         blues = np.linspace(bottom, middle, half, axis=0)
#         reds = np.linspace(middle, top, half, axis=0)
#         colors = np.vstack((blues, reds))
#     else:
#         # odd number, keep white in the middle
#         blues = np.linspace(bottom, middle, half, axis=0)
#         reds = np.linspace(middle, top, half + 1, axis=0)
#         colors = np.vstack((blues, reds))

#     return LinearSegmentedColormap.from_list("muted_redblue", colors)

# def redblue(m=None):
#     # If m is not specified, use the current figure's colormap size
#     if m is None:
#         m = plt.get_cmap().N

#     if m % 2 == 0:
#         # Even case: From [0, 0, 1] to [1, 1, 1], then [1, 1, 1] to [1, 0, 0]
#         m1 = m // 2
#         r = np.linspace(0, 1, m1)
#         g = r
#         r = np.concatenate((r, np.ones(m1)))
#         g = np.concatenate((g, np.flipud(g)))
#         b = np.flipud(r)
#     else:
#         # Odd case: From [0, 0, 1] to [1, 1, 1], then [1, 1, 1] to [1, 0, 0]
#         m1 = m // 2
#         r = np.linspace(0, 1, m1)
#         g = r
#         r = np.concatenate((r, np.ones(m1 + 1)))
#         g = np.concatenate((g, [1], np.flipud(g)))
#         b = np.flipud(r)

#     # Combine r, g, b to create the colormap array
#     c = np.vstack((r, g, b)).T
#     return c


def plot_snapshot(
    indir, name, Nx, dt, dt_out=10, time=None, timepoint=None, save=False, outdir=""
):
    if time != None:
        timepoint = int(time / (dt * dt_out))
    elif timepoint != None:
        time = timepoint * dt
    else:
        raise Exception(
            "Either time or timepoint must be set. time = timepoint * dt.")
    print(timepoint)
    first_line = timepoint * Nx
    last_line = first_line + Nx

    line_list = range(first_line, last_line)

    # fig = plt.figure(figsize=(3, 4), dpi=300)
    fig = plt.figure(figsize=(2, 4), dpi=300)

    normalize_phis = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1, vmax=1)

    snapshot = read_specific_lines(f"{indir}/{name}", line_list)
    sns.heatmap(
        snapshot[int(Nx/4):int(3*Nx/4)].T, #get rid of padding on left and right
        square=True,
        # cmap=plt.cm.colors.ListedColormap(redblue(100)),
        cmap=cm.RdBu_r,
        norm=normalize_phis,
        xticklabels=False,
        yticklabels=False,
        linewidths=0,
        cbar=False
    )
    # plt.title(f"t = {time}")
    plt.tight_layout()
    if save:
        plt.savefig(f"{outdir}/t={time}_{name}_only_heatmap_matlab_colors.png")
        plt.close()
    else:
        plt.show()

# phi_512_262144_1.0e-5__CPC_0.12_cohesin_0.14_eps_0.0067_domain_0_2
# phi_512_262144_1.0e-5__CPC_0.35_cohesin_0.12_eps_0.0067_domain_0_2
# name = "phi_512_262144_1.0e-5__CPC_0.25_cohesin_0.11_eps_0.0067_domain_0_2.txt"
# indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0075"
# name = "phi_512_19661_1.0e-5__CPC_0.173_cohesin_0.08_eps_0.0075_alpha_0_domain_0_2.txt"
# name = "phi_256_19661_1.0e-5__CPC_0.125_cohesin_0.08_eps_0.0075_domain_0_1.txt"
# phi_512_262144_1.0e-5__CPC_0.35_cohesin_0.14_eps_0.0067_domain_0_2

Nx = 512

#figure 5 t = 0.04
indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.04"
for CPC in ["0.35", "0.12"]:
    for cohesin in ["0.14", "0.12","0.09","0.06"]:
        name = f"phi_{Nx}_26214_1.0e-5__CPC_{CPC}_cohesin_{cohesin}_eps_0.0067_domain_0_2.txt"
        outdir = f"{indir}/snapshots_eps_0.0067_t_0.04/{'_'.join(name.split('_')[5:11])}"
        os.makedirs(outdir) if not os.path.exists(outdir) else None

        for time in [0, 0.01, 0.02, 0.03, 0.04]:
            try:
                plot_snapshot(
                    indir,
                    name,
                    Nx,
                    time=time,
                    dt=0.000001525878906,
                    save=True,
                    outdir=outdir,
                )
            except IndexError: print("Time {time} would not plot.")


#long-run simulations for Figure 5
indir="/project/g_bme-janeslab/SarahG/julia_out/CPC_geometry/CPC_domain_0_2_e_0.0067_t_0.4"

for CPC in ["0.35", "0.12"]:
    for cohesin in ["0.14", "0.12"]:
        name = f"phi_{Nx}_262144_1.0e-5__CPC_{CPC}_cohesin_{cohesin}_eps_0.0067_domain_0_2.txt"
        outdir = f"{indir}/snapshots_eps_0.0067_t_0.4/{'_'.join(name.split('_')[5:11])}"
        os.makedirs(outdir) if not os.path.exists(outdir) else None

        for time in [0, 0.1, 0.2, 0.3, 0.4]:
            try:
                plot_snapshot(
                    indir,
                    name,
                    Nx,
                    time=time,
                    dt=0.000001525878906,
                    save=True,
                    outdir=outdir,
                )
            except IndexError: print("Time {time} would not plot.")
#3265183 t = 0.4


# # for time in [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.08, 0.1, 0.2, 0.3, 0.35]:
# # for time in [0.05, 0.15, 0.18, 0.22, 0.25, 0.28]:
# for time in [0.025, 0.03]:
#     plot_snapshot(
#         indir,
#         name,
#         Nx,
#         time=time,
#         dt=0.000001525878906,
#         save=True,
#         outdir=f"{indir}/",
#     )
