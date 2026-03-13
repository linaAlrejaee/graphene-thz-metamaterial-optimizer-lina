"""
data_loader.py - COMSOL S-Parameter Data Pipeline
Parses simulation .txt files, extracts parameters, finds S12 dips, pairs ON/OFF states.
"""

import os
import re
import numpy as np
import pandas as pd


def parse_filename(filename):
    """
    Extract simulation parameters from COMSOL export filename.

    Handles patterns like:
        Sdx35_gw5cw28wgraph1hgraph2wau4_sigma0.3.txt
        S_gw3cw28wgraph1hgraph2wau4_sigma0.3 (1) (1).txt
    """
    # Remove file extension and Windows download suffixes like (1), (2), (1) (1)
    name = os.path.basename(filename)
    name = re.sub(r'\.txt$', '', name)
    name = re.sub(r'\s*\(\d+\)', '', name)  # remove (1), (2), etc.
    name = name.strip()

    params = {}

    # Extract dx from prefix: "Sdx35_" -> 35, "S_" -> 35 (default)
    dx_match = re.match(r'Sdx(\d+)_', name)
    if dx_match:
        params['dx'] = int(dx_match.group(1))
    else:
        params['dx'] = 35  # default when filename starts with S_

    # Extract g_w, c_w, w_graph (wgraph), h_graph (hgraph), w_au (wau)
    gw_match = re.search(r'gw(\d+)', name)
    cw_match = re.search(r'cw(\d+)', name)
    wgraph_match = re.search(r'wgraph(\d+)', name)
    hgraph_match = re.search(r'hgraph(m?\d+)', name)
    wau_match = re.search(r'wau(\d+)', name)
    sigma_match = re.search(r'sigma([\d.]+)', name)

    params['g_w'] = int(gw_match.group(1)) if gw_match else None
    params['c_w'] = int(cw_match.group(1)) if cw_match else None
    params['w_graph'] = int(wgraph_match.group(1)) if wgraph_match else None
    params['h_graph'] = int(hgraph_match.group(1).replace('m', '-')) if hgraph_match else None
    params['w_au'] = int(wau_match.group(1)) if wau_match else None
    params['sigma'] = float(sigma_match.group(1)) if sigma_match else None

    return params


def read_comsol_file(filepath):
    """
    Read a COMSOL exported .txt file.
    Skips header lines starting with %, returns DataFrame with freq_hz, s12, s22.
    """
    freq, s12, s22 = [], [], []

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('%') or line == '':
                continue
            parts = line.split()
            if len(parts) >= 3:
                freq.append(float(parts[0]))
                s12.append(float(parts[1]))
                s22.append(float(parts[2]))

    df = pd.DataFrame({
        'freq_hz': freq,
        'freq_ghz': [f / 1e9 for f in freq],
        's12': s12,
        's22': s22
    })
    return df


def find_dip(freq, s_param):
    """Find the minimum (dip) of an S-parameter and its frequency."""
    min_idx = np.argmin(s_param)
    return s_param[min_idx], freq[min_idx]


def load_all_data(folder_path):
    """
    Load all .txt COMSOL files from folder.
    Returns a summary DataFrame with one row per simulation.
    """
    rows = []

    for fname in os.listdir(folder_path):
        if not fname.endswith('.txt'):
            continue

        filepath = os.path.join(folder_path, fname)
        params = parse_filename(fname)

        # Skip files where parsing failed
        if params['sigma'] is None:
            print(f"  Skipping (can't parse): {fname}")
            continue

        curve = read_comsol_file(filepath)

        s12_min, s12_min_freq = find_dip(curve['freq_ghz'].values, curve['s12'].values)
        s22_min, s22_min_freq = find_dip(curve['freq_ghz'].values, curve['s22'].values)

        row = {
            'filename': fname,
            'dx': params['dx'],
            'g_w': params['g_w'],
            'c_w': params['c_w'],
            'w_graph': params['w_graph'],
            'h_graph': params['h_graph'],
            'w_au': params['w_au'],
            'sigma': params['sigma'],
            's12_min': s12_min,
            's12_min_freq': s12_min_freq,
            's22_min': s22_min,
            's22_min_freq': s22_min_freq,
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df.sort_values(['dx', 'g_w', 'c_w', 'sigma']).reset_index(drop=True)
    return df


def pair_on_off(df):
    """
    Pair ON (sigma=0.3) and OFF (sigma=1.2) simulations with same geometry.
    Returns DataFrame with frequency shift and dip comparison.
    """
    geo_cols = ['dx', 'g_w', 'c_w', 'w_graph', 'h_graph', 'w_au']

    on_df = df[df['sigma'] == 0.3].copy()
    off_df = df[df['sigma'] == 1.2].copy()

    pairs = pd.merge(on_df, off_df, on=geo_cols, suffixes=('_on', '_off'))

    if len(pairs) == 0:
        print("No ON/OFF pairs found.")
        return pd.DataFrame()

    pairs['freq_shift_ghz'] = abs(pairs['s12_min_freq_on'] - pairs['s12_min_freq_off'])
    pairs['avg_dip'] = (pairs['s12_min_on'] + pairs['s12_min_off']) / 2

    result = pairs[geo_cols + [
        's12_min_on', 's12_min_freq_on',
        's12_min_off', 's12_min_freq_off',
        'freq_shift_ghz', 'avg_dip'
    ]]
    return result


def get_full_curves(folder_path):
    """
    Load full S-parameter curves for all files.
    Returns dict: {filename: {params: dict, curve: DataFrame}}
    """
    curves = {}

    for fname in os.listdir(folder_path):
        if not fname.endswith('.txt'):
            continue

        filepath = os.path.join(folder_path, fname)
        params = parse_filename(fname)

        if params['sigma'] is None:
            continue

        curve = read_comsol_file(filepath)
        curves[fname] = {'params': params, 'curve': curve}

    return curves


# --- Run standalone to verify ---
if __name__ == '__main__':
    from config import DATA_DIR

    print("=" * 70)
    print("COMSOL Data Loader - Loading all simulation files")
    print("=" * 70)

    df = load_all_data(DATA_DIR)
    print(f"\nFound {len(df)} unique simulations:\n")
    print(df[['dx', 'g_w', 'c_w', 'h_graph', 'sigma', 's12_min', 's12_min_freq']].to_string(index=False))

    print("\n" + "=" * 70)
    print("ON/OFF Pairs (for frequency shift)")
    print("=" * 70)

    pairs = pair_on_off(df)
    if len(pairs) > 0:
        print(f"\nFound {len(pairs)} ON/OFF pairs:\n")
        print(pairs[['dx', 'g_w', 'c_w', 's12_min_on', 's12_min_freq_on',
                      's12_min_off', 's12_min_freq_off', 'freq_shift_ghz', 'avg_dip']].to_string(index=False))
    else:
        print("\nNo complete ON/OFF pairs found.")
