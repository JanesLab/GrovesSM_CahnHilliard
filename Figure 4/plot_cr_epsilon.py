# %%
# Plot relationship between critical radius and epsilon values for a given alpha.
# This gives a line plot that allows us to approximate the epsilon value we should use to get a critical radius equal to the CPC critical radius from images.
import scipy.optimize
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# plt.rcParams["font.family"] = "Arial"
plt.rcParams['pdf.use14corefonts'] = True
# %%
########################################
# Trend of R0 vs equilibrium radii
########################################

# Plot the final equilibrium radius for a given alpha and epsilon for various R0. We want to see if the relationship
# between critical eq radius and R0 is linear or not, to see if the cases that grow from R0 to critical eq radius
# are converging to some critical eq radius as the R0 approaches the critical initial radius.
# indir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output"
# indir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/radii_lineplots_kymographs/alt_IC_periodic_BC_split_droplet"
# # alpha = "0.5"
# epsilon = "0.011257"
# df = pd.read_csv(
#     f"{indir}/radius_0.5_level_set_epsilon_{epsilon}_twohalves.txt",
#     header=0,
#     index_col=None,
# )
# print(df.head())


# wide_df = df.pivot(index='R0', columns='time', values='radius')
# # wide_df = df.pivot_table(values="radius", index="R0", columns="time")

# x = []
# y = []
# for i, r in wide_df.iterrows():
#     if r.hasnans:
#         pass
#     else:
#         end_idx = r.last_valid_index()
#         y.append(r[end_idx])
#         x.append(i)

# xs = np.array(x)
# ys = np.array(y)
# coef = np.polyfit(xs, ys, 1)
# poly1d_fn = np.poly1d(coef)
# # poly1d_fn is now a function which takes in x and returns an estimate for y
# f, ax = plt.subplots()
# plt.plot(xs, ys, "o", xs, poly1d_fn(x), "--")
# plt.text(
#     0.95,
#     0.1,
#     f"y = {round(coef[0],3)}x+ {round(coef[1],3)}",
#     horizontalalignment="right",
#     verticalalignment="center",
#     transform=ax.transAxes,
# )
# plt.xlabel("R0")
# plt.ylabel("Final (Equilibrium) radius at T=10")
# # plt.title(f"Epsilon: {epsilon}, alpha: {alpha}")
# # plt.savefig(
# #     f"{indir}/critical_radius/alpha_{alpha}/final_radius_vs_R0_eps_{epsilon}.pdf"
# # )
# plt.show()
# print(y[0])
# %%
# import scipy.optimize
# xs = np.array(x)
# ys = np.array(y)
# def h2l(x, m, t, b):
#     return m * np.exp(t * x) + b
# # perform the fit
# p0 = (1, 0.5, -1) # start with values near those we expect
# params, cv = scipy.optimize.curve_fit(h2l, xs, ys, p0)
# m, t, b = params
# sampleRate = 20_000 # Hz
# tauSec = (1 / t) / sampleRate

# # determine quality of the fit
# squaredDiffs = np.square(ys - h2l(xs, m, t, b))
# squaredDiffsFromMean = np.square(ys - np.mean(ys))
# rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
# print(f"R² = {rSquared}")

# # plot the results
# plt.plot(xs, ys, '.', label="data")
# plt.plot(xs, h2l(xs, m, t, b), '--', label="fitted")
# plt.title("Fitted Exponential Curve")


# # inspect the parameters
# print(f"Y = {m} * e^(-{t} * x) + {b}")
# print(f"Tau = {tauSec * 1e6} µs")


# %%
# ########################################
# # all alpha
# ########################################
# df = pd.read_csv(
#     "/nonlinear_multigrid/julia_multigrid/manuscript_output/critical_radius/critical_radii_epsilon.csv",
#     header=0,
#     index_col=None,
# )

# print(df.head())

# sns.lineplot(
#     data=df,
#     y="critical equilibrium radius",
#     x="epsilon",
#     hue="alpha",
#     linestyle="-",
#     markers="o",
# )
# plt.show()

# %%
# ########################################
# # only alpha = -0.5, with max and min
# ########################################
# df = pd.read_csv(
#     "/nonlinear_multigrid/julia_multigrid/manuscript_output/critical_radius/critical_radii_epsilon_-0.5.csv",
#     header=0,
#     index_col=None,
# )

