FROM python:3.8 as developer
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y gettext && \
                      apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /var/log/supervisor && \
    mkdir -p /etc/supervisor/conf.d && \
    mkdir -p /usr/src/app

WORKDIR /usr/src/app
ADD . /usr/src/app/
RUN chmod +x entrypoint.sh && pip3 install -r requirements.txt
RUN pip install gunicorn

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
FROM developer as production