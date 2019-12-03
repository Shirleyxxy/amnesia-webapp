#!/bin/bash
cd Desktop/Git/amnesia-demo

setup/kafka_2.12-2.3.0/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic changes > amnesia_result.json