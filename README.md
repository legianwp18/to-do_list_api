## Run the database service locally
To run the database service locally, we can type:
docker compose up -d db

You can check the status of the running container by typing:
docker ps

## Run Python app
docker compose up --build pythonapp

Now you can once again check the running containers:
docker ps -a
