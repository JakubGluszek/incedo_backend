#!/usr/bin/env bash

# for heroku deployment
uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port $PORT
