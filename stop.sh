#!/bin/bash
PID=$(ps aux | grep app.py | grep -v grep | awk '{ print $2 }')
kill -9 $PID