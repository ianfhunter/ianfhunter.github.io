---
author: ianfhunter
category: 1 technical
math: true
mermaid: true
share: true
tags:
- avrae
---

# Argument Parsing

```python
a = argparse(&ARGS&)
``` 
Grab arguments after arguments with a.last('name')  or whatever your variable is called.

```python
a = argparse(&ARGS&).last()
``` 
Grabs only the last entry of that argument

```python
a = argparse(&ARGS&).get('t')
``` 
Grab all the targets and put them in a list 

# Maps