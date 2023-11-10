---
layout: page
title: How to try to build a chess engine and fail

time: 10 minute
published: 2023-11-10

tags: CS Engines C#

excerpt_separator: <!--more-->

---

A Chess-AI is something of a rite of passage for every software engineer, as is a snake clone or a calculator console application. If you did not try to build one yet, you are certainly missing out (or preserving your own sanity, whatever you prefer). Between the [chessprogrammingwiki.org](https://www.chessprogramming.org/Main_Page) and other online ressources this is now a pretty well explored field, but that is not to say that innovation is impossible and nothing changed since the days of Deep Blue (the first ever chess computer the officially beat a grandmaster). 

<!--more-->
{% highlight json %}
{
	"test": "test"
}
{% endhighlight %}

In recent years Stockfish, the most advanced computer chess engine, has gotten a major upgrade in the form of a NNUE, a fast neural network of sorts which is used as it’s evaluation function. An evaluation function does exactly what it sounds like, it is used by the engine to evaluate the current position.

Today I would group chess engines into two categories: “explore the most possibilities as fast as possible” (Stockfish) and “have a very sophisticated evaluation function in the form of a neural network” (Leela Chess Zero).