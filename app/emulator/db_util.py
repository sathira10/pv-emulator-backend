import json
import os
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client import write_api

org = "fyp"
bucket = "emulator"


def new_client():
    with open(os.path.join("app", "influxdb.json")) as f:
        influx_data = json.load(f)
    token = influx_data["token"]

    client = InfluxDBClient(url="http://localhost:8086", token=token)
    return client


def db_write(api: write_api, i_adc: float, v_adc: float, v_ref: float):
    time = datetime.utcnow()

    i_adc = Point("C2000").field("i_adc", i_adc).time(time, WritePrecision.NS)
    v_adc = Point("C2000").field("v_adc", v_adc).time(time, WritePrecision.NS)
    v_ref = Point("C2000").field("v_ref", v_ref).time(time, WritePrecision.NS)

    try:
        api.write(bucket, org, [i_adc, v_adc, v_ref])
    except Exception as e:
        print(e)
