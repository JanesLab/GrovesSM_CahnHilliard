# %%
from statsmodels.stats.diagnostic import lilliefors
from scipy import stats
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
plt.rcParams['pdf.use14corefonts'] = True
plt.rcParams['pdf.fonttype'] = 'TrueType'
# %%
# data = pd.read_csv("Job_specs.csv", sep=",", header=0, index_col=None)
data_rivanna = pd.read_csv("Job_specs_Rivanna.csv",
                           sep=",", header=0, index_col=None)

# data['comp'] = "local"
data_rivanna['comp'] = "rivanna"

# %%
for length in [20, 200]:
    for i, r in data_rivanna.loc[data_rivanna['t_iter'] == length].iterrows():
        new_r = r.copy()
        new_r['t_iter'] = new_r['t_iter'] * 2000//length
        new_r['elapsed_time(s)'] = new_r['elapsed_time(s)'] * 2000//length
        new_r['comp'] = "rivanna_extrap"
        data_rivanna.loc[data_rivanna.shape[0]+1] = new_r

# %%
# all_data = pd.concat([data, data_rivanna], join='outer', ignore_index=True)
all_data = data_rivanna.copy()
# %%
all_data = all_data.loc[all_data["t_iter"] == 2000]
all_data = all_data.loc[all_data['method'] != "FD"]
all_data = all_data.loc[all_data['comp'] != "local"]

# %% Check if all expected cases ran on Rivanna
all_data = all_data.sort_values(
    by=['method', 'language', 'GridSize', 'print', 'boundary', 'IC_percent_+1', 'dt_out'])
for language in all_data['language'].unique():
    for method in all_data['method'].unique():
        for GridSize in all_data['GridSize'].unique():
            for bc in all_data['boundary'].unique():
                for IC in all_data['IC_percent_+1'].unique():
                    for print_data in all_data['print'].unique():
                        # print(bc, method, GridSize, language, IC)
                        if all_data.loc[(all_data["GridSize"] == GridSize) &
                                        (all_data["boundary"] == bc) &
                                        (all_data["method"] == method) &
                                        (all_data["language"] == language) &
                                        (all_data["IC_percent_+1"] == IC) &
                                        (all_data["print"] == print_data)].shape[0] == 0:
                            print(
                                f"Missing {language} {GridSize} {bc} {print_data} {method} {IC}")
                        elif all_data.loc[(all_data["GridSize"] == GridSize) &
                                          (all_data["boundary"] == bc) &
                                          (all_data["method"] == method) &
                                          (all_data["language"] == language) &
                                          (all_data["IC_percent_+1"] == IC) &
                                          (all_data["print"] == print_data)].shape[0] > 1:

                            print(
                                f"Duplicated: {language} {GridSize} {bc} {print_data} {method} {IC}")
                            print(all_data.loc[(all_data["GridSize"] == GridSize) &
                                               (all_data["boundary"] == bc) &
                                               (all_data["method"] == method) &
                                               (all_data["language"] == language) &
                                               (all_data["IC_percent_+1"] == IC) &
                                               (all_data["print"] == print_data)].index)
# (all_data.groupby(['language', 'method', 'GridSize', 'print', 'boundary',
#  'IC_percent_+1']).count()['date']).to_csv("Job_specs_Rivanna_counts.csv")

# output.403923 Missing Julia NMG 512 neumann 75p False

# %%
# if duplicated, keep the later one
all_data = all_data.sort_values(by=['date'])
all_data = all_data.drop_duplicates(
    subset=['language', 'method', 'GridSize', 'print', 'boundary', 'IC_percent_+1'], keep='last')

# %%
all_data = all_data.loc[(all_data["print"] == False)].reset_index()
# all_data.to_csv("Job_specs_Rivanna_cleaned.csv", index=False)

# %% add in Cython data
cython_data = pd.read_csv("Job_specs_Cython.csv",
                          sep=",", header=0, index_col=0)
