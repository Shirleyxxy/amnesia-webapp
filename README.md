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



- Second Implementation:
  - Step 1: Move to the right directory `cd amnesia-websocket`.
  - Step 2: Start the Cargo server by running `cargo run --release`.
  - Step 3: Point the browser to `localhost:8000` to launch the web app. The web app is able to talk to the Differential Dataflow model.
