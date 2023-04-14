#!/bin/bash
# add your path
ps aux | grep jupyter-lab | grep -v grep | awk '{print $2}' | xargs kill -9
export PYTHONPATH="$PYTHONPATH:/data/yckj3980/llm_inference"
# start JupyterLab using an environment
nohup jupyter-lab > /data/yckj3980/llm_inference/log/jupyter.out &
