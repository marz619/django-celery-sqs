#!/usr/bin/env bash

curl -X POST localhost:8000/queue/ -d '{"failure_rate": 0.5, "message": "fifty-fifty"}'
curl -X POST localhost:8000/queue/ -d '{"failure_rate": 0.6, "message": "sixty-forty"}'
curl -X POST localhost:8000/queue/ -d '{"failure_rate": 0.75, "message": "three quarters"}'
curl -X POST localhost:8000/queue/ -d '{"failure_rate": 0.999999, "message": "six nines"}'
curl -X POST localhost:8000/queue/ -d '{"message": "100% failure"}'
curl -X POST localhost:8000/queue/ -d '{"failure_rate": "failure_rate", "message": "bad failure_rate value"}'
