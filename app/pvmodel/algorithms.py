from dataclasses import astuple
import numpy as np
from PySAM import SixParsolve, Singlediodeparams
from scipy.special import lambertw
from app.pvmodel.data import Datasheet, Parameters

# reference conditions
c_ref = 25
t_ref = c_ref + 273.15
g_ref = 1000

# cell types for NREL method
cell_types = ["monoSi", "multiSi/polySi", "cis", "cigs", "cdte", "amorphous"]

# physical constants
k = 1.38064852e-23  # Boltzmann const in [J/(m^2*K)]
q = 1.60217657e-19  # Electron charge in [C]
eg_ref = 1.121  # band gap voltage [eV]
eg = eg_ref * q  # band gap energy
vt_ref = k * t_ref / q  # reference thermal voltage


# Algorithm 1 - Using NREL PySAM Library*
# PySAM . National Renewable Energy Laboratory. https://github.com/nrel/pysam
# * This algorithm uses DeSoto's Method
# (De Soto, W., S. A. Klein, et al. (2006). “Improvement and validation of a model for photovoltaic array performance.”)

# NOTE - the parameters "gamma" and "reference temperature" are not used in this implementation of nrel algorithms
# gamma is calculated from available data while reference temperature is taken as 25

def nrel_sam(data: Datasheet):
    assert data.cell_type in cell_types, "Invalid cell type"
    gamma = data.beta / data.voc * 100  # gamma is calculated using beta and voc data

    # solve for parameters at reference conditions
    solver_input = {"Isc": data.isc,
                    "Voc": data.voc,
                    "Imp": data.imp,
                    "Vmp": data.vmp,
                    "alpha_isc": data.alpha,
                    "beta_voc": data.beta,
                    "Nser": data.n_ser,
                    "celltype": data.cell_type,
                    "Tref": c_ref,
                    "gamma_pmp": gamma}

    solver = SixParsolve.new()
    solver.SixParameterSolver.assign(solver_input)
    solver.execute(0)
    solver_output = solver.export()["Outputs"]

    # temperature and irradiance corrections
    solver_input = {"Il_ref": solver_output["Il"],
                    "Io_ref": solver_output["Io"],
                    "Rs_ref": solver_output["Rs"],
                    "Rsh_ref": solver_output["Rsh"],
                    "a_ref": solver_output["a"],
                    "Adj_ref": solver_output["Adj"],
                    "alpha_isc": data.alpha,
                    "I": data.g,
                    "T": data.c}

    solver = Singlediodeparams.new()
    solver.SingleDiodeModel.assign(solver_input)
    solver.execute(0)
    solver_output = solver.export()["Outputs"]

    parameters = Parameters(solver_output["Il"], solver_output["Io"], solver_output["Rs"], solver_output["Rsh"],
                            solver_output["a"], "nrel_sam")
    return parameters


# Algorithm 2 - Lambert W Function Based Method
# Reference - Callegaro, L., Ciobotaru, M., & Agelidis, V. G. (2016). Implementation of 3D Lookup Tables in PLECS
# for Modeling Photovoltaic Modules. 2016 Australasian Universities Power Engineering Conference (AUPEC)

def lambert_w(data: Datasheet):
    (isc, voc, imp, vmp, alpha, beta, n_ser, cell_type, c, g) = astuple(data)

    # diode ideality factor
    a = (beta - voc / t_ref) / ((n_ser * vt_ref) * ((alpha / isc) - (3 / t_ref) - (eg / (k * (t_ref ** 2)))))

    # photo generated current is approximated by short circuit current
    iph = isc

    # dark saturation current
    io = iph * np.exp(-voc / (a * n_ser * vt_ref))

    x = lambertw((vmp / (a * io * n_ser * vt_ref)) * (2 * imp - iph - io) * np.exp(
        vmp * (vmp - 2 * a * n_ser * vt_ref) / (np.power(a, 2) * np.power(n_ser, 2) * np.power(vt_ref, 2)))) \
        + (2 * vmp) / (n_ser * a * vt_ref) - np.power(vmp, 2) / (
                np.power(a, 2) * np.power(n_ser, 2) * np.power(vt_ref, 2))

    # series and shunt resistances
    rs = np.real((x * a * n_ser * vt_ref - vmp) / imp)
    rsh = np.real((x * a * n_ser * vt_ref) / (iph - imp - io * (np.exp(x) - 1)))

    # account for G and T
    # uses equations from Sera 2007
    t = c + 273.15
    g_ratio = g / g_ref

    vt = a * vt_ref
    alpha = alpha / isc * 100  # Convert alpha to %/C
    isc_t = isc * (1 + (alpha / 100) * (t - t_ref))
    voc_t = voc + beta * (t - t_ref)

    io_t = (isc_t - (voc_t - rs * isc_t) / rsh) * np.exp(-voc_t / (n_ser * vt * (t / t_ref)))
    iph_t = io_t * np.exp(voc_t / (n_ser * vt * (t / t_ref))) + voc_t / rsh
    iph_gt = iph_t * g_ratio

    # Correction to match definition of A from CEC
    a_nrel = n_ser * vt_ref * a

    parameters = Parameters(iph_gt, io_t, rs, rsh, a_nrel, "lambert_w")
    return parameters
