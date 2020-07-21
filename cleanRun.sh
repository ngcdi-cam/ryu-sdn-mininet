#!/bin/bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker volume rm influxdb1_datest1
