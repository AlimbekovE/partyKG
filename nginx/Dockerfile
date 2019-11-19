FROM nginx:1.17.2
COPY nginx.tmpl /etc/nginx/nginx.tmpl
COPY nginx-http.tmpl /etc/nginx/nginx-http.tmpl
COPY gzip.conf /etc/nginx/gzip.conf
COPY proxy.conf /etc/nginx/proxy.conf
COPY start.sh /usr/local/bin/start.sh
COPY start-http.sh /usr/local/bin/start-http.sh
