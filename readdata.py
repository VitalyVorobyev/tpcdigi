#! /usr/bin/env python

import sys
import numpy as np


def group_by_event(data, maxevt=10**7, key='evtn'):
    unique_events = np.unique(data[key])
    maxevt = min(maxevt, unique_events.shape[0])
    return {k: data[data[key] == k] for k in unique_events[:maxevt]}


def get_data(key, datapath, maxevt=10**7):
    g4data = np.load('/'.join([datapath, f'g4hits_gun_{key}_digi.npy']))
    hits = np.load('/'.join([datapath, f'digi_gun_{key}_digi.npy']))
    return group_by_event(g4data, maxevt), group_by_event(hits, maxevt)
