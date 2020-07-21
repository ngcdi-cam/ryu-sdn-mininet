#!/bin/bash
service openvswitch-switch start
echo $MN_SCRIPT
echo $SDN_C1
python $MN_SCRIPT $SDN_C1
