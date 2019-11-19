#!/bin/bash

envsubst '$$SERVER_NAME' < /etc/nginx/nginx.tmpl > /etc/nginx/nginx.conf
nginx -g 'daemon off;'