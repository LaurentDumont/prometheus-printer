#!/bin/bash

name="oh-no-its-on-fire-$RANDOM"
url='http://prom.northernsysadmin.com:9093/api/v1/alerts'

echo "firing up alert $name"

curl -XPOST $url -d @- <<EOF
[{
"labels": {
  "alertname": "$name",
  "severity": "warning-high",
  "instance": "$name.coldnorthadmin.com"
},
"annotations": {
  "summary": "POTATO - High latency is high!"
},
"generatorURL": "http://prometheus.int.example.net/<generating_expression>"
}]
EOF