# print(df.head())
# y = "critical equilibrium radius (min)"
# sns.lineplot(data=df, y=y, x="epsilon", marker="o")
# plt.title(f"Critical radius vs. epsilon \n {y}, alpha = -0.5")
# plt.savefig(f"{y}_vs_epsilon.png")
# plt.show()

# %%

# plt.figure()
# plt.plot(
#     df["epsilon"],
#     df["critical equilibrium radius (min)"],
#     label="Min (inflection point)",
#     marker="o",
# )
# plt.plot(
#     df["epsilon"],
#     df["critical equilibrium radius (max)"],
#     label="Max (equilibrium radius)",
#     marker="o",
# )
# plt.legend(loc="upper right")
# plt.title("Critical radius vs. epsilon, alpha = -0.5")
# plt.xlabel("Epsilon")
# plt.ylabel("Critical Radius")
# plt.show()
# xs = np.array(df["epsilon"].values[1:4])
# ys = np.array(df["critical equilibrium radius (min)"].values[1:4])
# coef = np.polyfit(xs, ys, 1)
# poly1d_fn = np.poly1d(coef)

# xs_max = np.array(df["epsilon"].values)
# ys_max = np.array(df["critical equilibrium radius (max)"].values)
# coef_max = np.polyfit(xs_max, ys_max, 1)
# poly1d_fn_max = np.poly1d(coef_max)

# # poly1d_fn is now a function which takes in x and returns an estimate for y
# f, ax = plt.subplots()
# plt.plot(xs, ys, "o", label="Minimum (inflection points)")
# plt.plot([0.030019, 0.09, 0.15], poly1d_fn(
#     [0.030019, 0.09, 0.15]), "-", c="#1f77b4")
# plt.plot(xs_max, ys_max, "o", label="Maximum ($R_{eq}$ minimum)")
# plt.plot(
#     [0.015009, 0.09, 0.15], poly1d_fn_max([0.015009, 0.09, 0.15]), "-", c="#ff7f0e"
# )
# plt.text(
#     0.99,
#     0.25,
#     f"y = {round(coef[0],3)}x+ {round(coef[1],3)}",
#     horizontalalignment="right",
#     verticalalignment="center",
#     transform=ax.transAxes,
#     c="#1f77b4",
# )
# plt.text(
#     0.99,
#     0.3,
#     f"y = {round(coef_max[0],3)}x+ {round(coef_max[1],3)}",
#     horizontalalignment="right",
#     verticalalignment="center",
#     transform=ax.transAxes,
#     c="#ff7f0e",
# )
# plt.axhline(
#     y=0.108, label="Experimental CPC $R_{critical}$", c="k", linestyle="--")
# plt.legend(loc="lower right")

# plt.title("Critical radius vs. epsilon, alpha = -0.5")
# plt.xlabel("Epsilon")
# plt.ylabel("Critical Radius")
# plt.savefig("Critical equilibrium radius (min and max)_vs_epsilon.png")

# # %%
# ########################################
# # all alpha, REUSE THIS ONE
# ########################################
# df = pd.read_csv(
#     "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output/critical_radius/critical_radii_epsilon copy.csv",
#     header=0,
#     index_col=None,
# )
# print(df.head())
# df_0 = df.loc[df["alpha"] == 0]
# y = "critical equilibrium radius (min)"
# sns.lineplot(
#     data=df_0,
#     y=y,
#     x="epsilon",
#     markers=True,
#     style="Nx",
#     hue="Nx",
#     palette="muted",
#     alpha=0.6,
# )
# plt.title(f"Critical radius vs. epsilon")
# plt.ylabel("Critical equilibrium radius")
# # plt.savefig(
# #     f"/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output/critical_radius/cr_vs_epsilon_alpha_0.pdf"
# # )
# # plt.close()
# plt.show()

# # %%
# df = pd.read_csv(
#     "critical_radii_epsilon copy.csv",
#     header=0,
#     index_col=None,
# )

