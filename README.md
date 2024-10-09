Set up a `Kafka` cluster with Zookeeper, to handle streaming data. It uses a Cassandra database as a sink, but you could easily modify this part.

![kafka-spotify](https://github.com/user-attachments/assets/d6a1a4b1-33cc-476d-a34b-41325bde66a4)

## Setup

### 1. Clone the repo and go to the kafka folder
```bash
git clone https://github.com/n-traore/private-dockerfile-compose-examples.git && \
cd private-dockerfile-compose-examples/kafka/kafka-spotify
```

### 2. Run this command so your .env is not commited to version control
```bash
git update-index --assume-unchanged .env
```

### 3. Populate the .env file with your values


### 4. Create a one node Cassandra cluster using docker and create the Keyspace and tables
```bash
docker run --rm --name cassandra_sink -d cassandra:3.11.5
docker cp cassandra-sink.cql cassandra_sink:/

# wait a few seconds for cassandra to be reachable, then run
docker exec -i cassandra_sink cqlsh -f cassandra-sink.cql
```

To check that everything went well, you can connect to the container and describe the table like this :
```bash
docker exec -it cassandra_sink cqlsh
describe sink.spotify_playlist
```

### 5. Run Kafka
The first step is to choose whether you want to run a single node or a multi-nodes cluster.

> For the single node, run this command : 
```bash
# Start single node cluster
docker compose -f docker-compose.zookeeperkafka.yml up -d
docker network connect kafka_net cassandra_sink
```
To check that everything went well : `docker compose -f docker-compose.zookeeperkafka.yml logs broker | grep started`

> For multi-nodes, run this command : 
```bash
# Start 3 nodes cluster
docker compose -f docker-compose.zookeeperkafka_multi.yml up -d
docker network connect kafka_net cassandra_sink
```

Then create the producer and consumer that will stream data to the cluster. Here we have defined the producer and consumer as simple Python apps that you can run using the following command :
```bash
docker compose up
```
This will run on the foreground so you can see the messages arrive on the console every 10 seconds. Stop using `ctrl+c`.


You can view the cluster in UI with kafdrop by going to [http://localhost:9010](http://localhost:9010)  

![image](https://github.com/user-attachments/assets/ef51539e-98c3-440d-a565-27c7231dc442)
![image](https://github.com/user-attachments/assets/4a0d7b83-f00b-4fb9-8462-01dfb0ee5184)


### 6. Clean-up
Stop and delete all containers. For example, for cassandra and the multi-nodes cluster containers :
```bash
docker stop cassandra_sink
docker compose -f docker-compose.zookeeperkafka_multi.yml down
```
