---
title: Chisel
---

Project: [github.com/jpillora/chisel](https://github.com/jpillora/chisel/)

# Setup

~~~ bash
go install github.com/jpillora/chisel@latest
~~~

Cross-compile an obfuscated version for Windows ([source](https://mobile.twitter.com/snovvcrash/status/1540395267064741890)).

~~~ bash
go install mvdan.cc/garble@latest
git clone --depth 1 https://github.com/jpillora/chisel
cd ./chisel
CGO_ENABLED=1 GOOS=windows GOARCH=amd64 garble -literals -tiny build -trimpath
file ./chisel.exe
~~~
