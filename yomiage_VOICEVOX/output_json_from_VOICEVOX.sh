#!/bin/sh
curl -s -X POST "host.docker.internal:$1/audio_query?text=$2&speaker=$3" > tmp/query.json