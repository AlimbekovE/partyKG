#!/bin/bash


cp /usr/src/app/supervisor/supervisor.conf /etc/supervisor.conf
#cp /usr/src/app/supervisor/worker.conf /etc/supervisor/conf.d/worker.conf

if [ "$DJ_DEBUG" == true ]
then
    cp /usr/src/app/supervisor/web-devel.conf /etc/supervisor/conf.d/web.conf
else
    cp /usr/src/app/supervisor/web-prod.conf /etc/supervisor/conf.d/web.conf
fi

supervisord -c /etc/supervisor.conf