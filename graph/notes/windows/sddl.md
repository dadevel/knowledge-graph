---
title: SDDL
---

[[notes/windows/index]] Security Descriptor Definition Language

Format: `ACE_TYPE;ACE_FLAGS;RIGHTS;OBJECT_GUID;INHERIT_OBJECT_GUID;ACCOUNT_SID`

Example: `(A;;RPWPCCDCLCSWRCWDWOGA;;;S-1-1-0)`

Result:

~~~
Type:
A = ACCESS_ALLOWED_ACE_TYPE

Access rights:
RP = ADS_RIGHT_DS_READ_PROP
WP = ADS_RIGHT_DS_WRITE_PROP
CC = ADS_RIGHT_DS_CREATE_CHILD
DC = ADS_RIGHT_DS_DELETE_CHILD
LC = ADS_RIGHT_ACTRL_DS_LIST
SW = ADS_RIGHT_DS_SELF
RC = READ_CONTROL
WD = WRITE_DAC
WO = WRITE_OWNER
GA = GENERIC_ALL

SID:
S-1-1-0
~~~

Untested tools:

- [sddl_py](https://github.com/t94j0/sddl_py), SDDL parser
- [SdDumper](https://github.com/daem0nc0re/TangledWinExec/tree/main/SdDumper), SDDL parser

References:

- [ACE Strings](https://learn.microsoft.com/en-us/windows/win32/secauthz/ace-strings)
- [A brief summary of the various versions of the Security Descriptor Definition Language](http://web.archive.org/web/20221130222211/https://devblogs.microsoft.com/oldnewthing/20220510-00/?p=106640)
