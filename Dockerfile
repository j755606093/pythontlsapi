FROM python:2.7.9

ADD . /project
RUN pip install --upgrade pip
RUN chmod a+x /project/src/run.sh
EXPOSE 8000
CMD ["/project/src/run.sh"]
