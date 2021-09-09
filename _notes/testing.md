---
category: none
date: 09-09-2021
season: none
share: true
title: Admonition
---

# Admonition présentation  

Admonition work on this blog using CSS and IAL. It use : `{: .type}` and `{: .ad-title-type}`.
The script will add `**title**{: .ad-title-type}` if found `title:` in the admonition block.

It doesn't support :
- Collapse
- Color
- Icon
- Custom admonition (convert to note by default)
Collapse, color, and icon are just removed in the conversion.

The final admonition part will be :
```md
{: .admonition-type}
> **title**{: .ad-title-type}
> Word
> Word
```

If no title is found, the admonition will be one line, as that :
```md
{: .admonition-type}
> Admonition content
```

It also supports markdown and latex.


  
{: .note}    
> **Notes**{: .ad-title-note}  
> content  
  
{: .abstract}    
> **Notes**{: .ad-title-abstract}  
> content  
  
{: .todo}    
> **Notes**{: .ad-title-todo}  
> content  
  
{: .done}    
> content  
  
{: .note}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> **Testing mardkown Admonition**   
> $$1+2 = 3$$  
  
  
```python
print("hello")
```