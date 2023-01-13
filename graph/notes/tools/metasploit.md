---
title: Metasploit
---

Project: [github.com/rapid7/metasploit-framework](https://github.com/rapid7/metasploit-framework/)

# Usage

Set a variable in the context of the current module.

~~~
show options
set KEY VALUE
~~~

Set variable globally.

~~~
setg KEY VALUE
~~~

Set exploit target type (OS, OS version).

~~~
show targets
set target N
~~~

Put foreground shell to background.

~~~
background
~~~

Bring background shell back to foreground.

~~~
session -l
session -i N
~~~
