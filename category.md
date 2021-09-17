---
layout: post
title: Catégorie
permalink: /category/
content-type: eg
---

<style>
.category-content a {
    text-decoration: none;
    color: #4183c4;
}

.category-content a:hover {
    text-decoration: underline;
    color: #4183c4;
}
</style>

<main>
{% assign mydocs = site.notes | group_by: 'category' %}
{% for cat in mydocs %}
	{%- if cat.name != 'false' -%} 
<details>
<summary>{{ cat.name | capitalize | reverse }}</summary>
    <ul>
      {% assign items = cat.items | sort: 'title' %}
      {% for item in items %}
        <li><a href="{{ item.url }}">{{ item.title }}</a></li>
      {% endfor %}
    </ul>
</details>
{%- endif -%}
{% endfor %}
<br/>
<br/>
</main>