# alpha = 0
# tmp = df.loc[df["alpha"] == alpha]
# # plt.figure()
# # plt.plot(tmp['epsilon'], tmp['critical equilibrium radius (min)'], label = "Min (inflection point)", marker = "o")
# # plt.plot(tmp['epsilon'], tmp['critical equilibrium radius (max)'], label = "Max (equilibrium radius)", marker = "o")
# # plt.legend(loc = "upper right")
# # plt.title(f"Critical radius vs. epsilon, alpha = {alpha}")
# # plt.xlabel("Epsilon")
# # plt.ylabel("Critical Radius")
# # plt.show()
# xs = np.array(tmp["epsilon"])  # [0:2])
# ys = np.array(tmp["critical equilibrium radius (min)"])  # [0:2])
# coef = np.polyfit(xs, ys, 1)
# poly1d_fn = np.poly1d(coef)

# # xs_max = np.array(tmp['epsilon'].values)
# # ys_max = np.array(tmp['critical equilibrium radius (max)'].values)
# # coef_max = np.polyfit(xs_max,ys_max,1)
# # poly1d_fn_max = np.poly1d(coef_max)

# # poly1d_fn is now a function which takes in x and returns an estimate for y
# f, ax = plt.subplots()
# plt.plot(xs, ys, "o")  # ,label = "Minimum (inflection points)")
# plt.plot([0, 0.09], poly1d_fn([0, 0.09]), "-", c="#1f77b4")
# # plt.plot(xs_max,ys_max, 'o', label = "Maximum ($R_{eq}$ minimum)")
# # plt.plot( [0, 0.09, 0.15], poly1d_fn_max([0, 0.09, 0.15]), '-', c = '#ff7f0e')
# plt.text(
#     0.99,
#     0.25,
#     f"y = {round(coef[0],3)}x+ {round(coef[1],3)}",
#     horizontalalignment="right",
#     verticalalignment="center",
#     transform=ax.transAxes,
#     c="#1f77b4",
# )
# # plt.text(.99,0.3, f"y = {round(coef_max[0],3)}x+ {round(coef_max[1],3)}",
# #          horizontalalignment='right',
# #       verticalalignment='center',
# #       transform = ax.transAxes, c = '#ff7f0e')
# plt.axhline(
#     y=0.054, label="Experimental CPC $R_{critical}$", c="k", linestyle="--")
# plt.legend(loc="lower right")

# plt.title(f"Critical radius vs. epsilon, alpha = {alpha}")
# plt.xlabel("Epsilon")
# plt.ylabel("Critical Radius")
# plt.show()
# plt.savefig(f"Critical equilibrium radius (min)_vs_epsilon_alpha_{alpha}.png")
# %% with hyperbolic to linear fit
########################################
# FINAL FIGURE CR vs E, FIGURE 3E
########################################

df = pd.read_csv(
    "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output/critical_radius/critical_radii_epsilon copy.csv",
    header=0,
    index_col=None,
)

alpha = 0
tmp = df.loc[df["alpha"] == alpha]
xs = np.array(tmp["epsilon"])  # [0:2])
ys = np.array(tmp["critical equilibrium radius (min)"])
# ys = np.array(tmp["critical initial radius"])  # [0:2])

print(df.head())


def h2l(x, m, t, b):
    #     return m * np.exp(t * x) + b
    # b(1).*(b(2).*xdata./(b(3) + xdata) + xdata);
    return m * (t * x / (b + x) + x)  # HYPERBOLIC FIT
    # return


# hyperbolic to linear
# perform the fit
p0 = (0, 0, 0)  # start with values near those we expect
params, cv = scipy.optimize.curve_fit(h2l, xs, ys, p0)
print(params)
# 1.06258065 0.06720503 0.00389349
m, t, b = params
# determine quality of the fit
squaredDiffs = np.square(ys - h2l(xs, m, t, b))
squaredDiffsFromMean = np.square(ys - np.mean(ys))
rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
print(f"H2L R² = {rSquared}")

# %% FIGURE 3E
# plot the results
f, ax = plt.subplots(figsize=(5, 4))

