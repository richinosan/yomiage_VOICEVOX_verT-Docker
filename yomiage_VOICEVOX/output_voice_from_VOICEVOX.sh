#!/bin/sh
curl -s -H "Content-Type: application/json" -X POST -d @tmp/query.json host.docker.internal:$1/synthesis?speaker=$2 > tmp/tmp_voice.wav