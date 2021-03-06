from dataclasses import asdict

from app.pvmodel.algorithms import nrel_sam, lambert_w
from app.pvmodel.data import Datasheet
from app.pvmodel.utility import get_plot, get_figure


def get_params(data):
    try:
        data_sheet = Datasheet(float(data["isc"]),
                               float(data["voc"]),
                               float(data["imp"]),
                               float(data["vmp"]),
                               float(data["alpha"]),
                               float(data["beta"]),
                               int(data["n_ser"]),
                               data["cell_type"],
                               float(data["c"]),
                               float(data["g"]))
    except ValueError as e:
        print(e)
        return {"error": "invalid_input", "description": str(e)}

    try:
        result = nrel_sam(data_sheet)
    except Exception:
        try:
            result = lambert_w(data_sheet)
        except Exception as e:
            print(e)
            return {"error": "calculation_error", "description": str(e)}
    finally:
        params = asdict(result.round())

        v_out, i_out, p_out = get_plot(data_sheet, result)
        iv_curve, pv_curve = get_figure(v_out, i_out, p_out)

        params["iv"] = iv_curve
        params["pv"] = pv_curve

    return params
