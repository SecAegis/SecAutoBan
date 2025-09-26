FROM ubuntu AS download
RUN apt update && apt install --no-install-recommends -y git curl ca-certificates
RUN git clone --depth 1 https://github.com/SecAegis/SecAutoBan
ARG TARGETARCH
RUN curl -L -o gobgp.tar.gz $(curl -s https://api.github.com/repos/osrg/gobgp/releases/latest | grep browser_download_url | cut -d'"' -f4 | grep ${TARGETARCH})
RUN mkdir /gobgp && tar -xzf gobgp.tar.gz -C /gobgp gobgp gobgpd

FROM alpine
COPY --from=download /SecAutoBan/device/alarm /device/alarm
COPY --from=download /SecAutoBan/device/block /device/block
COPY --from=download /gobgp/gobgp /usr/bin/gobgp
COPY --from=download /gobgp/gobgpd /usr/bin/gobgpd
RUN apk update && apk add --no-cache py3-pip
RUN pip3 install --break-system-packages SecAutoBan requests RouterOS-api scapy
