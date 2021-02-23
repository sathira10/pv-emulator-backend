from app.pvmodel.algorithms import nrel_sam, lambert_w
from app.pvmodel.data import Datasheet
from app.pvmodel.utility import get_plot, get_figure

# Kyocera kc200gt
isc = 8.21
voc = 32.9
imp = 7.61
vmp = 26.3
alpha = 0.00318
beta = -0.123
n_ser = 54
cell_type = "multiSi/polySi"

datasheet = Datasheet(isc, voc, imp, vmp, alpha, beta, n_ser, cell_type, 25, 1000)

print(str(nrel_sam(datasheet).round()))
print(str(lambert_w(datasheet).round()))

v_out, i_out, p_out = get_plot(datasheet, nrel_sam(datasheet))
get_figure(v_out, i_out, p_out)
