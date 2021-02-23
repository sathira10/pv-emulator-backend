from dataclasses import dataclass

import numpy as np


@dataclass()
class Datasheet:
    isc: float  # short circuit current
    voc: float  # open circuit voltage
    imp: float  # max power point current
    vmp: float  # max power point voltage
    alpha: float  # temp coefficient of isc
    beta: float  # temp coefficient of voc
    n_ser: float  # number of cells in series
    cell_type: str  # cell material
    c: float  # temperature in degrees Celsius
    g: float  # irradiance


@dataclass()
class Parameters:
    iph: float  # photo current
    io: float  # saturation current
    rs: float  # series resistance
    rsh: float  # shunt resistance
    a: float  # diode ideality factor
    algorithm   : str  # algorithm used

    def round(self):
        self.iph = np.round(self.iph, 2)
        self.io = float(np.format_float_scientific(self.io, 2))
        self.rs = np.round(self.rs, 3)
        self.rsh = np.round(self.rsh, 2)
        self.a = np.round(self.a, 2)
        return self
