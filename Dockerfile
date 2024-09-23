# Build the Jekyll site
FROM ruby:3.1.3-bullseye AS builder

# Install js runtime for katex
RUN apt-get install -y curl gpg
RUN curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install -y nodejs

WORKDIR /usr/src/app

COPY Gemfile .

RUN bundle install

COPY . .

ENV JEKYLL_ENV=production
RUN bundle exec jekyll build

# Serving the site
FROM nginx:stable-alpine

COPY --from=builder /usr/src/app/_site /usr/share/nginx/html
COPY _nginx/nginx.conf /etc/nginx/conf.d/default.conf