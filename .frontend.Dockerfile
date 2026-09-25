FROM nginx:alpine

COPY frontend/ /usr/share/nginx/html/

RUN cp /usr/share/nginx/html/login.html /usr/share/nginx/html/index.html

EXPOSE 80
