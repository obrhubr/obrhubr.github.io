---
layout: about
title: About

favicon: favicon.png
---

Hey, my name is {{ site.data.metadata.site.person.firstname }} ([Github](https://github.com/obrhubr)). I'm a developer from Austria.

### Work Experience

{% for work in site.data.metadata.person.work %}
 - [{{ work.company }}]({{ work.url }}) {{ work.description }} {% endfor %}

### Acknowledgements

My site's design was heavily inspired by [James Haydon's Blog](https://jameshaydon.github.io), which I discovered through HackerNews.

I could also not have built this site without [notion2md](https://github.com/echo724/notion2md).

The font I use on the site was taken from [xeiaso.net](https://xeiaso.net/) as detailed in [this article](https://xeiaso.net/blog/iaso-fonts/). Many thanks for providing this great font!

### Recommendations

I urge you to checkout the following blogs and sites:

 * [jameshaydon.github.io](https://jameshaydon.github.io)
 * [tom7.org](http://tom7.org/)
 * [qntm.org](https://qntm.org)
 * [maggieappleton.com](https://maggieappleton.com/)
 * [publicdomainreview.org](https://publicdomainreview.org/)
 * [www.thirtythreeforty.net](https://www.thirtythreeforty.net/)
 * [simonwillison.net](https://simonwillison.net/)
 * [fasterthanli.me](https://fasterthanli.me/)
 * [xeiaso.net](https://xeiaso.net/)