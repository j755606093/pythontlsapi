FROM ubuntu:16.04

RUN sudo apt-get update 
RUN sudo apt-get install -y --no-install-recommends \
         python python-dev python-pip \
         openssl \
         zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

ADD . /project
RUN chmod a+x /project/src/run.sh
EXPOSE 8000
CMD ["/project/src/run.sh"]
