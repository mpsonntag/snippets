# BUILDER IMAGE
FROM golang:alpine AS binbuilder

RUN go version

RUN mkdir /build
COPY ./* /build/
WORKDIR /build
RUN go build

# RUNNER IMAGE
FROM alpine:latest

RUN mkdir -p /srv/tickserv

COPY --from=binbuilder /build/tickexp /srv/tickserv/

WORKDIR /srv/tickserv/

EXPOSE 8899
ADD docker_startup.sh /srv/tickserv/
RUN chmod +x ./docker_startup.sh
ENTRYPOINT ["./docker_startup.sh"]
