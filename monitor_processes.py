#!/usr/bin/python

import psutil
import os
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

while True:
	time.sleep(15)
	influxPushRecord = []
	for proc in psutil.process_iter(attrs = ['pid','name', 'cpu_times', 'memory_info', 'gids', 'uids','ppid']):
		fields = proc.info
		tags = {}
		fields["pcpu.user"] = proc.info["cpu_times"].user
		fields["pcpu.system"] = proc.info["cpu_times"].system
		fields["pcpu.children_user"] = proc.info["cpu_times"].children_user
		fields["pcpu.children_system"] = proc.info["cpu_times"].children_system
        	fields["pmem.rss"] = proc.info["memory_info"].rss
        	fields["pmem.vms"] = proc.info["memory_info"].vms
        	fields["pmem.shared"] = proc.info["memory_info"].shared
        	fields["pmem.lib"] = proc.info["memory_info"].lib
        	fields["pmem.data"] = proc.info["memory_info"].data
        	fields["pmem.dirty"] = proc.info["memory_info"].dirty

		tags["puids.real"] = proc.info["uids"].real
		tags["puids.effective"] = proc.info["uids"].effective
		tags["puids.saved"] = proc.info["uids"].saved
        	tags["pgids.real"] = proc.info["gids"].real
        	tags["pgids.effective"] = proc.info["gids"].effective
        	tags["pgids.saved"] = proc.info["gids"].saved
		tags["pid"] = proc.info["pid"]
		tags["ppid"] = proc.info["ppid"]
		tags["name"] = proc.info["name"]
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

# pp(influx_push_record)
