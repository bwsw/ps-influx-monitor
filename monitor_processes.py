#!/usr/bin/env python3

import psutil
import os
import sys
import time
from influxdb import InfluxDBClient
import socket

influxHost = os.environ["INFLUX_HOST"]
influxPort = int(os.environ["INFLUX_PORT"])
influxDB = os.environ["INFLUX_DB"]
influxUser = os.environ["INFLUX_USER"]
influxPassword = os.environ["INFLUX_PASSWORD"]

influxClient = InfluxDBClient(influxHost, influxPort, influxUser, influxPassword, influxDB)

hostname = socket.gethostname()

sleep_time = 15
if len(sys.argv) > 1:
   sleep_time = int(sys.argv[1])

while True:
   time.sleep(sleep_time)
   influxPushRecord = []
   for proc in psutil.process_iter(attrs = ['pid','name', 'cpu_times', 'memory_info', 'gids', 'uids','ppid']):
     fields = proc.info
     tags = {}
     fields["pcpu.user"] = float(proc.info["cpu_times"].user)
     fields["pcpu.system"] = float(proc.info["cpu_times"].system)
     fields["pcpu.children_user"] = float(proc.info["cpu_times"].children_user)
     fields["pcpu.children_system"] = float(proc.info["cpu_times"].children_system)
     fields["pmem.rss"] = float(proc.info["memory_info"].rss)
     fields["pmem.vms"] = float(proc.info["memory_info"].vms)
     fields["pmem.shared"] = float(proc.info["memory_info"].shared)
     fields["pmem.lib"] = float(proc.info["memory_info"].lib)
     fields["pmem.data"] = float(proc.info["memory_info"].data)
     fields["pmem.dirty"] = float(proc.info["memory_info"].dirty)

     tags["puids.real"] = int(proc.info["uids"].real)
     tags["puids.effective"] = int(proc.info["uids"].effective)
     tags["puids.saved"] = int(proc.info["uids"].saved)
     tags["pgids.real"] = int(proc.info["gids"].real)
     tags["pgids.effective"] = int(proc.info["gids"].effective)
     tags["pgids.saved"] = int(proc.info["gids"].saved)
     tags["pid"] = proc.pid
     tags["ppid"] = proc.ppid()
     tags["name"] = proc.name()
     tags["exe"] = proc.exe()
     tags["cwd"] = proc.cwd()
     tags["cmdline"] = " ".join(proc.cmdline())
     tags["hostname"] = hostname

     del fields["memory_info"]
     del fields["cpu_times"]
     del fields["uids"]
     del fields["gids"]
     del fields["pid"]
     del fields["ppid"]
     del fields["name"]

     influxRecord = {
       "fields": fields,
       "tags": tags,
       "measurement": influxDB
     }
     influxPushRecord.append(influxRecord)

   influxClient.write_points(influxPushRecord)	

