#!/bin/sh
curl -s -X POST "host.docker.internal:50021/audio_query?text=$1&speaker=$2" > tmp/query.json