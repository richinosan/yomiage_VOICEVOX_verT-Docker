#!/bin/sh
curl -s -X GET "host.docker.internal:$1/speakers" > tmp/speakers.json