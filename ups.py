# coding: utf-8

import plistlib, subprocess
import http.client as httplib
from prometheus_client import start_http_server, Summary, Gauge, Enum
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import collections,os, time,calendar, sys, argparse, getopt, logging, datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta



class JsonCollector(object):
    def __init__(self):
        pass

    def collect(self):
        f = open("ups.txt", "w")
        ups = subprocess.run(["pmset", "-g", "ps", "-xml"], check=True, stdout=f)
        with open("ups.txt", 'rb') as infile:
            plist = plistlib.load(infile)

        ups_current_capacity = int(plist["Current Capacity"])
        ups_enabled_audible_alarm = plist["Enable Audible Alarm"]
        ups_internal_failure = plist["Internal Failure"]
        ups_is_charging = plist["Is Charging"]
        ups_is_present = plist["Is Present"]
        ups_max_capacity = plist["Max Capacity"]
        ups_name = plist["Name"]
        ups_power_source_id = plist["Power Source ID"]
        ups_power_source_state = plist["Power Source State"]
        ups_product_id = plist["Product ID"]
        ups_required_voltage = plist["Set Required Voltage"]
        ups_time_to_empty = plist["Time to Empty"]
        ups_transport_type = plist["Transport Type"]
        ups_type = plist["Type"]
        ups_vendor_id = plist["Vendor ID"]
        ups_input_voltage = int(plist["Voltage"])

        ups = GaugeMetricFamily(
            'ups',
            'UPS Current Capacity',
            labels=['ups_enabled_audible_alarm', 'ups_internal_failure','ups_is_charging','ups_is_present','ups_max_capacity', 'ups_name', 'ups_power_source_id','ups_power_source_state', 'ups_product_id', 'ups_required_voltage', 'ups_time_to_empty', 'ups_transport_type', 'ups_type', 'ups_vendor_id', 'ups_input_voltage' ])
        label_values = [ups_enabled_audible_alarm, ups_internal_failure, ups_is_charging, ups_is_present,ups_max_capacity, ups_name, ups_power_source_id, ups_power_source_state, ups_product_id, ups_required_voltage, ups_time_to_empty, ups_transport_type, ups_type, ups_vendor_id, ups_input_voltage ]
        
        # Browse the dictionary containing the json returned by the api, to link each metric to a dictionary key
        ups.add_metric(label_values, ups_current_capacity)
        yield ups
if __name__ == "__main__":
    print(time.strftime("%H:%M:%S"), "- Exporter launched: port 9902")
    start_http_server(9902)
    REGISTRY.register(JsonCollector())
    while True: time.sleep(1)            
