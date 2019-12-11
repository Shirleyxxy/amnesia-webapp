## Web App Demonstration of Amnesia

This web app serves to demonstrate the decremental update procedures for an item-based collaborative filtering model. Specifically, the web app will display the corresponding changes of history matrix, total item interactions, cooccurrence matrix, and item similarity matrix after removing (i.e. “forgetting”) and adding the data of a particular user.

#### Project Milestones

1. Illustrate the changes of the matrices given input JSON files.
2. Connect Differential Dataflow with the web app to display the real-time changes.
   - First implementation using `Flask` and `Apache Kafka`
   - Second implementation using `JavaScript` and `WebSocket`
3. Create a user interface so that users can interact with the web app.

#### Access the WebApp Demo

- First Implementation:
  - Step 1: Move to the right directory `cd amnesia-kafka`.
  - Step 2: untar kafka: `tar -xzf kafka_2.12-2.3.0.tgz`.
  - Step 3: Start the zookeeper server by running commands `setup/kafka_2.12-2.3.0/bin/zookeeper-server-start.sh setup/kafka_2.12-2.3.0/config/zookeeper.properties`.
  - Step 4: Open a new console, and start kafka server by running command `setup/kafka_2.12-2.3.0/bin/kafka-server-start.sh setup/kafka_2.12-2.3.0/config/server.properties`. (First time running may take a while to build)
  - (Optional) If first time running, create kafka topics by opening a new console and create topics within kafka cluster: else, skip to Step 5. 
    - Create kafka topics to feed in changes `setup/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic interactions`.
    - After finished, create another topic to receive updates: `setup/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic changes`.
    - If already created, will raise error indicating topics already created, then proceed to step 5.
  - Step 5: Open another console, launch differential dataflow and direct its output to kafka: `cargo run --release | setup/kafka_2.12-2.3.0/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic changes`.
  - Step 6: Run `python kafka_main.py`. Wait until local address returns in terminal (takes around 5s).
  - Step 7: Point the browser to `http://127.0.0.1:5000/` to launch the web app. The web app is able to talk to kafka cluster and Differential Dataflow model.

- Second Implementation:
  - Step 1: Move to the right directory `cd amnesia-websocket`.
  - Step 2: Start the Cargo server by running `cargo run --release`.
  - Step 3: Point the browser to `localhost:8000` to launch the web app. The web app is able to talk to the Differential Dataflow model.
