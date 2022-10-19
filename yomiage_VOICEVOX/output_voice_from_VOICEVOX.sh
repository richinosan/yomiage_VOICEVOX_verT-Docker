#!/bin/sh
curl -s -H "Content-Type: application/json" -X POST -d @tmp/query.json host.docker.internal:50021/synthesis?speaker=$1 > tmp/tmp_voice.wav