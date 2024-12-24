#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
gunicorn -w 4 -b 0.0.0.0:5000 src.webapp:app
