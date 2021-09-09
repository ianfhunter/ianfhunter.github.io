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

---
  
{: .note}    
> **Title**{: .ad-title-note}  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.   

{: .note}  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
  
{: .abstract}    
> **Abstract**{: .ad-title-abstract}  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
 
{: .abstract}   
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  


{: .todo}    
> **Notes**{: .ad-title-todo}  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
  
{: .todo}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
  
{: .tip}
> **Tip**{: .ad-title-tip}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .tip}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .done}
> **Success**{: .ad-title-done}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .done}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    

{: .question}
> **Question**{: .ad-title-question}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .question}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    

{: .warning}
> **warning**{: .ad-title-warning}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .warning}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    

{: .failure}
> **Failure**{: .ad-title-failure}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .failure}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    


{: .danger}  
> **Danger**{: .ad-title-danger}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .danger}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    

{: .bug}  
> **Bug**{: .ad-title-bug}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .bug}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    

{: .example}  
> **Example**{: .ad-title-example}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .example}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    

{: .quote}  
> **Quote**{: .ad-title-quote}
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.  

{: .quote}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.    


{: .note}    
> Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et *euismod nulla*.  
> **Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod nulla.**   
> $$1+2 = 3$$  
