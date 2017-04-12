FROM python:2.7.13

RUN apt-get update 
RUN sudo apt-get install -y --no-install-recommends \
        Python-openssl \
    && rm -rf /var/lib/apt/lists/*

ADD . /project
RUN chmod a+x /project/src/run.sh
EXPOSE 8000
CMD ["/project/src/run.sh"]
