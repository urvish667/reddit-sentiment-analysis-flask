# Reddit Sentiment Analysis

Analyze Reddit comments' sentiment with ease using this Docker container. Extract valuable insights from Reddit discussions effortlessly.

## Features

- Perform sentiment analysis on Reddit comments.
- Generate pie charts to visualize sentiment distribution.
- Analyze keyword frequencies.
- Dockerized for easy deployment.

## Usage

To run the container, use the following command:

```shell
docker run -dit --name reddit-sentiment -p 5000:5000 -e MYSQL_USER=reddit -e MYSQL_PASSWORD=reddit -e MYSQL_DATABASE=reddit_db -e MYSQL_HOSTNAME=172.17.0.2 -e CLIENT_ID=<client_id> -e CLIENT_SECRET=<client_secret> -e USER_AGENT='<app-name>/<version> by <reddit-username>' reddit-sentiment-analysis
```

Ensure you've set all the required environment variables for Reddit API integration.

### Using MySQL Backend

You can set up the MySQL backend by using the official MySQL Docker image. Here's an example of how to run the MySQL container:

```shell
docker run -d --name mysql-db -e MYSQL_ROOT_PASSWORD=root-password -e MYSQL_USER=reddit -e MYSQL_PASSWORD=reddit -e MYSQL_DATABASE=reddit_db mysql:latest
```

Make sure to replace `root-password` with your desired root password and set the same MySQL credentials (`MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DATABASE`) in the Reddit Sentiment Analysis container environment variables.
