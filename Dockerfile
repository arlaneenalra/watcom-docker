# Watcom Docker Build Environment
#
# To build use:
# docker build -t lapinlabs/watcom .
FROM alpine:3.20
MAINTAINER Chris Salch <emeraldd.chris@gmail.com> 

LABEL description="An OpenWatcom V2 build environment."
ARG RELEASE="Current-build"

# Setup the build environment all in one pass. This helps us to reduce image
# size by doing cleanup in the same layer as the setup.
RUN apk add --no-cache --update --virtual .build-deps \
      curl \
      make \
      xxd \
    # Build and install Watcom package
    && cd /tmp \
    && curl -L https://github.com/open-watcom/open-watcom-v2/releases/download/$RELEASE/ow-snapshot.tar.xz -o current.tar.xz \
    && mkdir /opt/watcom \
    && cd /opt/watcom \
    && xzcat /tmp/current.tar.xz | tar xv \
    # Clean up after ourselves (do this in the same layer)
    && rm -rf /tmp/current.tar.xz \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

ENV WATCOM="/opt/watcom"
ENV PATH="$WATCOM/binl64:$WATCOM/binl:$PATH"
ENV EDPATH="$WATCOM/eddat"
ENV INCLUDE="$WATCOM/h"

CMD ["/bin/sh"]
