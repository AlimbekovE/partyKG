#!/bin/bash

envsubst '$$SERVER_NAME' < /etc/nginx/nginx-http.tmpl > /etc/nginx/nginx.conf
nginx -g 'daemon off;'