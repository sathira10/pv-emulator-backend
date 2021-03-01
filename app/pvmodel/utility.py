import os
from dataclasses import astuple
from datetime import datetime

import numpy as np
from scipy.optimize import root
import matplotlib.pyplot as plt
from matplotlib import rcParams

from app.pvmodel.data import Datasheet, Parameters


def get_plot(data: Datasheet, params: Parameters):
    voc = data.voc
    (iph, io, rs, rsh, a, algorithm) = astuple(params)
    array_size = 300  # number of points
    v_out = np.linspace(0, voc)
    i_out = []

    for v in v_out:
        def f(i):
            return i - iph + io * np.exp((v + i * rs) / a) - io + (v + i * rs) / rsh

        result = root(f, np.array([iph / 2]))
        i_out.append(result.x[0])

    p_out = [x * y for x, y in zip(v_out, i_out)]
    return v_out, i_out, p_out


def get_figure(v_out, i_out, p_out):
    plt.style.use('seaborn')
    # rcParams['font.family'] = 'sans-serif'
    # rcParams['font.sans-serif'] = ["cambria math"]

    # Delete all files in folder
    file_list = [f for f in os.listdir("./app/static") if f.endswith(".png")]
    for f in file_list:
        os.remove(os.path.join("app", "static", f))

    # generate new plots
    now = datetime.now()
    fig = plt.figure(figsize=(4, 2.25), dpi=300)
    ax = plt.gca()
    ax.plot(v_out, i_out, color='#05668D')
    ax.set(xlabel='voltage (V)', ylabel='current (A)')
    ax.set_ylim(0, 2 * (max(i_out) // 2) + 2)
    ax.set_xlim(0, 5 * (v_out[-1] // 5) + 5)
    iv_curve = "IV-" + now.strftime('%m%d%H%M%S') + ".png"
    path = os.path.join("app", "static", iv_curve)
    plt.savefig(path, bbox_inches='tight')

    fig = plt.figure(figsize=(4, 2.25), dpi=300)
    ax = plt.gca()
    ax.plot(v_out, p_out, color='#05668D')
    ax.set(xlabel='voltage (V)', ylabel='current (A)')
    ax.set_ylim(0, 10 * (max(p_out) // 10) + 10)
    ax.set_xlim(0, 5 * (v_out[-1] // 5) + 5)
    pv_curve = "PV-" + now.strftime('%m%d%H%M%S') + ".png"
    path = os.path.join("app", "static", pv_curve)
    plt.savefig(path, bbox_inches='tight')
    return iv_curve, pv_curve
