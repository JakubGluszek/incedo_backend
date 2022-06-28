#!/bin/sh
# for heroku deployment
uvicorn app.main:app --host 0.0.0.0 --port $PORT