cython_data['comp'] = "cython"
for length in [20, 200]:
    for i, r in cython_data.loc[cython_data['t_iter'] == length].iterrows():
        new_r = r.copy()
        new_r['t_iter'] = new_r['t_iter'] * 2000//length
        new_r['elapsed_time(s)'] = new_r['elapsed_time(s)'] * 2000//length
        new_r['comp'] = "rivanna_extrap_cython"
        cython_data.loc[cython_data.shape[0]+1] = new_r
cython_data = cython_data.loc[cython_data["t_iter"] == 2000]
# cython_data['language'] = "Cython"
# rename columns to match all_data
cython_data = cython_data.rename(columns={
    'GridSize': 'GridSize',
    'boundary': 'boundary',
    'method': 'method',
    'print': 'print',
    'note': 'IC_percent_+1',
    'elapsed_time(s)': 'elapsed_time(s)',
})
# %%
all_data = pd.concat([all_data, cython_data], join='outer', ignore_index=True)
print(all_data)

# %% compare average time for NMG, 128, periodic, no print, all languages, with and without Cython
subset_no_cython = all_data.loc[(all_data["GridSize"] == 128)
                                & (all_data["method"] == "NMG") &
                                (all_data['comp'] == "rivanna_extrap")]
subset_cython = all_data.loc[(all_data["GridSize"] == 128)
                             & (all_data["method"] == "NMG") &
                             (all_data['comp'] == "rivanna_extrap_cython")]

# compare each condition separately
for IC in all_data['IC_percent_+1'].unique():
    for BC in all_data['boundary'].unique():
        no_cython_time = subset_no_cython.loc[subset_no_cython['IC_percent_+1']
                                              == IC]['elapsed_time(s)'].mean()
        cython_time = subset_cython.loc[subset_cython['IC_percent_+1']
                                        == IC]['elapsed_time(s)'].mean()
        print(f"{IC} NMG 128 {BC} no print: No Cython: {no_cython_time:.2f} seconds, With Cython: {cython_time:.2f} seconds, Speedup: {no_cython_time/cython_time:.2f}x")

# max vs min speedup
# %% FIGURE 2B and 2C: gridsize 128, no print, both BC, all languages, NMG  or SAV only
GridSize = 128
method = "NMG"


def plot_fig2(all_data, method):
    fig, ax = plt.subplots(1, 1, figsize=(4, 4))
    g = sns.barplot(
        all_data.loc[(all_data["GridSize"] == GridSize) &
                     (all_data["method"] == method) &
                     (all_data["print"] == False) &
                     (all_data['comp'] != "rivanna_extrap_cython")],
        y="elapsed_time(s)",
        x="language",
        hue="boundary",
        hue_order=["periodic", "neumann"],
        order=["Python", "MATLAB", "Julia"],
        errorbar=None,
        legend=False
        # log=True
        # palette="Set2"
    )
    sns.swarmplot(
        all_data.loc[(all_data["GridSize"] == GridSize) &
                     (all_data["method"] == method) &
                     (all_data["print"] == False)],
        y="elapsed_time(s)",
        x="language",
        hue="boundary",
        hue_order=["periodic", "neumann"],
        order=["Python", "MATLAB", "Julia"],
        dodge=True,
        palette='dark:k',
        legend=False
        # log=True
        # palette="Set2"
    )
    plt.ylim(1, 1e6)
    g.figure.get_axes()[0].set_yscale('log')
    plt.suptitle(
        f"Elapsed Time for {GridSize}x{GridSize} Grid Size, 2000 Iterations, {method}", y=1.)
    plt.xlabel("Solver")
    plt.ylabel("Elapsed Time (seconds)")
    plt.tight_layout()
    return fig, ax


# method = "SAV"
# fig, ax = plot_fig2(all_data, method)
# ax.yaxis.tick_right()
# ax.yaxis.set_label_position("right")  # move the label too

# # Hide top and left spines
# ax.spines['left'].set_visible(False)
# ax.spines['top'].set_visible(False)
# plt.tight_layout()

# plt.show()
# plt.savefig(
# f"./output/both_bc_compare_runtime_{GridSize}_{method}_no_print_Figure_2B.pdf"
# )

method = "NMG"
fig, ax = plot_fig2(all_data, method)
# Hide top and right spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.savefig(
    f"./output/both_bc_compare_runtime_{GridSize}_{method}_no_print_Figure_2C_with_Cython.pdf")
