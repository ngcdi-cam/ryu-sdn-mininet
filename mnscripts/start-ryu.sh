#!/bin/bash
cp /mnscripts/multipath.py /usr/local/lib/python3.7/site-packages/ryu/app/
PYTHONPATH=. /usr/local/bin/ryu run --observe-links /usr/local/lib/python3.7/site-packages/ryu/app/gui_topology/gui_topology.py /usr/local/lib/python3.7/site-packages/ryu/app/multipath.py
