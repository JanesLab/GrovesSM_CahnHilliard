import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors


def read_chunk(phi_name, indir, timepoint,delim= " ", rows_per_timepoint = 128):
    start_row = timepoint * rows_per_timepoint
    end_row = start_row + rows_per_timepoint
    # Read only the required rows
    phi_chunk = np.genfromtxt(
        f"{indir}/{phi_name}", 
        skip_header=start_row, 
        max_rows=rows_per_timepoint,
        delimiter=delim
    )
    return phi_chunk 

def plot_timepoint(phi_name, indir, outdir, timepoints, delim = " ",Nx = 128):
    # max_iter = 400000
    dt =  2.5e-5
    dt_out = 10
    nx= int(phi_name.split("_")[1])
    # nx = 128
    # T_total = 10
    # # want t = 0, 2, 4, 6, 8, 10
    # timesteps = 0, 80000, 160000, 240000, 320000, 400000
    # # 80000 timesteps = 8000th matrix (every ten steps recorded); 0 included
    # for timepoint in [0,8000,16000,24000,32000,40000]:
    for timepoint in timepoints:

        print("Timepoint ",timepoint)
        tmp = read_chunk(phi_name, indir, timepoint = timepoint, delim=delim, rows_per_timepoint=Nx)
        # xx = np.linspace(0, 1 / 128 * (nx - 1), nx)
        normalize_phis = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1, vmax=1)
        s = sns.heatmap(
            tmp,
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
            f"{outdir}/{phi_name}_{timepoint*dt*dt_out:.2e}.png",
            bbox_inches="tight",
            pad_inches=0,
            dpi=300,
        )
        plt.close()

        #zoomed plot
        # s = sns.heatmap(
        #     # tmp[49:81,49:81],
        #     tmp[46:84,46:84],
        #     square=True,
        #     cmap=cm.RdBu_r,
        #     norm=normalize_phis,
        #     cbar=False,
        #     linewidths=0.0,
        # )
        # plt.xticks(ticks=[], labels=[])
        # plt.yticks(ticks=[], labels=[])
        # # plt.title(f"Time= {timepoint*dt}")
        # plt.tight_layout()
        # plt.savefig(
        #     f"{outdir}/{phi_name}_{timepoint*dt*dt_out:.2e}.png",
        #     bbox_inches="tight",
        #     pad_inches=0,
        #     dpi=300,
        # )
        # plt.close()


# indir = "/project/g_bme-janeslab/SarahG/julia_out/critical_radius_alt_IC"
indir = "/project/g_bme-janeslab/SarahG/julia_out/critical_radius_updated_IC"

outdir = f"{indir}/timepoint_plots"
timepoints = [0,8000,16000,24000,32000,40000]
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.118_eps_0.015009.txt", indir, outdir, timepoints = timepoints)
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.11625_eps_0.015009.txt", indir, outdir, timepoints = timepoints)

# plot_timepoint("phi_128_400000_1.0e-6__R0_0.115_eps_0.015009.txt", indir, outdir, timepoints = [0,2000,4000,6000,8000])
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.118_eps_0.015009.txt", indir, outdir, timepoints = [0,2000,4000,6000,8000])

#timepoints = 0, 0.01, 0.03, 0.1, 0.3, 1, 3, 10 
timepoints = [0, 40, 120, 400, 1200,4000,12000,40000]
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.11_eps_0.015009.txt", indir, outdir, timepoints = timepoints)
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.12_eps_0.015009.txt", indir, outdir, timepoints = timepoints)
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.12_eps_0.011257.txt", indir, outdir, timepoints = timepoints)
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.09_eps_0.011257.txt", indir, outdir, timepoints = timepoints)
plot_timepoint("phi_128_400000_1.0e-6__R0_0.25_eps_0.12007.txt", indir, outdir, timepoints = timepoints, Nx = 128)
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.06_eps_0.011257.txt", indir, outdir, timepoints = timepoints)
# plot_timepoint("phi_128_400000_1.0e-6__R0_0.1_eps_0.011257.txt", indir, outdir, timepoints = timepoints)


