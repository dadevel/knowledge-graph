---
title: Base64 File Transfer
---

[[notes/file-transfer/index]] by encoding binary data in Base64.

Linux Coreutils.

~~~ bash
base64 -w0 ./input.bin > ./output.txt
base64 -d ./input.txt > ./output.bin
~~~

Python.

~~~ bash
python3 -m base64 -e ./input.bin > ./output.txt
python3 -m base64 -d ./input.txt > ./output.bin
~~~

PowerShell.

~~~ powershell
[System.IO.File]::WriteAllText("$(pwd)\output.txt", [System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes("$(pwd)\input.bin")))
[System.IO.File]::WriteAllBytes("$(pwd)\output.bin", [System.Convert]::FromBase64String([System.IO.File]::ReadAllText("$(pwd)\input.txt")))
~~~

Windows builtin.

~~~ bat
certutil.exe -decode .\input.txt .\output.bin
~~~
