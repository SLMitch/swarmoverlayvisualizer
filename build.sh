#!/bin/bash

docker build -t slmitch/swarmoverlayvisualizer-webserver webserver
docker build -t slmitch/swarmoverlayvisualizer-agent agent