# fig = plt.figure(figsize = (5,4))
plt.text(
    0.95,
    0.024,
    f"R² = {round(rSquared,3)}",
    horizontalalignment="right",
    verticalalignment="center",
    transform=ax.transAxes,
)
# plt.plot(xs, ys, '.', label="Simulation results")
markers = {128: "o", 256: "^"}
plt.plot(
    np.linspace(0, 0.1),
    h2l(np.linspace(0, 0.1), m, t, b),
    "--",
    label="Fit",
    c="gray",
)
# sns.scatterplot(
#     data=tmp,
#     x="epsilon",
#     y="critical equilibrium radius (min)",
#     # hue="Nx",
#     palette=sns.color_palette("bright"),
#     edgecolor="k",
#     markers=markers,
#     style="Nx",
#     c="k",
# )
for cat, group in tmp.groupby("Nx"):
    ax.scatter(
        group["epsilon"],
        group["critical equilibrium radius (min)"],
        edgecolors="k",
        facecolors="none",
        marker=markers[cat],
        label=cat,
    )


print(h2l(0.0125, m, t, b))
plt.title("Hyperbolic-to-Linear Fit of\n Critical Radius vs Epsilon")
plt.xlabel(r"Epsilon ($ \epsilon $)")
plt.ylabel(r"Critical Equilibrium Radius ($R_c$)")
plt.legend()
plt.xlim(0, 0.1)
plt.ylim(0, 0.18)
plt.tight_layout()
# plt.savefig(
# f"Critical equilibrium radius_vs_epsilon_alpha_{alpha}_hyperlin_128_256_black_v2.pdf"
# )
# plt.close()
plt.show()

# %%
# FIGURE 4D
fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 0.06, 10000)
y = 3.2*h2l(np.linspace(0, 0.06, 10000), m, t, b)
plt.plot(
    x, y,
    "--",
    label=" H2L Simulation Fit",
    c="gray",
)
plt.ylabel(r"Critical Radius ($R_c$, $nm$)")
plt.xlabel(r"Epsilon ($ \epsilon $, nm)")
# ax.fill_between(x, y, where=(y <= .1), color='C1', alpha=0.3,
#                 interpolate=True)
# Mask values to ensure filling is within y1 and y2
# y1 and y2 come from CI of bootstrapping from 10 images (choose 5)
mask = (y >= .166) & (y <= .17)  # um values
y_fill = y[mask]
x_fill = x[mask]
ax.fill_betweenx(y_fill, 0, x_fill, color='gray', alpha=0.3,
                 interpolate=True, label="25-75% CI")

# mask2 = (x >= .015) & (x <= .02)
# y_fill2 = y[mask]
# x_fill2 = x[mask]
ax.fill_between(x_fill, 0, y_fill, color='gray', alpha=0.3, interpolate=True)

# convert ymax and xmax to 0-1, percentage of axis
# approx_Rc = 3.2*h2l(0.0067, m, t, b)
approx_e = 0.00676  # unitless value
plt.axvline(ymin=0,  ymax=(0.168-.1)/.1,
            x=0.00676, label="Experimental CPC $R_{critical}$", c="k", linestyle="--")
plt.axhline(xmin=0,  xmax=0.00676/0.015,
            y=0.168, c="k", linestyle="--")

plt.xlim(0, 0.015)
plt.ylim(0.1, 0.2)

# convert um to nm
plt.yticks(
    plt.yticks()[0][1:-1],
    [round(j * 1000, 3) for j in plt.yticks()[0][1:-1]],
    fontsize=8,
)

# convert unitless to nm
plt.xticks(
    plt.xticks()[0][1:-1],
    [round(j * 3200, 3) for j in plt.xticks()[0][1:-1]],
    fontsize=8,
)
plt.title(
    rf"HeLa; $R_c$= 168 nm, IQR = 166-170 nm\n $\epsilon$ = {round(3200*0.00676,2)} nm, IQR = {round(3200*x_fill.min(),2)}-{round(3200*x_fill.max(),2)} nm")
plt.legend()
plt.show()
# plt.savefig(
# f"Critical equilibrium radius_vs_epsilon_alpha_{alpha}_hyperlin_black_fill_experimental_bootstrap_nm_fixedx3200nm.pdf")


