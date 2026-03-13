"""
analyze.py - Summary analysis and report generation.
Prints findings to terminal and saves report.txt.
"""

import os
import pandas as pd
from config import DATA_DIR, OUTPUT_DIR
from data_loader import load_all_data, pair_on_off


def generate_report(df, pairs, output_dir):
    """Generate a text report of all findings."""
    lines = []

    def add(text=""):
        lines.append(text)
        print(text)

    add("=" * 70)
    add("COMSOL SIMULATION ANALYSIS REPORT")
    add("Project: ML-Based Optimization of Graphene THz Metamaterial Devices")
    add("=" * 70)

    # --- Section 1: Data Overview ---
    add(f"\n1. DATA OVERVIEW")
    add(f"   Total simulations loaded: {len(df)}")
    add(f"   ON/OFF pairs available:   {len(pairs)}")
    # Auto-detect which parameters are varied vs constant
    param_cols = ['dx', 'g_w', 'c_w', 'h_graph', 'w_graph', 'w_au']
    varied = [c for c in param_cols if df[c].nunique() > 1]
    constant = {c: df[c].iloc[0] for c in param_cols if df[c].nunique() == 1}

    add(f"   Parameters varied:        {', '.join(varied)}")
    if constant:
        const_str = ', '.join(f"{k}={v}" for k, v in constant.items())
        add(f"   Parameters constant:      {const_str}")

    add(f"\n   Parameter ranges:")
    for col in varied:
        vals = sorted(df[col].unique())
        add(f"   - {col}: {vals}")

    # --- Section 2: All Simulations Table ---
    add(f"\n2. ALL SIMULATIONS")
    add("-" * 70)
    table = df[['dx', 'g_w', 'c_w', 'h_graph', 'sigma', 's12_min', 's12_min_freq']].copy()
    table.columns = ['dx', 'g_w', 'c_w', 'h_graph', 'sigma', 'S12 Dip (dB)', 'Dip Freq (GHz)']
    table['S12 Dip (dB)'] = table['S12 Dip (dB)'].round(2)
    add(table.to_string(index=False))

    # --- Section 3: Best Configurations ---
    add(f"\n3. BEST CONFIGURATIONS")
    add("-" * 70)

    # Best dip depth (most negative S12)
    best_dip = df.loc[df['s12_min'].idxmin()]
    add(f"   Deepest S12 dip: {best_dip['s12_min']:.2f} dB at {best_dip['s12_min_freq']:.0f} GHz")
    add(f"     Config: dx={best_dip['dx']}, g_w={best_dip['g_w']}, c_w={best_dip['c_w']}, h_graph={best_dip['h_graph']}, sigma={best_dip['sigma']}")

    if len(pairs) > 0:
        # Best frequency shift
        best_shift = pairs.loc[pairs['freq_shift_ghz'].idxmax()]
        add(f"\n   Largest frequency shift: {best_shift['freq_shift_ghz']:.0f} GHz")
        add(f"     Config: dx={best_shift['dx']}, g_w={best_shift['g_w']}, c_w={best_shift['c_w']}, h_graph={best_shift['h_graph']}")

        # Best combined (deepest avg dip + largest shift)
        best_combined = pairs.loc[pairs['avg_dip'].idxmin()]
        add(f"\n   Deepest average dip (ON+OFF): {best_combined['avg_dip']:.2f} dB")
        add(f"     Config: dx={best_combined['dx']}, g_w={best_combined['g_w']}, c_w={best_combined['c_w']}, h_graph={best_combined['h_graph']}")

    # --- Section 4: ON/OFF Pairs ---
    if len(pairs) > 0:
        add(f"\n4. ON/OFF PAIR COMPARISON")
        add("-" * 70)
        pair_table = pairs[['dx', 'g_w', 'c_w', 'h_graph',
                            's12_min_on', 's12_min_freq_on',
                            's12_min_off', 's12_min_freq_off',
                            'freq_shift_ghz', 'avg_dip']].copy()
        pair_table.columns = ['dx', 'g_w', 'c_w', 'h_graph',
                              'ON Dip(dB)', 'ON Freq(GHz)',
                              'OFF Dip(dB)', 'OFF Freq(GHz)',
                              'Shift(GHz)', 'AvgDip(dB)']
        for col in ['ON Dip(dB)', 'OFF Dip(dB)', 'AvgDip(dB)']:
            pair_table[col] = pair_table[col].round(2)
        add(pair_table.to_string(index=False))

    # --- Section 5: Parameter Sensitivity ---
    add(f"\n5. PARAMETER SENSITIVITY (ON state, sigma=0.3)")
    add("-" * 70)

    on_data = df[df['sigma'] == 0.3]

    # dx sensitivity (g_w=3, c_w=28, h_graph=2 sweep)
    dx_sweep = on_data[(on_data['g_w'] == 3) & (on_data['c_w'] == 28) & (on_data['h_graph'] == 2)].sort_values('dx')
    if len(dx_sweep) > 1:
        dx_range = dx_sweep['dx'].max() - dx_sweep['dx'].min()
        dip_range = dx_sweep['s12_min'].min() - dx_sweep['s12_min'].max()
        freq_range = dx_sweep['s12_min_freq'].max() - dx_sweep['s12_min_freq'].min()
        add(f"   dx (unit cell size): {dx_sweep['dx'].min()}-{dx_sweep['dx'].max()} um")
        add(f"     S12 dip change:  {dip_range:.2f} dB over {dx_range} um range")
        add(f"     Freq change:     {freq_range:.0f} GHz over {dx_range} um range")
        add(f"     Sensitivity:     {dip_range/dx_range:.3f} dB/um,  {freq_range/dx_range:.1f} GHz/um")

    # c_w sensitivity (g_w=5, dx=35 sweep)
    cw_sweep = on_data[(on_data['g_w'] == 5) & (on_data['dx'] == 35)].sort_values('c_w')
    if len(cw_sweep) > 1:
        cw_range = cw_sweep['c_w'].max() - cw_sweep['c_w'].min()
        dip_range = cw_sweep['s12_min'].min() - cw_sweep['s12_min'].max()
        freq_range = cw_sweep['s12_min_freq'].max() - cw_sweep['s12_min_freq'].min()
        add(f"\n   c_w (capacitor width): {cw_sweep['c_w'].min()}-{cw_sweep['c_w'].max()} um")
        add(f"     S12 dip change:  {dip_range:.2f} dB over {cw_range} um range")
        add(f"     Freq change:     {freq_range:.0f} GHz over {cw_range} um range")
        add(f"     Sensitivity:     {dip_range/cw_range:.3f} dB/um,  {freq_range/cw_range:.1f} GHz/um")

    # h_graph sensitivity (dx=35, g_w=3, c_w=28 sweep)
    hg_sweep = on_data[(on_data['dx'] == 35) & (on_data['g_w'] == 3) & (on_data['c_w'] == 28)].sort_values('h_graph')
    if len(hg_sweep) > 1:
        hg_range = hg_sweep['h_graph'].max() - hg_sweep['h_graph'].min()
        dip_range = hg_sweep['s12_min'].min() - hg_sweep['s12_min'].max()
        add(f"\n   h_graph (graphene height): {hg_sweep['h_graph'].min()} to {hg_sweep['h_graph'].max()} um")
        add(f"     S12 dip change:  {dip_range:.2f} dB over {hg_range} um range")
        add(f"     Sensitivity:     {dip_range/hg_range:.3f} dB/um")
        add(f"     Best value:      h_graph={hg_sweep.loc[hg_sweep['s12_min'].idxmin(), 'h_graph']} "
            f"({hg_sweep['s12_min'].min():.2f} dB)")

    # --- Section 6: Missing Data ---
    add(f"\n6. MISSING DATA (sigma=1.2 pairs needed)")
    add("-" * 70)

    on_only = df[df['sigma'] == 0.3]
    off_only = df[df['sigma'] == 1.2]
    geo_cols = ['dx', 'g_w', 'c_w', 'w_graph', 'h_graph', 'w_au']

    missing = on_only[~on_only.set_index(geo_cols).index.isin(
        off_only.set_index(geo_cols).index)]

    if len(missing) > 0:
        add(f"   {len(missing)} simulations need sigma=1.2 counterparts:")
        for _, row in missing.iterrows():
            add(f"   - dx={row['dx']}, g_w={row['g_w']}, c_w={row['c_w']}, h_graph={row['h_graph']} (has sigma=0.3 only)")
    else:
        add("   All ON simulations have matching OFF pairs!")

    # --- Section 7: Recommendations ---
    add(f"\n7. RECOMMENDATIONS FOR NEXT SIMULATIONS")
    add("-" * 70)
    if len(missing) > 0:
        add("   Priority 1: Run sigma=1.2 for unmatched ON-state files:")
        for _, row in missing.iterrows():
            add(f"     - dx={row['dx']}, g_w={row['g_w']}, c_w={row['c_w']}, h_graph={row['h_graph']}, sigma=1.2")

    add("")
    if constant:
        add("   Priority 2: Vary parameters that are still constant:")
        for k, v in constant.items():
            add(f"     - {k}: currently fixed at {v}")

    add("")
    add("   Priority 3: Explore promising parameter space:")
    if 'h_graph' in varied:
        best_hg = on_data.loc[on_data['s12_min'].idxmin()]
        add(f"     - h_graph={best_hg['h_graph']} gave deepest dip ({best_hg['s12_min']:.2f} dB) — try nearby values")
    add("     - Larger dx and c_w values tend to give deeper dips")

    # --- Section 8: Distance to Target ---
    add(f"\n8. DISTANCE TO OPTIMIZATION TARGETS")
    add("-" * 70)
    add(f"   Target S12 dip:      -20 dB")
    add(f"   Current best:        {best_dip['s12_min']:.2f} dB")
    add(f"   Gap:                 {-20 - best_dip['s12_min']:.2f} dB to go")
    if len(pairs) > 0:
        add(f"\n   Target freq shift:   large as possible")
        add(f"   Current best:        {pairs['freq_shift_ghz'].max():.0f} GHz")

    add("\n" + "=" * 70)
    add("END OF REPORT")
    add("=" * 70)

    # Save to file
    report_path = os.path.join(output_dir, 'report.txt')
    with open(report_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"\nReport saved to: {report_path}")


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = load_all_data(DATA_DIR)
    pairs = pair_on_off(df)

    generate_report(df, pairs, OUTPUT_DIR)
