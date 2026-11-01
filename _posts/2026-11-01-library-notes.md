---
author: ianfhunter
category: 1 technical
math: true
mermaid: true
share: true
tags:
- coding
---

```ad-info
This article is a continual WIP, where I will add particular things of note as I develop
```

# Make
Make doesn't export defaulted variables to subshells, only to sub-makes


# Python
## CPPYY

Avoid using `const char *` and prefer `std::string`

(Cppyy cannot determine the owner of memory with const char \* . std::string is generally preferrable in all cases according to developers)