#!/bin/bash
FILE1=$1
cd $FILE1
setup/kafka_2.12-2.3.0/bin/kafka-server-start.sh setup/kafka_2.12-2.3.0/config/server.properties