# %% MCF10A supplement
# FIGURE 4D
fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 0.06, 10000)
y = 3.2*h2l(np.linspace(0, 0.06, 10000), m, t, b)
plt.plot(
    x, y,
    "--",
    label=" H2L Simulation Fit",
    c="gray",
)
plt.ylabel(r"Critical Radius ($R_eq$, $nm$)")
plt.xlabel(r"Epsilon ($ \epsilon $, nm)")
# ax.fill_between(x, y, where=(y <= .1), color='C1', alpha=0.3,
#                 interpolate=True)
# Mask values to ensure filling is within y1 and y2
# y1 and y2 come from CI of bootstrapping from 10 images (choose 5)
mask = (y >= .1864) & (y <= .1922)
y_fill = y[mask]
x_fill = x[mask]
ax.fill_betweenx(y_fill, 0, x_fill, color='gray', alpha=0.3,
                 interpolate=True, label="25-75% CI")

# mask2 = (x >= .015) & (x <= .02)
# y_fill2 = y[mask]
# x_fill2 = x[mask]
ax.fill_between(x_fill, 0, y_fill, color='gray', alpha=0.3, interpolate=True)

# convert ymax and xmax to 0-1, percentage of axis
# approx_Rc = 3.2*h2l(0.0067, m, t, b)
approx_e = 0.00676
plt.axvline(ymin=0,  ymax=(0.1892-.1)/.1,
            x=0.0089, label="Experimental CPC $R_{eq}$", c="k", linestyle="--")
plt.axhline(xmin=0,  xmax=0.0089/0.015,
            y=0.1892, c="k", linestyle="--")

plt.xlim(0, 0.015)
plt.ylim(0.1, 0.2)

# convert um to nm
plt.yticks(
    plt.yticks()[0][1:-1],
    [round(j * 1000, 3) for j in plt.yticks()[0][1:-1]],
    fontsize=8,
)

plt.xticks(
    plt.xticks()[0][1:-1],
    [round(j * 3200, 3) for j in plt.xticks()[0][1:-1]],
    fontsize=8,
)
plt.legend()
plt.title(
    rf"MCF10A; $R_c$= 189.2 nm, IQR = 186.4-192.2 nm\n $\epsilon$ = {0.0089*3200} nm, IQR = {round(3200*x_fill.min(),2)}-{round(3200*x_fill.max(),2)} nm")
plt.show()
# plt.savefig(
# f"Critical equilibrium radius_vs_epsilon_alpha_{alpha}_hyperlin_black_fill_experimental_bootstrap_nm_MCF10A_fixed3200nm.pdf")
# print(x_fill)
# %% FIGURE S3C: multiple fits


def linFit(x, m, b):
    return m * x + b


def logFit(x, a, b):
    return a * np.log(x) + b


def hyperbolic(x, m, t, b):
    return m * (t * x / (b + x))  # HYPERBOLIC FIT
    # return


def cubic_root(x, a):
    return a * np.cbrt(x)


def powerFit(x, a, b):
    return a * np.power(x, b)


def calculate_bic(xs, ys, func, p0):
    """
    Calculate the best fit parameters and BIC for a given function.

    Parameters:
    xs (array): Independent variable data.
    ys (array): Dependent variable data.
    func (callable): The model function.
    p0 (list): Initial guess for parameters.

    Returns:
    dict: Dictionary containing best fit parameters, BIC, and residuals.
    """
    # Fit the function to the data
    params, cv = scipy.optimize.curve_fit(func, xs, ys, p0=p0)

    # Calculate residuals
    residuals = ys - func(xs, *params)

    # Sum of squared residuals
    ssr = np.sum(residuals**2)

    # Number of observations
    n = len(ys)

    # Number of parameters
    k = len(params)

    # Bayesian Information Criterion
    bic = n * np.log(ssr / n) + k * np.log(n)

    return {"best_fit_parameters": params, "bic": bic, "residuals": residuals}

# %%


