FROM python:2.7.13

ADD . /project
RUN  apt-get update
RUN  apt-get install -y --no-install-recommends libssl-dev \
                    openssl \
                    python-openssl \
                    zlib1g 
RUN  pip install --upgrade pip
RUN  pip install pyOpenSSL
RUN chmod a+x /project/src/run.sh
EXPOSE 8000
CMD ["/project/src/run.sh"]
