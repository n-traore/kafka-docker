Set up a `Kafka` cluster with Zookeeper, to handle streaming data. It uses a Cassandra database as a sink, but you could easily modify this part.

![image](https://github.com/user-attachments/assets/7756442d-5300-4c9d-b4c4-5064c5958060)


## Setup

### 1. Clone the repo and go to the kafka folder
```bash
git clone https://github.com/n-traore/kafka-docker.git && cd kafka-docker
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

![image](https://github.com/user-attachments/assets/4e8365b1-79a7-4dda-942b-581dccf4bb6f)
![image](https://github.com/user-attachments/assets/f70896e0-9620-4cb8-9143-75682b2a7318)



### 6. Clean-up
Stop and delete all containers. For example, for cassandra and the multi-nodes cluster containers :
```bash
docker stop cassandra_sink
docker compose -f docker-compose.zookeeperkafka_multi.yml down
```
