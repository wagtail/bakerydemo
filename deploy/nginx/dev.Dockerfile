FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY dev.nginx.conf /etc/nginx/conf.d
