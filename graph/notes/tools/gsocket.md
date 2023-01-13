---
title: gsocket
---

Project: [github.com/hackerschoice/gsocket](https://github.com/hackerschoice/gsocket)

# Setup

On Debian-based distros.

~~~ bash
curl -SLfo gsocket.deb https://github.com/hackerschoice/binary/raw/main/gsocket/latest/gsocket_1.4.38_all.deb
sudo apt install -y ./gsocket.deb
~~~

With Docker/Podman.

~~~ bash
podman run --rm -it --network host docker.io/hackerschoice/gsocket:latest --help
~~~

Build from source.

~~~ bash
apt install --no-install-recommends -y build-essential libssl-dev
curl -LO https://github.com/hackerschoice/gsocket/releases/download/v1.4.33/gsocket-1.4.33.tar.gz
tar -xzf gsocket-1.4.33.tar.gz
cd ./gsocket-1.4.33
./configure
make install
~~~