plt.show()

plt.close()
# %% compare grid sizes
GridSizes = [512, 256, 128, 64]
print_data = False
# Create color palette: dark to light for each GridSize
default_colors = sns.color_palette()  # seaborn default
blue_base = default_colors[0]   # typically blue
orange_base = default_colors[1]  # typically orange

blue_shades = sns.light_palette(
    blue_base, n_colors=len(GridSizes)+1, reverse=True)
orange_shades = sns.light_palette(orange_base,
                                  n_colors=len(GridSizes)+1,
                                  reverse=True)
gray_shades = sns.light_palette(
    "black", n_colors=len(GridSizes)+1, reverse=True)

# palette_periodic = sns.light_palette("blue", len(GridSizes)+1)[::-1]
# palette_neumann = sns.light_palette("orange", len(GridSizes)+1)[::-1]
for i, method in enumerate(["NMG", "SAV"]):
    fig, ax = plt.subplots(figsize=(4, 4))

    for j, gr in enumerate(GridSizes):
        # Filter by GridSize and Method
        subset = all_data.loc[(all_data["GridSize"] == gr)
                              & (all_data["method"] == method) &
                              (all_data["print"] == False)]

        grid_palette = {
            "periodic": blue_shades[j],
            "neumann": orange_shades[j]
        }

        gray_palette = {"periodic": gray_shades[j], "neumann": gray_shades[j]}
        # Plot this GridSize on top of previous ones
        sns.barplot(
            data=subset,
            x="language",
            y="elapsed_time(s)",
            hue="boundary",
            hue_order=["periodic", "neumann"],
            order=["Python", "MATLAB", "Julia"],
            dodge=True,
            ax=ax,
            palette=grid_palette,  # ✅ This is now a dict, not a Series
            errorbar=None,
            zorder=i,  # optional for drawing order control,
            legend=False)
        sns.swarmplot(
            data=subset,
            x="language",
            y="elapsed_time(s)",
            hue="boundary",
            hue_order=["periodic", "neumann"],
            order=["Python", "MATLAB", "Julia"],
            dodge=True,
            # palette=gray_palette,
            palette="dark:k",
            size=4,
            ax=ax,
            # errorbar=None,
            zorder=i,  # optional for drawing order control,
            legend=False)
    ax.set_yscale("log")
    ax.set_title(f"{method}")
    ax.set_xlabel("Solver")
    ax.set_ylabel("Elapsed Time (seconds)")
    if method == "SAV":
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")  # move the label too

        # Hide top and left spines
        ax.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
    else:
        # Hide top and right spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
    plt.ylim(1, 1e7)
    plt.tight_layout()
    # plt.show()
    plt.savefig(f"./output/{method}_no_print_Figure_S2_gridsizes.pdf")
    plt.close()


# %% FIGURE 2A: IC and endpoints for periodic and neumann

indir = "/Users/smgroves/Documents/GitHub/CHsolvers_package/output/output_Rivanna_Figure_2"
IC = "50p"
phi_name_MG_periodic = f"NMG_Julia_2000_dt_5.50e-06_Nx_128_periodic_dtout_10{IC}_phi.csv"
phi_MG_p = np.genfromtxt(
    f"{indir}/{phi_name_MG_periodic}",
    delimiter=",",
)
phi_MG_p = phi_MG_p.reshape(-1, 128, 128).transpose(1, 2, 0)

phi_name_MG_neumann = f"NMG_Julia_2000_dt_5.50e-06_Nx_128_neumann_dtout_10{IC}_phi.csv"
phi_MG_n = np.genfromtxt(
    f"{indir}/{phi_name_MG_neumann}",
    delimiter=",",
)
phi_MG_n = phi_MG_n.reshape(-1, 128, 128).transpose(1, 2, 0)

# %% save individual plots

