"""
visualize.py - Generate plots from COMSOL simulation data.
Saves 5 PNG plots to a plots/ folder.
"""

import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for saving PNGs

from config import DATA_DIR, PLOTS_DIR
from data_loader import load_all_data, pair_on_off, get_full_curves


def plot_all_s12_curves(curves, plots_dir):
    """Plot 1: All S12 curves overlaid, colored by sigma."""
    fig, ax = plt.subplots(figsize=(12, 7))

    for fname, data in sorted(curves.items(), key=lambda x: x[1]['params']['sigma']):
        p = data['params']
        curve = data['curve']
        sigma = p['sigma']

        color = 'tab:blue' if sigma == 0.3 else 'tab:red'
        alpha = 0.9
        label = f"dx={p['dx']} gw={p['g_w']} cw={p['c_w']} σ={sigma}"

        ax.plot(curve['freq_ghz'], curve['s12'], color=color, alpha=alpha, label=label)

    ax.set_xlabel('Frequency (GHz)', fontsize=12)
    ax.set_ylabel('S12 (dB)', fontsize=12)
    ax.set_title('All S12 Transmission Curves', fontsize=14)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(plots_dir, '1_all_s12_curves.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_s12_dip_vs_cw(df, plots_dir):
    """Plot 2: S12 dip depth vs c_w, grouped by g_w."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Filter to dx=35 only for fair comparison across c_w
    filtered = df[(df['sigma'] == 0.3) & (df['dx'] == 35)]
    for gw, group in filtered.groupby('g_w'):
        ax.scatter(group['c_w'], group['s12_min'], s=100, label=f'g_w={gw} μm', zorder=5)
        ax.plot(group['c_w'], group['s12_min'], '--', alpha=0.5)

    ax.set_xlabel('c_w - Capacitor Width (μm)', fontsize=12)
    ax.set_ylabel('S12 Dip Depth (dB)', fontsize=12)
    ax.set_title('S12 Dip Depth vs Capacitor Width (sigma=0.3, ON state)', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()  # more negative = deeper dip = better, show at top

    plt.tight_layout()
    path = os.path.join(plots_dir, '2_s12_dip_vs_cw.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_s12_dip_vs_dx(df, plots_dir):
    """Plot 3: S12 dip depth vs dx (unit cell size sweep)."""
    dx_sweep = df[(df['g_w'] == 3) & (df['c_w'] == 28) & (df['sigma'] == 0.3)]

    if len(dx_sweep) == 0:
        print("  Skipping dx plot - no dx sweep data found")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(dx_sweep['dx'], dx_sweep['s12_min'], s=100, color='tab:blue', zorder=5)
    ax.plot(dx_sweep['dx'], dx_sweep['s12_min'], '--', color='tab:blue', alpha=0.5)

    # Add frequency labels
    for _, row in dx_sweep.iterrows():
        ax.annotate(f'{row["s12_min_freq"]:.0f} GHz',
                     (row['dx'], row['s12_min']),
                     textcoords='offset points', xytext=(10, 5), fontsize=9)

    ax.set_xlabel('dx - Unit Cell Size (μm)', fontsize=12)
    ax.set_ylabel('S12 Dip Depth (dB)', fontsize=12)
    ax.set_title('S12 Dip Depth vs Unit Cell Size (g_w=3, c_w=28, sigma=0.3)', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.invert_yaxis()

    plt.tight_layout()
    path = os.path.join(plots_dir, '3_s12_dip_vs_dx.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_on_off_comparison(curves, pairs, plots_dir):
    """Plot 4: ON vs OFF S12 curves side-by-side for each pair."""
    if len(pairs) == 0:
        print("  Skipping ON/OFF comparison - no pairs found")
        return

    n_pairs = len(pairs)
    fig, axes = plt.subplots(1, n_pairs, figsize=(5 * n_pairs, 5), squeeze=False)

    for i, (_, pair) in enumerate(pairs.iterrows()):
        ax = axes[0][i]

        # Find matching curve files
        for fname, data in curves.items():
            p = data['params']
            if (p['dx'] == pair['dx'] and p['g_w'] == pair['g_w'] and
                    p['c_w'] == pair['c_w']):
                curve = data['curve']
                if p['sigma'] == 0.3:
                    ax.plot(curve['freq_ghz'], curve['s12'], 'b-', linewidth=2,
                            label=f'ON (σ=0.3)')
                elif p['sigma'] == 1.2:
                    ax.plot(curve['freq_ghz'], curve['s12'], 'r-', linewidth=2,
                            label=f'OFF (σ=1.2)')

        # Mark dips
        ax.axvline(pair['s12_min_freq_on'], color='blue', linestyle=':', alpha=0.5)
        ax.axvline(pair['s12_min_freq_off'], color='red', linestyle=':', alpha=0.5)

        # Annotate frequency shift
        shift = pair['freq_shift_ghz']
        mid_freq = (pair['s12_min_freq_on'] + pair['s12_min_freq_off']) / 2
        mid_dip = pair['avg_dip']
        ax.annotate(f'Δf = {shift:.0f} GHz', xy=(mid_freq, mid_dip),
                     fontsize=11, fontweight='bold', color='green',
                     ha='center', va='bottom')

        ax.set_title(f"dx={pair['dx']} gw={pair['g_w']} cw={pair['c_w']}", fontsize=11)
        ax.set_xlabel('Frequency (GHz)', fontsize=10)
        ax.set_ylabel('S12 (dB)', fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    fig.suptitle('ON vs OFF State Comparison (S12)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    path = os.path.join(plots_dir, '4_on_off_comparison.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_freq_shift_bar(pairs, plots_dir):
    """Plot 5: Frequency shift bar chart across parameter combinations."""
    if len(pairs) == 0:
        print("  Skipping frequency shift bar chart - no pairs found")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    labels = [f"dx={r['dx']} gw={r['g_w']} cw={r['c_w']}" for _, r in pairs.iterrows()]
    shifts = pairs['freq_shift_ghz'].values
    avg_dips = pairs['avg_dip'].values

    x = range(len(labels))

    bars1 = ax.bar(x, shifts, width=0.4, color='tab:green', alpha=0.8, label='Freq Shift (GHz)')

    # Add value labels on bars
    for bar, val in zip(bars1, shifts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f'{val:.0f} GHz', ha='center', fontsize=11, fontweight='bold')

    # Secondary axis for dip depth
    ax2 = ax.twinx()
    ax2.scatter(x, avg_dips, color='tab:red', s=150, zorder=5, marker='D', label='Avg Dip Depth (dB)')
    ax2.set_ylabel('Avg S12 Dip Depth (dB)', fontsize=12, color='tab:red')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_xlabel('Parameter Combination', fontsize=12)
    ax.set_ylabel('Frequency Shift (GHz)', fontsize=12)
    ax.set_title('Frequency Shift & Dip Depth per Configuration', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')

    # Combined legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    plt.tight_layout()
    path = os.path.join(plots_dir, '5_freq_shift_and_dip.png')
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  Saved: {path}")


if __name__ == '__main__':
    os.makedirs(PLOTS_DIR, exist_ok=True)

    print("=" * 60)
    print("Generating plots from COMSOL simulation data")
    print("=" * 60)

    # Load data
    df = load_all_data(DATA_DIR)
    pairs = pair_on_off(df)
    curves = get_full_curves(DATA_DIR)

    print(f"\nLoaded {len(df)} simulations, {len(pairs)} ON/OFF pairs\n")

    # Generate all plots
    print("Generating plots:")
    plot_all_s12_curves(curves, PLOTS_DIR)
    plot_s12_dip_vs_cw(df, PLOTS_DIR)
    plot_s12_dip_vs_dx(df, PLOTS_DIR)
    plot_on_off_comparison(curves, pairs, PLOTS_DIR)
    plot_freq_shift_bar(pairs, PLOTS_DIR)

    print(f"\nAll plots saved to: {PLOTS_DIR}")
