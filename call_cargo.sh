#!/bin/bash
cd Desktop/Git/amnesia-demo

cargo run --release | setup/kafka_2.12-2.3.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic changes