# timepoints = [0, 10, 20, 100, 1000, 2000]
timepoints = [0, 200]
dt_out = 10
dt = 5.5e-6
for bc in ['periodic']:
    for timepoint in timepoints:
        normalize_phis = mcolors.TwoSlopeNorm(vcenter=0, vmin=-1, vmax=1)
        if bc == "periodic":
            phi_MG = phi_MG_p
            title = "Periodic"
        else:
            phi_MG = phi_MG_n
            title = "Neumann"

        s = sns.heatmap(
            phi_MG[:, :, timepoint],
            square=True,
            cmap=cm.RdBu_r,
            norm=normalize_phis,
            cbar=False,
            linewidths=0.0,
        )
        plt.xticks(ticks=[], labels=[])
        plt.yticks(ticks=[], labels=[])
        # plt.title(f"Time= {timepoint*dt*dt_out}, {title} BC")
        plt.tight_layout()
        plt.savefig(
            f"{indir}/NMG_Julia_2000_dt_5.5e-6_t_{title}_{IC}_{timepoint*dt*dt_out:.2e}.pdf",
            bbox_inches="tight",
            pad_inches=0,
            dpi=300,
        )
        plt.close()

# %% Statistical test comparisons: normality tests
GridSize = 128

df = all_data.loc[(all_data["GridSize"] == GridSize) &
                  (all_data["print"] == False)].reset_index()


# %%
# Log transform all the simulations in 2B, subtract the mean of each group, then qq plot the mean-centered data.


def log_transform_and_center(df):
    df['log_elapsed_time'] = np.log10(df['elapsed_time(s)'])
    grouped = df.groupby(['language', 'method', 'boundary'])
    df['mean_log_elapsed_time'] = grouped['log_elapsed_time'].transform('mean')
    df['centered_log_elapsed_time'] = df['log_elapsed_time'] - \
        df['mean_log_elapsed_time']
    return df


df = log_transform_and_center(df)
# %%
# Create a QQ plot for each pair across method
a = df.loc[df['method'] == 'NMG', 'centered_log_elapsed_time']
b = df.loc[df['method'] == 'SAV', 'centered_log_elapsed_time']
percs = np.linspace(0, 100, 21)
qn_a = np.percentile(a, percs)
qn_b = np.percentile(b, percs)

plt.plot(qn_a, qn_b, ls="", marker="o")
plt.plot([-.2, .2], [-.2, .2], color='red', ls='--')
plt.xlabel("Mean-Centered Log-transformed NMG Elapsed Time Quantiles")
plt.ylabel("Mean Centered Log-transformed SAV Elapsed Time Quantiles")
plt.title("QQ Plot of NMG vs SAV Elapsed Time")

# %%

# 2. Lillifors Test
lilliefors_test = lilliefors(a.values - b.values)
print("\nLilliefors Test:")
print("Statistic:", lilliefors_test[0])
print("P-value:", lilliefors_test[1])

# 3. Jarque-Bera Test
jarque_bera_test = stats.jarque_bera(a.values - b.values)
print("\nJarque-Bera Test:")
print("Statistic:", jarque_bera_test.statistic)
print("P-value:", jarque_bera_test.pvalue)

# 4. Anderson-Darling Test
anderson_darling_test = stats.anderson(a.values - b.values)
print("\nAnderson-Darling Test:")
print("Statistic:", anderson_darling_test.statistic)
print("Critical values:", anderson_darling_test.critical_values)
print("Significance levels:", anderson_darling_test.significance_level)

# %% compare NMG vs FD_IE for neumann and periodic BC, 128, no print, MATLAB
# neumann then periodic
NMG_ex = [263.2739, 435.1856]
FD_IE_ex = [415.4461, 806.8495]
labels = ['Neumann', 'Periodic']
x = np.arange(len(labels))
width = 0.35
fig, ax = plt.subplots(figsize=(3, 3))
rects1 = ax.bar(x - width/2, NMG_ex, width, label='NMG')
rects2 = ax.bar(x + width/2, FD_IE_ex, width, label='FD_IE')
ax.set_ylabel('Elapsed Time (seconds)')
# ax.set_title('Elapsed Time by Method and Boundary Condition')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

plt.ylim(1e2, 1e3)
plt.yscale('log')
plt.tight_layout()
plt.savefig(f"./output/NMG_vs_FD_IE_neumann_periodic_128_no_print_MATLAB.pdf")
plt.show()

# %%
