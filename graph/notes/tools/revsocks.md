---
title: revsocks
---

Project: [github.com/kost/revsocks](https://github.com/kost/revsocks)

# Setup

~~~ bash
git clone --depth 1 https://github.com/kost/revsocks.git
cd ./revsocks
go mod init github.com/brimstone/rsocks/v2
go mod tidy
go build
GOOS=windows go build
~~~