initial_guess = [0.0, 0.0, 0.0]
results_H2L = calculate_bic(xs, ys, h2l, initial_guess)
print("H2L", results_H2L["bic"])
xfit = np.linspace(0, 0.1)
for fit in ["Linear", "Log", "Hyperbolic", "Power", "Cubic Root"]:
    print(fit)
    if fit == "Linear":
        initial_guess = [1.0, 0.0]
        results = calculate_bic(xs, ys, linFit, initial_guess)
        yfit = linFit(xfit, *results["best_fit_parameters"])
    elif fit == "Log":
        initial_guess = [1.0, 0.0]
        results = calculate_bic(xs, ys, logFit, initial_guess)
        yfit = logFit(xfit, *results["best_fit_parameters"])
    elif fit == "Hyperbolic":
        initial_guess = [1, 0.0, 0.0]
        results = calculate_bic(xs, ys, hyperbolic, initial_guess)
        yfit = hyperbolic(xfit, *
                          results["best_fit_parameters"])
    elif fit == "Cubic Root":
        initial_guess = [.1]
        results = calculate_bic(xs, ys, cubic_root, initial_guess)
        yfit = cubic_root(xfit, *
                          results["best_fit_parameters"])
    elif fit == "Power":
        initial_guess = [1.0, 1.0]
        results = calculate_bic(xs, ys, powerFit, initial_guess)
        yfit = powerFit(xfit, *results["best_fit_parameters"])

    print("BIC: ", results["bic"])
    print("Parameters: ", results["best_fit_parameters"])
    plt.figure(figsize=(4, 3))

    plt.plot(
        xfit,
        h2l(xfit, *results_H2L["best_fit_parameters"]),
        label=f"H2L Fit, BIC = {round(results_H2L['bic'],2)}",
    )
    plt.plot(
        xfit,
        yfit,
        label=f"{fit} Fit, BIC = {round(results['bic'],2)}",
    )
    markers = {128: "o", 256: "^"}
    sns.scatterplot(
        data=tmp,
        x="epsilon",
        y="critical equilibrium radius (min)",
        # hue="Nx",
        edgecolors="k",
        facecolors="none",
        markers=markers,
        style="Nx",
        alpha=1,
        zorder=10,
        linewidth=1
    )
    plt.xlim(0, 0.1)
    plt.ylim(0, 0.18)
    print(h2l(0.0125, m, t, b))

    plt.title("Different Fits of\n Critical Radius vs Epsilon")
    plt.xlabel("$\epsilon$")
    plt.ylabel("$R_{eq}$")
    plt.legend()
    # plt.savefig(
    #     f"Critical equilibrium radius_vs_epsilon_alpha_{alpha}_multi_fits_{fit}_vs_H2L.pdf"
    # )
    # plt.close()
    plt.show()

# %%

# initial_guess = [1.0, 0.0]
# results = calculate_bic(xs, ys, linFit, initial_guess)
# print("Linear", results["bic"])
# plt.plot(
#     np.linspace(0, 0.09),
#     linFit(np.linspace(0, 0.09), *results["best_fit_parameters"]),
#     # "--",
#     label=f"Linear Fit, BIC = {round(results['bic'],2)}",
#     c=sns.color_palette()[0],
#     # alpha=0.6,
# )


# initial_guess = [1, 0.0, 0.0]
# results = calculate_bic(xs, ys, hyperbolic, initial_guess)
# print("Hyperbolic", results["bic"])
# plt.plot(
#     np.linspace(0, 0.09),
#     hyperbolic(np.linspace(0, 0.09), *results["best_fit_parameters"]),
#     # "--",
#     label=f"Hyperbolic Fit, BIC = {round(results['bic'],2)}",
#     c=sns.color_palette()[2],
#     # alpha=0.6,
# )

# initial_guess = [1.0, 0.0]
# results = calculate_bic(xs, ys, logFit, initial_guess)
# print("Log", results["bic"])
# plt.plot(
#     np.linspace(0, 0.09),
#     logFit(np.linspace(0, 0.09), *results["best_fit_parameters"]),
#     # "--",
#     label=f"Log Fit, BIC = {round(results['bic'],2)}",
#     c=sns.color_palette()[3],
#     # alpha=0.6,
# )

# markers = {128: "o", 256: "^"}

# sns.scatterplot(
#     data=tmp,
#     x="epsilon",
#     y="critical equilibrium radius (min)",
#     # hue="Nx",
#     palette=sns.color_palette("bright"),
#     edgecolors="k",
#     facecolors="none",
#     markers=markers,
#     style="Nx",
#     alpha=1,
#     zorder=10,
#     linewidth=1
# )

# # convert um to nm
# plt.yticks(
#     plt.yticks()[0][1:-1],
#     [round(j * 1000, 3) for j in plt.yticks()[0][1:-1]],
#     fontsize=8,
# )

