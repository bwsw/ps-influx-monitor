# ps-influx-monitor

Script loads data from process statistics (PS) to InfluxDB to be visualized in Grafana

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
      "measurement": "ps",
      "policy": "default",
      "query": "SELECT sum(\"pmem.rss\")/8 FROM \"ps\" WHERE $timeFilter GROUP BY time($interval), \"puids.effective\" fill(null)",
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
