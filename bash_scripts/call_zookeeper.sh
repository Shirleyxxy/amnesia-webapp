#!/bin/bash
FILE1=$1
cd $FILE1
setup/kafka_2.12-2.3.0/bin/zookeeper-server-start.sh setup/kafka_2.12-2.3.0/config/zookeeper.properties