# plt.xticks(
#     plt.xticks()[0][1:-1],
#     [round(j * 1000, 3) for j in plt.xticks()[0][1:-1]],
#     fontsize=8,
# )
# print(h2l(0.0125, m, t, b))
# plt.title("Different Fits of\n Critical Radius vs Epsilon")
# plt.xlabel("$\epsilon$ ($nm$)")
# plt.ylabel("$R_{eq}$ ($nm$)")
# plt.legend()
# # plt.savefig(
# #     f"Critical equilibrium radius_vs_epsilon_alpha_{alpha}_multi_fits_128_256_v2.pdf"
# # )
# # plt.close()
# plt.show()


# # %% FIGURE 3
# tmp = df.loc[df["alpha"] == 0]

# fig = plt.figure(figsize=(5, 4))


# def crit_init_r_theory(e, V=1):
#     return np.cbrt((np.sqrt(6) / (8 * np.pi)) * V * e)


# plt.rcParams["mathtext.fontset"] = "cm"


# f, ax = plt.subplots(figsize=(5, 4))

# plt.plot(
#     np.linspace(0, 0.10),
#     crit_init_r_theory(np.linspace(0, 0.10)),
#     "--",
#     label=f"Theory",
#     c="grey",
#     alpha=0.6,
# )

# markers = {128: "o", 256: "^"}

# # sns.scatterplot(
# #     data=tmp,
# #     x="epsilon",
# #     y="critical initial radius",
# #     # hue="Nx",
# #     palette=sns.color_palette("bright"),
# #     edgecolor="k",
# #     markers=markers,
# #     style="Nx",
# # )
# for cat, group in tmp.groupby("Nx"):
#     ax.scatter(
#         group["epsilon"],
#         group["critical initial radius"],
#         edgecolors="k",
#         facecolors="none",
#         marker=markers[cat],
#         label=cat,
#     )
# plt.legend()
# plt.xlim(0, 0.10)
# plt.ylim(0, 0.25)
# plt.title("Critical Initial Radius vs Epsilon")
# plt.xlabel(r"Epsilon ($ \epsilon $)")
# plt.ylabel(r"Critical Initial Radius ($R_0$)")
# plt.tight_layout()
# plt.savefig(f"Critical initial radius_vs_epsilon_w_theory_128_256_black_v2.pdf")
# plt.close()
# plt.show()
# %% power law for Rc values (0.168, IQR = 0.166-0.170)
# power law fit from above
a = 0.4586624
exp = 0.43996249
# ax^b = y
# y/a = x^b
# x = (y/a)^(1/b)


exp = 0.43996249


def power_law_inverse(y, a, exp):
    return (y / a) ** (1 / exp)


print(power_law_inverse(0.168/3.2, a, exp))
print(power_law_inverse(0.166/3.2, a, exp))
print(power_law_inverse(0.170/3.2, a, exp))

# %%
# comparing H2L and power law
# run simulations with large epsilon to see which is fitting better:
# eps = 0.12, M = 64

print(h2l(0.12, m, t, b))  # 0.1966762832418493
print(powerFit(0.12, a, exp))  # 0.18045437984979126

# running simulations with the large epsilon (M = 64, Nx = 128) for R0 = 0.21, 0.2, 0.19, 0.18, 0.17


# %%
# Figure 4D Power Law
fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 0.06, 10000)
y = 3.2*powerFit(np.linspace(0, 0.06, 10000), a, exp)
plt.plot(
    x, y,
    "--",
    label=" Power Law Simulation Fit",
    c="gray",
)
plt.ylabel(r"Critical Radius ($R_c$, $nm$)")
plt.xlabel(r"Epsilon ($ \epsilon $, nm)")
# ax.fill_between(x, y, where=(y <= .1), color='C1', alpha=0.3,
#                 interpolate=True)
# Mask values to ensure filling is within y1 and y2
# y1 and y2 come from CI of bootstrapping from 10 images (choose 5)
mask = (y >= .166) & (y <= .17)  # um values
y_fill = y[mask]
x_fill = x[mask]
ax.fill_betweenx(y_fill, 0, x_fill, color='gray', alpha=0.3,
                 interpolate=True, label="25-75% CI")

# mask2 = (x >= .015) & (x <= .02)
# y_fill2 = y[mask]
# x_fill2 = x[mask]
ax.fill_between(x_fill, 0, y_fill, color='gray', alpha=0.3, interpolate=True)

