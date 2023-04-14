#!/bin/bash
ps aux | grep jupyter-lab | grep -v grep | awk '{print $2}' |xargs kill -9

