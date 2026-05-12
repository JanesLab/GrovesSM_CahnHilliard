# %% SPINODAL DECOMPOSITION: Structure factor analysis
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib import font_manager
from matplotlib import rcParams

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft2, fftfreq
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit


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
phi_name_SAV = "SAV_MATLAB_2000_dt_5.50e-06_Nx_128_n_relax_4_dtout_1_phi.csv"

# %%
phi_SAV = np.genfromtxt(f"{indir_SAV}/{phi_name_SAV}", delimiter=",")

phi_SAV = phi_SAV.reshape(-1, 128, 128).transpose(1, 2, 0)

# %%
# indir_MG = f"/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/nonlinear_multigrid/julia_multigrid/manuscript_output/spinodal_smooth_relax_function/output"
phi_MG_name = "NMG_MATLAB_6000_dt_5.50e-06_Nx_128_n_relax_4_dtout_1_tol_1e-6phi.csv"
# phi_MG_name = "MG_6000_dt_5.5e-6_Nx_128_n_relax_4_eps_0.015009369912862116_phi.txt"
phi_MG = np.genfromtxt(f"{indir_MG}/{phi_MG_name}", delimiter=",")
phi_MG = phi_MG.reshape(-1, 128, 128).transpose(1, 2, 0)

# %%


class StructureFactorAnalyzer:
    """
    Compute structure factor S(k) and extract coarsening length scales.
    """

    def __init__(self, L, N):
        """
        Parameters
        ----------
        L : float
            Physical domain size (box is [0,L]² )
        N : int
            Number of grid points in each direction
        """
        self.L = L
        self.N = N
        self.dx = L / N

    def compute_structure_factor(self, phi):
        """
        Compute structure factor S(k) from phase field φ(x,y).

        Parameters
        ----------
        phi : ndarray (N, N)
            Phase field at a single time step

        Returns
        -------
        k : ndarray
            Wavenumber magnitudes (1D array)
        S_k : ndarray
            Structure factor (1D array, radially averaged)
        k_max : float
            Wavenumber of peak in S(k)
        l_char : float
            Characteristic length scale = 2π / k_max
        """

        # Remove mean from phase field
        phi_centered = phi - np.mean(phi)

        # 2D FFT
        phi_hat = fft2(phi_centered)

        # Power spectrum (magnitude squared)
        power = np.abs(phi_hat) ** 2

        # Shift so DC is at center
        power_shifted = np.fft.fftshift(power)

        # Create coordinate grid relative to center
        center = self.N // 2
        coords = np.arange(-center, center)
        yy, xx = np.meshgrid(coords, coords, indexing='ij')
        r_pix = np.sqrt(xx**2 + yy**2)

        # Bin power by radius (in pixel space)
        n_bins = self.N // 2
        radii = np.arange(n_bins, dtype=float)
        S_k = np.zeros(n_bins)

        for i in range(1, n_bins):
            # Annulus between r=i-0.5 and r=i+0.5 pixels
            mask = (r_pix >= i - 0.5) & (r_pix < i + 0.5)
            if np.any(mask):
                S_k[i] = np.mean(power_shifted[mask])

        # Convert pixel radius to wavenumber (in physical units)
        # Wavenumber spacing: dk = 2π/L
        # Pixel i corresponds to k = i * (2π/L) / (N/(2π))
        # Simpler: k = 2π * i / L (approximately, for large N)
        k = 2 * np.pi * radii / self.L

        # Find peak (skip very small k)
        skip_idx = max(2, int(0.02 * n_bins))
        idx_max = np.argmax(S_k[skip_idx:]) + skip_idx
        k_max = k[idx_max]

        # Length scale: l(t) = 2π / k_max
        l_char = 2 * np.pi / k_max if k_max > 0 else np.inf

        return k, S_k, k_max, l_char

    def analyze_series(self, phi_list, times=None):
        """
        Analyze a time series of phase fields.

        Parameters
        ----------
        phi_list : list of ndarray
            Phase field at successive times
        times : array-like, optional
            Time values. If None, uses indices.

        Returns
        -------
        dict with keys:
            't': times
            'k': wavenumber grid
            'S_k': list of structure factors
            'l': characteristic length scales
            'k_peak': peak wavenumbers
        """

        if times is None:
            times = np.arange(len(phi_list))
        times = np.asarray(times)

        l_list = []
        k_peak_list = []
        S_k_list = []
        k_vals = None

        for phi in phi_list:
            k, S_k, k_max, l_char = self.compute_structure_factor(phi)
            l_list.append(l_char)
            k_peak_list.append(k_max)
            S_k_list.append(S_k)
            if k_vals is None:
                k_vals = k

        return {
            't': times,
            'k': k_vals,
            'S_k': S_k_list,
            'l': np.array(l_list),
            'k_peak': np.array(k_peak_list),
        }


