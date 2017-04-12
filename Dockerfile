FROM python:2.7.13

ADD . /project
RUN sudo apt-get update
RUN sudo apt-get install -y --no-install-recommends libssl-dev \
                    openssl \
                    python-openssl \
                    zlib1g 
RUN sudo pip install --upgrade pip
RUN sudo pip install pyOpenSSL
RUN chmod a+x /project/src/run.sh
EXPOSE 8000
CMD ["/project/src/run.sh"]
