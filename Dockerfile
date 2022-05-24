FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libpq-dev
# We copy just the requirements.txt first to leverage Docker cache
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
COPY . /app
CMD [ "python3", "run.py" ]