def power_law(t, a, n):
    """Power law: a * t^n"""
    return a * np.power(t, n)


def fit_exponent(t, l, t_min=None, t_max=None):
    """
    Fit l(t) ∝ t^n in log-log space.

    Parameters
    ----------
    t : ndarray
        Time points
    l : ndarray
        Length scales
    t_min, t_max : float, optional
        Fit window

    Returns
    -------
    dict with exponent, amplitude, R², fit info
    """

    # Filter to window
    if t_min is not None or t_max is not None:
        tmin = t_min if t_min is not None else t.min()
        tmax = t_max if t_max is not None else t.max()
        mask = (t >= tmin) & (t <= tmax)
    else:
        mask = np.ones(len(t), dtype=bool)

    t_fit = t[mask]
    l_fit = l[mask]

    # Remove invalid points
    valid = (t_fit > 0) & (l_fit > 0) & np.isfinite(l_fit)
    t_fit = t_fit[valid]
    l_fit = l_fit[valid]

    if len(t_fit) < 3:
        raise ValueError("Not enough valid points")

    # Log-log fit
    loglog_fit = np.polyfit(np.log10(t_fit), np.log10(l_fit), 1)
    exponent = loglog_fit[0]
    log_amplitude = loglog_fit[1]
    amplitude = 10 ** log_amplitude

    # R²
    yhat = log_amplitude + exponent * np.log10(t_fit)
    ss_res = np.sum((np.log10(l_fit) - yhat) ** 2)
    ss_tot = np.sum((np.log10(l_fit) - np.mean(np.log10(l_fit))) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0

    return {
        'exponent': exponent,
        'amplitude': amplitude,
        'r2': r2,
        't_fit': t_fit,
        'l_fit': l_fit,
        'log10_t_fit': np.log10(t_fit),
        'log10_l_fit': np.log10(l_fit),
        'log10_l_pred': yhat,
    }


# ============================================================================
# Plotting utilities
# ============================================================================

def plot_structure_factor_snapshots(analysis_result, n_snapshots=4, figsize=(14, 4)):
    """
    Plot S(k) at selected times.
    """

    times = analysis_result['t']
    k = analysis_result['k']
    S_k_list = analysis_result['S_k']

    # Select evenly-spaced snapshots
    if len(times) <= n_snapshots:
        indices = list(range(len(times)))
    else:
        indices = np.linspace(0, len(times)-1, n_snapshots, dtype=int)

    fig, axes = plt.subplots(1, len(indices), figsize=figsize)
    if len(indices) == 1:
        axes = [axes]

    for ax_idx, t_idx in enumerate(indices):
        ax = axes[ax_idx]
        S_k = S_k_list[t_idx]
        t_val = times[t_idx]

        # Plot S(k), excluding k=0
        ax.semilogy(k[1:], S_k[1:], 'o-', linewidth=2,
                    markersize=4, color='steelblue')
        ax.set_xlabel('Wavenumber k', fontsize=11)
        ax.set_ylabel('S(k)', fontsize=11)
        ax.set_title(f't = {t_val:.2e}', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3, which='both')
        ax.set_xlim(left=0)

    plt.tight_layout()
    return fig, axes


def plot_coarsening_law(t, l, t_min=None, t_max=None, figsize=(10, 7)):
    """
    Plot l(t) on log-log with power-law fit and theory curve.
    """

    fit_result = fit_exponent(t, l, t_min=t_min, t_max=t_max)

    fig, ax = plt.subplots(figsize=figsize)

    # All data
    ax.plot(t, l, 'o-', color='steelblue', linewidth=2, markersize=7,
            label='Measured l(t)', zorder=3)

    # Fit region
    t_fit = fit_result['t_fit']
    l_pred = 10 ** fit_result['log10_l_pred']
    exponent = fit_result['exponent']

    ax.plot(t_fit, l_pred, 's--', color='coral', linewidth=2.5, markersize=5,
            label=f"Fit: l ∝ t^{exponent:.4f}\n(R² = {fit_result['r2']:.5f})", zorder=1)

    # Theory: t^(1/3)
    # t_theory = np.logspace(np.log10(t_min), np.log10(t_max), 200)
    # Scale so it passes through approximate middle of data
    scale = np.median(l) / (np.median(t) ** (1/3))
    print(scale)
    print(t_fit)
    l_theory = scale * (t_fit ** (1/3))
    print(l_theory)
    ax.plot(t_fit, l_theory, color='green', linewidth=2.5, alpha=0.8,
            label='Theory: l ∝ t^(1/3)', zorder=2)

    ax.set_xlabel('Time t', fontsize=13, fontweight='bold')
    ax.set_ylabel('Characteristic length l(t)', fontsize=13, fontweight='bold')
    ax.set_title('Cahn-Hilliard Coarsening Dynamics',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11, loc='lower right', framealpha=0.95)
    ax.grid(True, alpha=0.35, which='both')

    # Add annotations
    textstr = f"Measured exponent: {exponent:.4f}\nLSV theory: 0.3333\nDeviation: {abs(exponent-1/3)/(1/3)*100:.1f}%"
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    return fig, ax, fit_result


def plot_phase_field_samples(phi_list, times=None, figsize=(12, 4)):
    """
    Show phase field at 3 time snapshots.
    """

    if times is None:
        times = np.arange(len(phi_list))

    # Select 3 snapshots
    n = len(phi_list)
    if n <= 3:
        indices = list(range(n))
    else:
        indices = [0, n//2, n-1]

    fig, axes = plt.subplots(1, len(indices), figsize=figsize)
    if len(indices) == 1:
        axes = [axes]

    vmin, vmax = -1, 1

    for ax_idx, i in enumerate(indices):
        ax = axes[ax_idx]
        phi = phi_list[i]
        t_val = times[i]

        im = ax.imshow(phi, cmap='RdBu_r', origin='lower',
                       vmin=vmin, vmax=vmax)
        ax.set_title(f't = {t_val:.2e}', fontsize=12, fontweight='bold')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.colorbar(im, ax=ax, label='φ')

    plt.tight_layout()
    return fig, axes


def plot_phi_cross_section(phi_list, times=None, y_index=None, figsize=(10, 6)):
    """
    Plot φ vs x at a fixed y-coordinate for 3 time snapshots.

    Parameters
    ----------
    phi_list : list of ndarray
        Phase field at successive times (each is N×N)
    times : array-like, optional
        Time values
    y_index : int, optional
        y-index to extract (default: middle, N/2)
    figsize : tuple
        Figure size

    Returns
    -------
    fig, ax
    """

    if times is None:
        times = np.arange(len(phi_list))

    # Get N from first phi
    N = phi_list[0].shape[0]

    # Default to middle of domain
    if y_index is None:
        y_index = N // 2

    # Select 3 snapshots
    n = len(phi_list)
    if n <= 3:
        indices = list(range(n))
    else:
        indices = [0, n//2, n-1]

    fig, ax = plt.subplots(figsize=figsize)

    colors = plt.cm.viridis(np.linspace(0, 1, len(indices)))

    for idx_num, i in enumerate(indices):
        phi = phi_list[i]
        t_val = times[i]

        # Extract cross-section at y = y_index
        phi_slice = phi[y_index, :]
        x = np.arange(N)

        ax.plot(x, phi_slice, 'o-', linewidth=2.5, markersize=6,
                color=colors[idx_num], label=f't = {t_val:.2e}', alpha=0.8)

    ax.set_xlabel('x', fontsize=12, fontweight='bold')
    ax.set_ylabel('φ(x, y=' + str(y_index) + ')',
                  fontsize=12, fontweight='bold')
    ax.set_title('Phase Field Cross-Section', fontsize=13, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, N-1)

    plt.tight_layout()
    return fig, ax


# %%
L = 1
N = 128
phi_list, times = [], []

for i in range(phi_MG.shape[2]):
    phi_list.append(phi_MG[:, :, i])
times = np.arange(phi_MG.shape[2]) * 10.0  #
print(
    f"    Generated {len(phi_list)} snapshots over t ∈ [{times[0]:.2f}, {times[-1]:.2f}]"
)

# %%
# Analyze
print("Computing structure factor S(k,t)...")
analyzer = StructureFactorAnalyzer(L=L, N=N)
result = analyzer.analyze_series(phi_list, times=times)
print(
    f"    Length scales range: l(t) ∈ [{result['l'].min():.3f}, {result['l'].max():.3f}]"
)

# %%

# Fit
print("\n[3] Fitting coarsening exponent...")
# Use middle 60% of data to avoid transient and saturation
# t_min = times[int(0.2 * len(times))]
# t_max = times[int(0.8 * len(times))]
t_min = times[int(0.0 * len(times))]
t_max = times[-1]
# t_min = times[len(times)//3]          # 33%
# t_max = times[int(0.7*len(times))]    # 70%
fit = fit_exponent(result['t'], result['l'], t_min=t_min, t_max=t_max)

print(f"    Exponent (fit):    {fit['exponent']:.6f}")
print(f"    Exponent (theory): 0.333333")
print(
    f"    Error:             {abs(fit['exponent'] - 1/3) / (1/3) * 100:.2f}%"
)
print(f"    Amplitude:         {fit['amplitude']:.6f}")
print(f"    R² quality:        {fit['r2']:.8f}")
print(f"    Fit window:        t ∈ [{t_min:.3f}, {t_max:.3f}]")

# %%
# Plots
print("\n[4] Generating plots...")

fig1, _ = plot_structure_factor_snapshots(result, n_snapshots=3)
fig1.savefig('./structure_factor_results/s_k_evolution.png',
             dpi=150,
             bbox_inches='tight')
print("    ✓ Saved: s_k_evolution.png")
# %%
fig2, _, _ = plot_coarsening_law(result['t'],
                                 result['l'],
                                 t_min=t_min,
                                 t_max=t_max)
fig2.savefig('./structure_factor_results/coarsening_law.png',
             dpi=150,
             bbox_inches='tight')
print("    ✓ Saved: coarsening_law.png")
# %%
fig3, _ = plot_phase_field_samples(phi_list, times=times)
fig3.savefig('./structure_factor_results/phase_field_evolution.png',
             dpi=150,
             bbox_inches='tight')
print("    ✓ Saved: phase_field_evolution.png")


if abs(fit['exponent'] - 1 / 3) < 0.01:
    print("✓ SUCCESS: Exponent is consistent with t^(1/3) LSV scaling!")
elif abs(fit['exponent'] - 1 / 3) < 0.05:
    print("≈ MARGINAL: Exponent is close but shows some deviation.")
    print("  Check transient regime and domain saturation effects.")
else:
    print("✗ FAILURE: Exponent significantly deviates from t^(1/3).")
    print("  Likely issues:")
    print("    - Too much numerical dissipation or coarse grid")
    print("    - Data dominated by transient or saturation regime")
    print("    - Non-conservative dynamics (check model type)")


# %%
fig1, _ = plot_structure_factor_snapshots(result, n_snapshots=8)

# %%
fig2, _, _ = plot_coarsening_law(result['t'],
                                 result['l'],
                                 t_min=t_min,
                                 t_max=t_max)

# %%
fig4, ax4 = plot_phi_cross_section(phi_list, times=times, y_index=64)
fig4.savefig('./structure_factor_results/phi_cross_section_y64.png',
             dpi=150,
             bbox_inches='tight')
print("    ✓ Saved: phi_cross_section_y64.png")
# %%
