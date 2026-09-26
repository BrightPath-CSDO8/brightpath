FROM nginx:alpine
COPY frontend/ /usr/share/nginx/html/
RUN cp /usr/share/nginx/html/login.html /usr/share/nginx/html/index.html
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/server_tokens.conf
RUN printf 'add_header X-Frame-Options "SAMEORIGIN" always;\nadd_header X-Content-Type-Options "nosniff" always;\nadd_header Referrer-Policy "strict-origin-when-cross-origin" always;\n' > /etc/nginx/conf.d/security_headers.conf
EXPOSE 80
