#!/bin/bash
FILE1=$1
cd $FILE1
cargo run --release | setup/kafka_2.12-2.3.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic changes
