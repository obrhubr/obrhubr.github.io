# Build the Jekyll site
FROM jekyll/jekyll:3.8 AS builder

WORKDIR /srv/jekyll
COPY . .
RUN jekyll build

# Serving the site
FROM nginx:stable-alpine

COPY --from=builder _site /usr/share/nginx/html
COPY _nginx/nginx.conf /etc/nginx/conf.d/default.conf