# -*- coding: utf-8 -*-
import plistlib, subprocess,re
import http.client as httplib
from prometheus_client import start_http_server, Summary, Gauge, Enum
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import collections,os, time,calendar, sys, argparse, getopt, logging, datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os

class JsonCollector(object):
    def __init__(self):
        pass

    def collect(self):
        f = open("ups.txt", "wb")
        ups = subprocess.run(["pmset", "-g", "ps", "-xml"], check=True, stdout=f)
        with open("ups.txt", 'rb') as infile:
            plist = plistlib.load(infile)

        ups_enabled_audible_alarm = plist["Enable Audible Alarm"]
        ups_enabled_audible_alarm = str(ups_enabled_audible_alarm).replace('\n', r'\n')        
        ups_internal_failure = plist["Internal Failure"]
        ups_internal_failure = str(ups_internal_failure).replace('\n', r'\n')  
        ups_current_capacity = int(plist["Current Capacity"])
        ups_is_charging = plist["Is Charging"]
        ups_is_charging = str(ups_is_charging).replace('\n', r'\n')
        ups_is_present = plist["Is Present"]
        ups_is_present = str(ups_is_present).replace('\n', r'\n')        
        ups_max_capacity = plist["Max Capacity"]
        ups_max_capacity = str(ups_max_capacity).replace('\n', r'\n')        
        ups_name = plist["Name"]
        ups_name = str(ups_name).replace('\n', r'\n')
        ups_power_source_id = plist["Power Source ID"]
        ups_power_source_id = str(ups_power_source_id).replace('\n', r'\n')        
        ups_power_source_state = plist["Power Source State"]
        ups_power_source_state = str(ups_power_source_state).replace('\n', r'\n')             
        ups_product_id = plist["Product ID"]
        ups_product_id = str(ups_product_id).replace('\n', r'\n')             
        ups_required_voltage = plist["Set Required Voltage"]
        ups_required_voltage = str(ups_required_voltage).replace('\n', r'\n')           
        ups_time_to_empty = plist["Time to Empty"]
        ups_time_to_empty = str(ups_time_to_empty).replace('\n', r'\n')            
        ups_transport_type = plist["Transport Type"]
        ups_transport_type = str(ups_transport_type).replace('\n', r'\n')             
        ups_type = plist["Type"]
        ups_type = str(ups_type).replace('\n', r'\n')           
        ups_vendor_id = plist["Vendor ID"]
        ups_vendor_id = str(ups_vendor_id).replace('\n', r'\n')           
        ups_input_voltage = int(plist["Voltage"])
        ups_input_voltage = str(ups_vendor_id).replace('\n', r'\n')               

        ups = GaugeMetricFamily(
            'ups',
            'ups_current_capacity',
             labels=['ups_is_charging', 'ups_is_present', 'ups_max_capacity', 'ups_name', 'ups_power_source_state', 'ups_required_voltage', 'ups_time_to_empty', 'ups_type', 'ups_input_voltage', 'ups_internal_failure', 'ups_enabled_audible_alarm' ])
        label_values = [ups_is_charging, ups_is_present,ups_max_capacity, ups_name, ups_power_source_state, ups_required_voltage, ups_time_to_empty, ups_type, ups_input_voltage, ups_internal_failure, ups_enabled_audible_alarm]

        # Browse the dictionary containing the json returned by the api, to link each metric to a dictionary key
        ups.add_metric(label_values, ups_current_capacity)
        yield ups
if __name__ == "__main__":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    print(time.strftime("%H:%M:%S"), "- Exporter launched: port 9902")
    start_http_server(9902)
    REGISTRY.register(JsonCollector())
    while True: time.sleep(1)
