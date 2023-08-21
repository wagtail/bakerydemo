FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY local.nginx.conf /etc/nginx/conf.d
