FROM nginx:alpine
COPY frontend/ /usr/share/nginx/html/
RUN cp /usr/share/nginx/html/login.html /usr/share/nginx/html/index.html
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/server_tokens.conf
EXPOSE 80
