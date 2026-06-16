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

# Define model with FIXED exponent
def power_law_cubic_root(t, A):
    return A * t**(1/3)  # Exponent fixed at 1/3

def fit_theory_amplitude(t, l, t_min=None, t_max=None):
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
    # Fit (A is the only free parameter)
    popt, pcov = curve_fit(power_law_cubic_root, t_fit, l_fit)
    
    A = popt[0]
    A_err = np.sqrt(pcov[0, 0])
    return A, A_err

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
              label=f"Fit: l ∝ t^{exponent:.4f}\n(R² = {fit_result['r2']:.5f})", zorder=2)

    # Theory: t^(1/3)
    # t_theory = np.logspace(np.log10(t.min()), np.log10(t.max()), 200)
    # Scale so it passes through approximate middle of data

    # fit best scale for theory
    scale, A_err = fit_theory_amplitude(t, l)
    print("Scale and error on amplitude of A*t^1/3: ", scale, A_err)
    # scale = np.median(l) / (np.median(t) ** (1/3))
    l_theory = scale * (t_fit ** (1/3))

    ax.plot(t_fit, l_theory, ':', color='green', linewidth=2.5, alpha=0.8,
              label='Theory: l ∝ t^(1/3)', zorder=1)

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

    return fig, ax, fit_result, scale, A_err


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


