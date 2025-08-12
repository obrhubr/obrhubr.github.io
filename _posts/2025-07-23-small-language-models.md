---
layout: page
title: "A Practical (and Incomplete) History of Language Models"
time: 5 minutes
published: 2025-07-23
colortags: [{'id': '4260119c-7ec5-48b3-ba5b-96f4335cdc7f', 'name': 'AI', 'color': 'yellow'}, {'id': '805abdfa-25d7-4253-b70a-011688c45da1', 'name': 'Statistics', 'color': 'blue'}]
tags: ['AI', 'Statistics']
permalink: small-language-models
favicon: small-language-models/favicon.png
excerpt: "This post is a little history lesson in the world of natural language processing. It should give a pretty practical overview of techniques (Markov Chains, BPE, GPTs) used to generate text since 1948 (Claude Shannon’s seminal paper) to today’s LLMs."
short: False
sourcecode: 
hn: 
math: True
image: assets/small-language-models/preview.png
---

> An attempt will be made to find how to make machines use language, form abstractions and concepts, solve kinds of problems now reserved for humans, and improve themselves. We think that a significant advance can be made in one or more of these problems if a carefully selected group of scientists work on it together for a summer. - [J. McCarthy, Dartmouth AI workshop proposal, 1955](http://jmc.stanford.edu/articles/dartmouth/dartmouth.pdf)

Turns out, it wasn’t actually that easy. A few years before the workshop, in 1949, [Alan Turing](https://en.wikipedia.org/wiki/Alan_Turing) devised the [Turing test](https://en.wikipedia.org/wiki/Turing_test), which measures a machine’s capabilities of using language. We now have, 75 years after it’s creation, [empirical proof of machines passing a rigorous Turing test in a controlled setting](https://arxiv.org/pdf/2503.23674), with 73% of judges mistaking GPT-4.5 for a human. That’s exactly **139 summers** more than J. McCarthy thought.

We’ve come a long way since the simple lookup-table-like system developed for [ELIZA](https://de.wikipedia.org/wiki/ELIZA) in 1966 (which did not pass the Turing test). I attempted to sum up my research into techniques used for language models in this post.

## Markov Chains

[Claude Shannon](https://en.wikipedia.org/wiki/Claude_Shannon), one of the original attendees of the Dartmouth summer workshop used [Markov Chains](https://en.wikipedia.org/wiki/Markov_chain) to approximate text in his 1949 paper *[A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)*. While he worked with character level Markov chains, we’ll also consider word and token level chains.

Markov Chains model stochastic processes. They model the way a random system - the weather for example - evolves from one state to another. If it’s `sunny`, there’s then a certain probability for `cloudy`, and from `cloudy` it’s more likely to get `rainy`. A Markov chain can be “trained” on a set of examples to approximate these probabilities.

![<p>Weather modeling Markov chain visualised.</p>](/assets/small-language-models/7b3d212c7707151715e539b9ea361e84.webp)

Because Markov Chains are essentially directed, weighted graphs, they can be visualised as matrices. The following heatmap shows the probability of a character appearing after another. Notice for example, that after `q` there is almost always a `u`.

![<p>Heatmap visualisation of a second order, character level, Markov chain, trained on Shakespeare.</p>](/assets/small-language-models/d55fcc549577120ac1fcd58f897f639e.webp)

The output of a model like this is essentially gibberish (text like “dw ci onerey gomilver” won’t exactly convince human judges in a Turing test) as knowing the single preceding character isn’t very useful to predict the next.

![<p>Comparison of the number of characters of context, the output produced by the Markov Chain and the size of the model.</p>](/assets/small-language-models/c6f543fefd07d494aff8a15cba447424.webp)

We can increase the size of the context (order of the model) to 3, 4 or even 6 characters, which of course massively increases the memory footprint of our markov chain matrix. The size of the Markov Chain grows $$ O(k^n) $$ which makes it impossible to provide more than a few dimensions of context.

There’s also the issue that, as we give more and more context, the output will slowly approximate the training corpus. This is especially noticeable for word-level chains, as n-grams of 4 or 5 words will be highly unique in a moderately sized text.

## Byte Pair Encoding

Training a Markov Chain on character level data has the consequence that the model can (and will) produce anything (from these characters). That is just a bit too much freedom to generate useful text. Using word-level data is a big constraint, as the model will never be able to generate any “new words” or declinations. It’s entirely limited to the words that were in the training corpus.

This is where tokens come in. They serve as a nice middle-ground between characters and words as they are usually more like syllables. You don’t get complete gibberish, but not all freedom has been removed. LLMs operate on token level data, you can [play with GPT tokenizers on their website](https://platform.openai.com/tokenizer).

The state of the art tokenizing algorithm is called byte pair encoding (BPE). A very readable implementation was provided by [Andrej Karpathy](https://karpathy.ai/) with [minBPE](https://github.com/karpathy/minbpe). The basic premise of BPE is the following:

1. Split the input into individual characters.

1. Go through the entire input in groups of two and count the occurrences of pairs.

1. Take the most frequent pair and merge it (`q` and `u` becomes `qu`) and add it as a new token.

1. Repeat from step 2. for the new list of tokens.

![<p>Showing how BPE works with a simple example.</p>](/assets/small-language-models/487d193eaf9cb381d43c667783426b25.webp)

Less frequent combinations will be represented using smaller tokens. BPE also doubles as a compression algorithm.

Applying BPE to the same dataset used above, produces tokens like `ing`, `for`, `and`, etc… The output is still meaningless, but it looks more like actual human language and isn’t a word for word reproduction of the corpus, all using only a single token of context: first citizen: “prithee now arrestthe otherincious lowd friendsthis doublecall”.

## GPTs

Now that we are operating on tokens, we’re essentially pretty close to modern LLMs. When we are working with a context of two or three tokens, they are all weighted equally, which is not ideal. Instead, we would like to change the output probabilities based on the current word and how it relates to those before it.

This is what LLMs do. A generative pre-trained transformer uses a mechanism known as [self-attention](https://en.wikipedia.org/wiki/Attention_(machine_learning)) to assign weights to the words in the context and have them interact with each other. Check out [Amanvir’s](https://amanvir.com/) [visualisation of the different attention heads in GPT-2](https://amanvir.com/gpt-2-attention) to get an intuition for this process. I also highly recommend checking out Andrej Karpathy’s [minGPT](https://github.com/karpathy/minGPT/tree/master) to understand GPTs.

After training a small GPT on the same Shakespeare text as before, tokenized into `10255` tokens with my re-implementation of Karpathy’s `minBPE`, we get the following results.

![<p>Output of our “small language model”.</p>](/assets/small-language-models/b1a2872f2cd73ec20b8309081ff34853.webp)

<br/>

