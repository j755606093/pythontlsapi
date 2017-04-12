FROM python:2.7.13

RUN apt-get update 
RUN apt-get install -y --no-install-recommends \
       openssl  \
       zlib1g-dev  \
    && rm -rf /var/lib/apt/lists/*

ADD . /project
RUN chmod a+x /project/src/run.sh
EXPOSE 8000
CMD ["/project/src/run.sh"]
