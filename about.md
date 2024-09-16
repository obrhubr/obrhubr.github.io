---
layout: about
title: About

favicon: favicon.png
---

{{ site.data.metadata.site.description }} ([Github](https://github.com/obrhubr))

Contact me @ <a>{{ site.data.metadata.person.contact }}</a>.

### Acknowledgements

My site's design was heavily inspired by [James Haydon's Blog](https://jameshaydon.github.io), which I discovered through HackerNews.

I could also not have built this site without [notion2md](https://github.com/echo724/notion2md).

The font I use on the site was taken from [xeiaso.net](https://xeiaso.net/) as detailed in [this article](https://xeiaso.net/blog/iaso-fonts/). Many thanks for providing this great font!

### Recommendations

I urge you to checkout the following blogs and sites:

{% assign sorted_recommendations = site.data.recommendations | sort: "name" %}
{% for rec in sorted_recommendations %}
 * [{{ rec.name }}]({{ rec.url }}) {% endfor %}