# convert ymax and xmax to 0-1, percentage of axis
# approx_Rc = 3.2*h2l(0.0067, m, t, b)
approx_e = 0.00676  # unitless value
plt.axvline(ymin=0,  ymax=(0.168-.1)/.1,
            x=power_law_inverse(0.168/3.2, a, exp), label="Experimental CPC $R_{critical}$", c="k", linestyle="--")
plt.axhline(xmin=0,  xmax=power_law_inverse(0.168/3.2, a, exp)/0.015,  # from previous cell execution power_law_inverse(0.168/3.2, a, b)
            y=0.168, c="k", linestyle="--")

plt.xlim(0, 0.015)
plt.ylim(0.1, 0.2)

# convert um to nm
plt.yticks(
    plt.yticks()[0][1:-1],
    [round(j * 1000, 3) for j in plt.yticks()[0][1:-1]],
    fontsize=8,
)

# convert unitless to nm
plt.xticks(
    plt.xticks()[0][1:-1],
    [round(j * 3200, 3) for j in plt.xticks()[0][1:-1]],
    fontsize=8,
)
plt.title(
    rf"HeLa; $R_c$= 168 nm, IQR = 166-170 nm $\epsilon$ = {round(3200*power_law_inverse(0.168/3.2, a, exp),2)} nm, IQR = {round(3200*x_fill.min(),2)}-{round(3200*x_fill.max(),2)} nm")
plt.legend()
plt.show()

# %%
# %% MCF10A supplement POWER LAW
# FIGURE 4D
fig, ax = plt.subplots(1, 1)
x = np.linspace(0, 0.06, 10000)
y = 3.2*powerFit(np.linspace(0, 0.06, 10000), a, exp)
plt.plot(
    x, y,
    "--",
    label=" Power Law Simulation Fit",
    c="gray",
)
plt.ylabel(r"Critical Radius ($R_eq$, $nm$)")
plt.xlabel(r"Epsilon ($ \epsilon $, nm)")
# ax.fill_between(x, y, where=(y <= .1), color='C1', alpha=0.3,
#                 interpolate=True)
# Mask values to ensure filling is within y1 and y2
# y1 and y2 come from CI of bootstrapping from 10 images (choose 5)
mask = (y >= .1864) & (y <= .1922)
y_fill = y[mask]
x_fill = x[mask]
ax.fill_betweenx(y_fill, 0, x_fill, color='gray', alpha=0.3,
                 interpolate=True, label="25-75% CI")

# mask2 = (x >= .015) & (x <= .02)
# y_fill2 = y[mask]
# x_fill2 = x[mask]
ax.fill_between(x_fill, 0, y_fill, color='gray', alpha=0.3, interpolate=True)

# convert ymax and xmax to 0-1, percentage of axis
# approx_Rc = 3.2*h2l(0.0067, m, t, b)
approx_e = 0.00676
plt.axvline(ymin=0,  ymax=(0.1892-.1)/.1,
            x=power_law_inverse(0.1892/3.2, a, exp), label="Experimental CPC $R_{eq}$", c="k", linestyle="--")
plt.axhline(xmin=0,  xmax=power_law_inverse(0.1892/3.2, a, exp)/0.015,
            y=0.1892, c="k", linestyle="--")

plt.xlim(0, 0.015)
plt.ylim(0.1, 0.2)

# convert um to nm
plt.yticks(
    plt.yticks()[0][1:-1],
    [round(j * 1000, 3) for j in plt.yticks()[0][1:-1]],
    fontsize=8,
)

plt.xticks(
    plt.xticks()[0][1:-1],
    [round(j * 3200, 3) for j in plt.xticks()[0][1:-1]],
    fontsize=8,
)
plt.legend()
plt.title(
    rf"MCF10A; $R_c$= 189.2 nm, IQR = 186.4-192.2 nm $\epsilon$ = {round(power_law_inverse(0.1892/3.2, a, exp)*3200,3)} nm, IQR = {round(3200*x_fill.min(),2)}-{round(3200*x_fill.max(),2)} nm")
plt.show()
# plt.savefig(
# f"Critical equilibrium radius_vs_epsilon_alpha_{alpha}_hyperlin_black_fill_experimental_bootstrap_nm_MCF10A_fixed3200nm.pdf")
# print(x_fill)

# %%
