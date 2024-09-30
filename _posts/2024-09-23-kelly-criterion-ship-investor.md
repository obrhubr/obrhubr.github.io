---
layout: page
title: "Deriving the Kelly Criterion to maximise Profit"
time: 6 minutes
published: 2024-09-23
colortags: [{'id': '11658a68-3c22-4966-b5fe-93f7c296ba7e', 'name': 'Data Analysis', 'color': 'green'}, {'id': '28d7f40f-be75-455e-9d82-781b78d1548c', 'name': 'Games', 'color': 'pink'}, {'id': '805abdfa-25d7-4253-b70a-011688c45da1', 'name': 'Statistics', 'color': 'blue'}]
tags: ['Data Analysis', 'Games', 'Statistics']
permalink: kelly-criterion-ship-investor
favicon: kelly-criterion-ship-investor/favicon.png
excerpt: "If you want to put some fraction of your money into a risky venture, how much should you invest? In order to maximise long term wealth, the Kelly Criterion is often used to size the bet. This post shows how to derive the gambling formula from the Kelly Criterion."
short: False
sourcecode: "https://github.com/obrhubr/kelly-criterion"
math: True
---

In a fictional casino which offers even odds on a fair coin toss game, how much of your money should you invest? If you said anything other than 0, you’re leaving broke in most timelines.

The Kelly Criterion is a way of maximising the expected value of the logarithm of wealth by staking a specific portion of it on a series of bets. This general concept of maximising can be used to size what fraction of your capital to invest in a bet or to distribute your capital between a number of bets.

