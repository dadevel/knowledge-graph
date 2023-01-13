---
title: Windows Quirks
---

Random [[notes/windows/index]] tricks.

# Dotted Directory

Create a directory that can not be opened in Explorer ([source](http://web.archive.org/web/20230721012100/https://soroush.me/blog/2010/12/a-dotty-salty-directory-a-secret-place-in-ntfs-for-secret-files/)).

~~~ bat
mkdir test
cd test
mkdir ...::$index_allocation
echo calc.exe > "...::$index_allocation\malware.bat"
...::$index_allocation\malware.bat
cd ..
rmdir test /s
~~~

# Installer Detection Technology

32bit executables that contain `setup`, `update` or `install` in their name trigger an UAC prompt because Windows wants to run them with Administrator privileges for backwards compatibility reasons ([source](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-vista/cc709628(v=ws.10)#installer-detection-technology)).
