import math
from time import sleep

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from influxdb_client.client.write_api import SYNCHRONOUS
from serial import Serial

from app.pvmodel.main import get_params
from app.emulator.serial_util import new_connection, close_connection, update_parameters, read
from app.emulator.db_util import new_client, db_write

# serial
ser = Serial()  # empty serial object
port = 'COM4'

# flags
processing_flag = False  # flag to indicate that serial is busy
incoming_flag = False  # flag to indicate arrival of a new request

app = Flask(__name__)
CORS(app, resources=r'/*', headers='Content-Type')


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/param_ext", methods=['POST'])
def param_ext():
    data = request.form.to_dict()
    print(data)
    result = get_params(data)
    print(result)
    return result


@app.route('/api/set_port', methods=["POST"])
def set_port():
    global port
    try:
        port = request.form.to_dict()["port"]
    except KeyError:
        return "port not set"

    global ser
    ser, status = new_connection(port)

    return "port selected " + port +' : ' +  status


@app.route('/api/emulate', methods=["POST"])
def emulate():
    global processing_flag, incoming_flag, ser  # refer to global var
    incoming_flag = True  # SET incoming_flag
    sleep(1)

    # wait until processing is done
    while True:
        if ~ processing_flag:
            break

    incoming_flag = False  # REMOVE incoming_flag
    processing_flag = True  # SET processing_flag

    client = new_client()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    update_parameters(ser, 8.22, 7.44e-10, 0.3255, 171.605, 1.428, 8.22)

    if client.health().status == "pass":
        while True:
            if incoming_flag:
                break
            result = read(ser)
            if result is not None:
                print(result)
                i_adc, v_adc, v_ref = result
                if math.isfinite(v_ref) and v_ref >= 0:
                    db_write(write_api, i_adc, v_adc, v_ref)
                else:
                    # db_write(write_api, 0.0, 0.0, 0.0)
                    print("invalid data")
            sleep(0.2)

    processing_flag = False  # REMOVE processing_flag

    return "closed process"


if __name__ == '__main__':
    app.run()
