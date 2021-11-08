#! /usr/bin/env python

params = {
    'r_in': 40.5,  # mm
    'r_out': 199.0,  # mm
    'zmax': 300.0,  # mm
    'pixel_size': 1.2,  # mm
    'drift_velocity': 34.5,  # mm / mus
    'time_frame': 50,  # ns
}
params['time2length'] = params['drift_velocity'] * 1.e-3,  # mm


def grid_size():
    return int(2 * params['r_out'] // params['pixel_size'])


def number_of_pads():
    return grid_size()**2


def padid(x, y, front=True):
    row = (params['r_out'] - y) // params['pixel_size']
    col = (params['r_out'] + x) // params['pixel_size']
    pixid = row * grid_size() + col
    if not front:
        pixid += number_of_pads()
    return pixid


def pixid2position(pixid):
    nega_z = pixid > number_of_pads()
    pixid[nega_z] -= number_of_pads()

    return (
        (pixid % grid_size()) * params['pixel_size'] - params['r_out'],
        params['r_out'] - (pixid // grid_size()) * params['pixel_size'],
        nega_z
    )

def digits_to_clusters(digits):
    x, y, nega_z = pixid2position(digits['channel'])
    z = params['zmax'] - digits['frame'] * params['time2length']
    z[nega_z] = -z[nega_z]
    return x, y, z