This post was inspired by [Entropic Thoughts](https://entropicthoughts.com/) incredible [series on the Kelly Criterion](https://entropicthoughts.com/the-misunderstood-kelly-criterion).

## So why the expected value of the logarithm of wealth?

The expected value of a bet $$ E[X] $$ doesn’t make sense in the real world, where your capital is limited and you can’t play until you win what you expected. Betting all your money on a razor thin edge might be worth it in theory, but in reality you’re as likely to lose and what are you going to invest with then?

To model the effect of compounding wins (and compounding losses) the logarithm of wealth is used. Let’s take the example of a simple even odds game with a binary output in which you invest half your money every turn. If you win, you get one and a half times your wealth, if you lose, you still have half your wealth. The expected value is 1, and thus in theory, playing an infinite number of times should net you zero losses.

$$ E[w] = 0.5w \cdot p + 1.5w \cdot (1 -  p)
\\
E[w] = 0.5w \cdot 0.5 + 1.5w \cdot 0.5 = 0.25w + 0.75w = 1w $$

Now, let’s compute the expected value of the logarithm of wealth:

$$ E[\log(X)] = p \cdot \log(0.5w) + (1 - p) \cdot \log(1.5w)
\\
E[\log(X)] = 0.5 \cdot \log(0.5) + 0.5 \cdot \log(w) + 0.5 \cdot \log(1.5) + 0.5 \cdot \log(w) \approx -0.21 + log(w) $$

The growth rate of your wealth playing this game is negative according to Kelly. In a typical, median world, the coin will show head as many times as tails and after three turns, you lose everything you have.


```javascript
10    (invest 5    ) => loss
5     (invest 2.5  ) => loss
2.5   (invest 1.25 ) => win
3.75  (invest 1.875) => win
5.625 final wealth. (p = 0.5)
```

This median case is what the Kelly Criterion optimises for (see point two in [this Less Wrong post](https://www.lesswrong.com/posts/DfZtwtGD6ymFtXmdA/kelly-is-just-about-logarithmic-utility#2)). Even though, on average over all possible worlds, the astronomical gains from that one time the coin only ever shows head compensate for all other losses and thus we have an expected value of 1.

![Diagram of a logarithmic function and Kelly himself.](/assets/kelly-criterion-ship-investor/add55295a1fceea5153e60a05198ec32.webp)

The logarithm acts as a sort of model for losses compounding, because it tends to negative infinity very quickly for negative returns, penalizing losses and diminishes the effect large improbable wins have on the expected value.

## Applying the Kelly Criterion

To illustrate the power of the Kelly Criterion, we’ll be looking at the [Ship Investor](https://entropicthoughts.com/binary-kelly-criterion-training-ship-investor-game) game that Entropic Thoughts designed. The player is a wealthy man in the 17th century, looking to invest in different shipments, trying to maximise his wealth. Every turn, four different investments are offered, for the same ship, but each having a different size. 

Your job is to determine the best investment, given the risks associated with the route the ships take. They can travel through the Gibraltar strait (very safe at over 90% success rate), the Malacca strait (between 60 and 80% of shipments pass) and the Bering strait (very unsafe, around 50% of ships pass).

I urge you to try it out before reading any further and to see if you would have been a wealthy magnate in bygone times.

![World map showing the different straits and their safety ratings.](/assets/kelly-criterion-ship-investor/40ad7950715ebf1290ecbe8af626c777.webp)

To succeed in the harsh business climate of past times and win the game, we always need to choose an investment that maximises our long-term wealth. Oh wait, isn’t that what the Kelly criterion is for?

For situations where you either win a fraction of the investment or lose all of it (most gambling works like this), the Kelly Criterion takes a simplified form, that can be used to estimate the fraction of your wealth to invest.

$$ f^* = p - \frac{(1 - p)}{B} $$

Where $$ f^* $$ is the fraction of wealth to invest and $$ B $$ is the proportion gained with a win (e.g. for a 1:1 odds bet $$ B = 1 $$).

## Simulating different Agents

To test this formula, I transcribed the ship investor game to a python script and created multiple agents that play with a certain agenda.

Here is what 200 Kelly betters look like, each playing 500 turns.

![Graph showing the wealth over time of a large number of Kelly bettors.](/assets/kelly-criterion-ship-investor/0296c860a5a836ddfaad14523829ea5f.webp)

On average, the bettors take a large profit, increasing their wealth from 100 ducats to over 100 million in 500 steps. The median wealth is also on a steady climb. 

There are a few that drop out and lose everything, because the implementation of the game sometimes generates negative odds, which means a Kelly bettor invests everything.

Even though in the short term, due to luck other strategies might outperform the Kelly Criterion, it ends up on top in the long term.

![Different betting strategies compared to the Kelly bet.](/assets/kelly-criterion-ship-investor/493d5aa5c939fc05f1ade28281414e91.webp)

## Deriving the Gambling Formula

So how do we get from the general rule of maximising logarithmic wealth to the very specific gambling formula for sizing your bets?

First, we express your wealth at step $$ n $$. $$ W $$ and $$ L $$ are the number of wins and losses.

$$ W_n = (f B + 1)^W \cdot (1 - f)^L $$

We can also express $$ W $$ and $$ L $$ with respect to $$ p $$ and $$ n $$.

$$ p = \frac{W}{n} \\
q = \frac{L}{n} = 1 - p $$

We can then express $$ W_n $$ with respect to $$ n $$ and $$ p $$.

$$ W_n = (fB + 1)^{np} \cdot (1 - f)^{nq} $$

Now, we apply the Kelly criterion, by expressing the growth rate $$ G $$.

$$ G = \lim_{n \to +\infty} \frac{1}{n} (\log(W_n))
\\
G = \lim_{n \to +\infty} p \cdot \log(fB + 1) + q \log(1 - f) $$

We want to find the point where $$ G $$ is at it’s maximum. As $$ G $$ is concave, this is the case for $$ \frac{\text{d}}{\text{d} f}G = 0 $$. 

The graph shows the growth rate as a function of the invested fraction. The Kelly bet is the fraction that maximises growth, where the tangent meets the curve. You can try to play around with the above function on [Desmos](https://www.desmos.com/calculator/y2e7vb4lvq).

![Graphing the growth rate against the fraction of wealth invested.](/assets/kelly-criterion-ship-investor/ba39232d3caffec946955617ce15afa5.webp)

$$ \frac{pB}{(fB + 1)} = \frac{1 - p}{1 - f} \\
f(1 - p + p) = p - \frac{(1 - p)}{B} $$

Which gives us the gambling formula.

$$ f = p - \frac{1 - p}{B} $$

If you want a better, more detailed explanation of the maths, I would recommend this [great post on the topic](https://fhur.github.io/notes/articles/the-kelly-criterion/index.html).

