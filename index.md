---
layout: page
title: Home
excerpt: "X"
search_omit: true
---

### tl;dr

If you want to get started immediately then just clone the repo and explore the [NSPN_CorticalMyelination_AnalysisWrapper.py](https://github.com/KirstieJane/NSPN_WhitakerVertes_PNAS2016/blob/master/NSPN_CorticalMyelination_AnalysisWrapper.py) file.


### What's in this repo

This repository contains all the data, analysis code and results (including figures and tables) from the NSPN Manuscript "Adolescence is associated with genomically patterned consolidation of the hubs of the human brain connectome". A write up of all the different files and naming structures can be found at the wiki page on [file descriptions](https://github.com/KirstieJane/NSPN_WhitakerVertes_PNAS2016/wiki/File-descriptions).

### Support

First check out the wiki to see if there's any documentation that might be helpful.

The next stop are the [current issues](https://github.com/KirstieJane/NSPN_WhitakerVertes_PNAS2016/issues) just in case someone has already asked your question already.

If they haven't please [open a new issue](https://github.com/KirstieJane/NSPN_WhitakerVertes_PNAS2016/issues/new) and provide as much information as you can. [Kirstie](https://github.com/KirstieJane) will get back to you within a couple of days.

### FAQs

#### Why figshare *and* GitHub?
The repository was created upon acceptance of the paper by PNAS by downloading the project files from [figshare](https://figshare.com/projects/NSPN_Adolescent_consolidation_of_human_connectome_hubs/4710). The Figshare project ensures that our data and code will be stored in perpetuity, but the goal of this GitHub repository is to make it easy for you to both access the files and to ask for help with the process. [Wiki documentation](https://github.com/KirstieJane/NSPN_WhitakerVertes_PNAS2016/wiki) will be built as necessary in response to your questions.


<ul class="post-list">
{% for post in site.categories.articles %}
  <li><article><a href="{{ site.url }}{{ post.url }}">{{ post.title }} <span class="entry-date"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time></span>{% if post.excerpt %} <span class="excerpt">{{ post.excerpt | remove: '\[ ... \]' | remove: '\( ... \)' | markdownify | strip_html | strip_newlines | escape_once }}</span>{% endif %}</a></article></li>
{% endfor %}
</ul>
