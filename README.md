# Process Monitoring Utility

Monitoring utility which discovers process information and stores it in an InfluxDB database. The data can be visualized in Grafana.


## Installation

### Install dependencies

```bash
$ /usr/bin/env python3 -m pip install --user --upgrade pip && /usr/bin/env python3 -m pip install --user -r requirements.txt
```

### Install influx with docker and create a configuration file

```bash
$ mkdir -p tmp/{config,data}
# generate config (don't forget to change it next if necessary)
$ sudo docker run --rm influxdb influxd config > tmp/config/influxdb.conf
```

### Run influxdb server

```bash
$ sudo docker run -p -d --restart always --name influx 8086:8086 \
      -v $PWD/tmp/config:/etc/influxdb:ro \
      -v $PWD/tmp/data:/var/lib/influxdb \
      influxdb -config /etc/influxdb/influxdb.conf
```

### Open a console to db (other terminal) and create a database where data will be stored

```baseh
$ sudo docker run -it --rm --link influx influxdb influx -host influx
> create database psstat
> exit
```

### Launch monitoring

```bash
# RUN AS root to see full process information
$ su
# create envars
(root) $ export INFLUX_HOST=localhost
(root) $ export INFLUX_PORT=8086
(root) $ export INFLUX_USER=dummy
(root) $ export INFLUX_PASSWORD=dummy
(root) $ export INFLUX_DB=psstat
(root) $ ./monitor_processes.py [DELAY in secs, default 15 secs]
```

### Grafana Notes

Example Grafana Panel JSON which enables monitoring of RAM usage for every system user:

```json

{
  "aliasColors": {},
  "bars": false,
  "datasource": "PS",
  "fill": 1,
  "id": 1,
  "interval": "120s",
  "legend": {
    "alignAsTable": false,
    "avg": false,
    "current": false,
    "max": false,
    "min": false,
    "show": true,
    "total": false,
    "values": false
  },
  "lines": true,
  "linewidth": 1,
  "links": [],
  "nullPointMode": "null",
  "percentage": false,
  "pointradius": 5,
  "points": false,
  "renderer": "flot",
  "seriesOverrides": [],
  "span": 12,
  "stack": false,
  "steppedLine": false,
  "targets": [
    {
      "dsType": "influxdb",
      "groupBy": [
        {
          "params": [
            "$interval"
          ],
          "type": "time"
        },
        {
          "params": [
            "puids.effective"
          ],
          "type": "tag"
        },
        {
          "params": [
            "null"
          ],
          "type": "fill"
        }
      ],
      "measurement": "psstat",
      "policy": "default",
      "query": "SELECT sum(\"pmem.rss\")/8 FROM \"psstat\" WHERE $timeFilter GROUP BY time($interval), \"puids.effective\" fill(null)",
      "rawQuery": true,
      "refId": "A",
      "resultFormat": "time_series",
      "select": [
        [
          {
            "params": [
              "pmem.rss"
            ],
            "type": "field"
          },
          {
            "params": [],
            "type": "sum"
          }
        ]
      ],
      "tags": [],
      "alias": ""
    }
  ],
  "thresholds": [],
  "timeFrom": null,
  "timeShift": null,
  "title": "Memory Usage By User",
  "tooltip": {
    "shared": false,
    "sort": 0,
    "value_type": "individual"
  },
  "type": "graph",
  "xaxis": {
    "mode": "time",
    "name": null,
    "show": true,
    "values": []
  },
  "yaxes": [
    {
      "format": "decbytes",
      "label": null,
      "logBase": 1,
      "max": null,
      "min": null,
      "show": true
    },
    {
      "format": "short",
      "label": null,
      "logBase": 1,
      "max": null,
      "min": null,
      "show": true
    }
  ]
}

```
