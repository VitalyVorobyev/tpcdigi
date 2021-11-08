#! /usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from recoclusters import digits_to_clusters, params

def draw_energy(g4data):
    plt.figure(figsize=(8, 6))
    plt.hist(g4data['energy'] * 10**6, bins=60, histtype='step')
    plt.xlabel('Energy deposition (keV)')
    plt.minorticks_on()
    plt.grid(which='major')
    plt.grid(which='minor', linestyle=':')
    plt.tight_layout()
    plt.show()


def add_grid(ax, xlbl, ylbl, eq):
    ax.set_xlabel(xlbl)
    ax.set_ylabel(ylbl)
    ax.minorticks_on()
    ax.grid(which='major')
    ax.grid(which='minor', linestyle=':')
    if eq:
        ax.axis('equal')


def draw_g4xyz(g4data, hits):
    fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(16, 8), sharey=False)

    x, y, z = digits_to_clusters(hits)
    rho = np.hypot(x, y)

    g4size = 15 * g4data['energy'] * 1.e5
    digisize = 15 * hits['ampl'] / 1.e6
    ax[0].scatter(g4data['prex'], g4data['prey'], s=g4size)
    ax[0].scatter(g4data['postx'], g4data['posty'], s=g4size)
    ax[0].scatter(x, y, s=digisize)
    add_grid(ax[0], xlbl='x (mm)', ylbl='y (mm)', eq=True)
    draw_ring(ax[0])

    prerho = np.hypot(g4data['prex'], g4data['prey'])
    postrho = np.hypot(g4data['postx'], g4data['posty'])
    ax[1].scatter(g4data['prez'], prerho, s=g4size)
    ax[1].scatter(g4data['postz'], postrho, s=g4size)
    ax[1].scatter(z, rho, s=digisize)
    ax[1].set_ylim((0, 1.05 * params['r_out']))
    add_grid(ax[1], xlbl='z (mm)', ylbl=r'$\rho$ (mm)', eq=False)
    draw_rect(ax[1])

    fig.tight_layout()
    plt.show()


def draw_rect(ax):
    zmax, r_in, r_out = [params[key] for key in ['zmax', 'r_in', 'r_out']]
    ax.plot([-zmax, -zmax, zmax, zmax, -zmax],
            [r_in, r_out, r_out, r_in, r_in], 'k-')


def draw_ring(ax):
    r_in, r_out = [params[key] for key in ['r_in', 'r_out']]
    draw_circ(ax, r_out)
    draw_circ(ax, r_in)


def draw_circ(ax, rad):
    phi = np.linspace(0, 2*np.pi, 100)
    ax.plot(rad*np.cos(phi), rad*np.sin(phi), 'k-')


def main():
    from readdata import get_data
    import sys
    key = 'mu_150.0' if len(sys.argv) < 2 else sys.argv[1]
    nevt = 10**6 if len(sys.argv) < 3 else int(sys.argv[2])
    g4hits, digits = get_data(key, nevt)

    for evtn, g4h in g4hits.items():
        print(digits.get(evtn, None).size, g4h.size)
        draw_g4xyz(g4h, digits.get(evtn, None))
    
    # evtn = 944
    # draw_g4xyz(g4hits[evtn], digits[evtn])


if __name__ == '__main__':
    main()
