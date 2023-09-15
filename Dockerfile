FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y python3 pip python3-dev build-essential default-libmysqlclient-dev libffi-dev pkg-config

# Create a directory for your app
RUN mkdir -p /root/reddit-sentiment-analysis

# Set the working directory
WORKDIR /root/reddit-sentiment-analysis

# Copy your app files into the container
COPY app/ /root/reddit-sentiment-analysis/app/
COPY run.py /root/reddit-sentiment-analysis/run.py
COPY requirements.txt /root/reddit-sentiment-analysis/requirements.txt

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Specify the command to run your app
CMD ["python3", "run.py"]
