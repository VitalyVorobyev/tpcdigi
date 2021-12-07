#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from recoclusters import digits_to_clusters, params
from tpcplot import add_grid

def x_center_of_mass(x, ampl):
    return x @ ampl / np.sum(ampl)


charge_to_ionization = 0.03 / 10**4  # [keV]


def process_track(hits):
    data = np.column_stack((*digits_to_clusters(hits), hits['ampl']))
    data = data[np.argsort(data[:, 2])]

    charge = np.sum(hits['ampl']) * charge_to_ionization
    clusters = []
    for z in np.unique(data[:, 2]):
        digits = data[data[:, 2] == z]
        mean = digits[:, :2].T @ digits[:, -1] / np.sum(digits[:, -1])
        clusters.append([mean[0], mean[1], z])
    clusters = np.array(clusters)
    deltas = clusters[1:] - clusters[:-1]
    trklen = np.sum(np.sqrt(np.sum(deltas**2, axis=1)))
    return charge, trklen, charge / trklen


def plot_dedx(lengths, values, charge):
    fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(12, 12))

    add_grid(ax[0, 0], 'Track length (mm)', 'events', False)
    ax[0, 0].hist(lengths, bins=60, histtype='step')
    ax[0, 0].set_xlim((0, 1.05 * np.max(lengths)))

    add_grid(ax[0, 1], 'Energy deposition (X / mm)', 'events', False)
    ax[0, 1].hist(values, bins=60, histtype='step')
    ax[0, 1].set_xlim((0, 1.05 * np.max(values)))

    add_grid(ax[1, 0], 'Track length (mm)', 'Energy deposition (X / mm)', False)
    ax[1, 0].scatter(lengths, values, s=2)
    ax[1, 0].set_xlim((0, 1.05 * np.max(lengths)))
    ax[1, 0].set_ylim((0, 1.05 * np.max(values)))

    add_grid(ax[1, 1], 'Track length (mm)', 'Charge', False)
    ax[1, 1].scatter(lengths, charge, s=2)
    ax[1, 1].set_xlim((0, 1.05 * np.max(lengths)))
    ax[1, 1].set_ylim((0, 1.05 * np.max(charge)))

    fig.tight_layout()
    plt.show()

def main():
    from readdata import get_data
    import sys
    key = 'mu_150.0' if len(sys.argv) < 2 else sys.argv[1]
    _, digits = get_data(key)

    lengths, values, charge = [], [], []
    for evtn, digits in digits.items():
        q, l, dEdx = process_track(digits)
        if l < 100 and l > 10 and dEdx < 5e7:
            print(f'{evtn:3d}: q={q:10.0f} l={l:6.2f} dEdx={dEdx:8.0f}')
            values.append(dEdx)
            lengths.append(l)
            charge.append(q)
    print(f'{np.mean(values)*1.e-6:.3f} +- {np.std(values)*1.e-6:.3f}')
    plot_dedx(lengths, values, charge)


if __name__ == '__main__':
    main()
