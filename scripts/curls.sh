#!/usr/bin/env bash

curl -X POST localhost:8000/queue/ -d '{"chance": 0.5, "message": "fifty-fifty"}'
curl -X POST localhost:8000/queue/ -d '{"chance": 0.5, "message": "fifty-fifty"}'
curl -X POST localhost:8000/queue/ -d '{"chance": 0.75, "message": "three quarters"}'
curl -X POST localhost:8000/queue/ -d '{"chance": 0.999999, "message": "six nines"}'
curl -X POST localhost:8000/queue/ -d '{"message": "absolute"}'
curl -X POST localhost:8000/queue/ -d '{"chance": "chance", "message": "bad chance"}'

