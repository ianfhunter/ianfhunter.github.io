---
author: ianfhunter
category: 1 technical
math: true
mermaid: true
share: true
tags:
- writing
---

```ad-info
This article is a continual WIP, where I will add particular things of note when coming up with solutions to the problems.
```


# The importance of sample cases
Small optimizations can sometimes break the logic of your code - so rather than waiting for a long run to finish, make sure you run your test cases first so you can fail early and fix it fast.


# Regex
Referring back to a group matched in regex again with `\1` (number corresponding with the captured group) helped detect recurring patterns

Partial capture `{0,2}` Allowed me to factor in recurring patterns that may clip at the end, e.g.
> 0.123456123456123


# Approaches
***Sometimes the 'ugly' way is the fastest***
A lot of the problems use repeated functions, like isPrime, isPandigital. Because these can be costly enough, it's probably worthwhile just generating a file with valid combinations, loading them in at the start and searching for them, rather than do the math each time.