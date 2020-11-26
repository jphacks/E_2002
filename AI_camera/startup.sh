#!/bin/bash

cd /home/robins/darknet

FLASK_APP=server.py flask run --host=0.0.0.0

