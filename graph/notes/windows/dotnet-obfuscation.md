---
title: .NET Obfuscation
---

Simple tricks for obfuscating .NET assemblies:

- open project in Visual Studio
- in right sidebar, right click on the project and select `Proprieties`
    - *Assembly Name* = random
    - *Platform target* = *Any CPU*
    - *Deterministic* = *no*
    - *File alignment* = *4096*
    - *Package ID* = random
    - *Title* = random
    - *Company* = random
    - *Product* = random
- rename namespaces and suspicious functions
- delete console help and logo
- remove functions and features that you don't need (!)
- build a release
