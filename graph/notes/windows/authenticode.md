---
title: Microsoft Authenticode
---

Authenticode provides code-signing on [[notes/windows/index]].

Notes:

- code signing for `.exe`, `.dll` and `.sys` binaries
- certificate and signature are embedded in the binary
- some PE header regions are excluded from the signature and can be modified without invalidating it which should allow to bypass hash-based block lists

Untested tools:

- [gSigFlip](https://github.com/akkuman/gSigFlip)
- [SigFlip](https://github.com/med0x2e/SigFlip)

References:

- [Changing a Signed Executable without Altering Windows Digital Signatures](http://web.archive.org/web/20230921104045/https://blog.barthe.ph/2009/02/22/change-signed-executable/)
- [Authenticode Stuffing Tricks](http://web.archive.org/web/20230604014312/https://vcsjones.dev/authenticode-stuffing-tricks/)
- [twitter.com/wdormann/status/1643336761051869185](https://twitter.com/wdormann/status/1643336761051869185)
- [Caveats for Authenticode Code Signing](https://web.archive.org/web/20150426192725/http://blogs.msdn.com/b/ieinternals/archive/2014/09/04/personalizing-installers-using-unauthenticated-data-inside-authenticode-signed-binaries.aspx)
