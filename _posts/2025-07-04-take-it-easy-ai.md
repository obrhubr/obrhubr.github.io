---
layout: page
title: "The 167 Point Ceiling of the Game Take-It-Easy"
time: 7 minutes
published: 2025-07-04
colortags: [{'id': '4260119c-7ec5-48b3-ba5b-96f4335cdc7f', 'name': 'AI', 'color': 'yellow'}, {'id': 'f50f3705-0c22-40e2-a074-91d12222a447', 'name': 'Puzzle', 'color': 'purple'}, {'id': '28d7f40f-be75-455e-9d82-781b78d1548c', 'name': 'Games', 'color': 'pink'}, {'id': '805abdfa-25d7-4253-b70a-011688c45da1', 'name': 'Statistics', 'color': 'blue'}]
tags: ['AI', 'Puzzle', 'Games', 'Statistics']
permalink: take-it-easy-ai
favicon: take-it-easy-ai/favicon.png
excerpt: "Instead of simply enjoying a cool board game, I dissect and explore the different approaches to solving the imperfect information game Take-It-Easy.
I compare basic heuristics to a more sophisticated reinforcement learning approach.
What’s the best a computer can do?"
short: False
sourcecode: "https://github.com/obrhubr/take-it-easy"
hn: 
math: True
image: assets/take-it-easy-ai/preview.png
---

[Nerd-sniping](https://xkcd.com/356/) me is pretty easy. Step 1 is to get me a board game. Step 2 is to beat me over and over (at the game, not literally please). This will give me the necessary motivation to build a program in order to take back my dignity…

## Meet Today’s Victim

*[Take It Easy](https://en.wikipedia.org/wiki/Take_It_Easy_(game))* is played on a hexagonal board with 19 tiles and a stack of 27 pieces. Each turn the player draws a random piece from their stack and places it on an open tile on the board. The goal is to score the highest number of points.

Each piece has three lines on it, one vertical, one diagonal from left to right (LR) and one from right to left (RL). There are three different “line values” per direction: the vertical line can be worth either 1, 5 or 9, the diagonal LR 3, 4 or 8 and the diagonal RL 2, 6 or 7.

![<p>Take-it-Easy board (with numbered tiles) and pieces.</p>](/assets/take-it-easy-ai/0f4cbe24484db169924f9ffdb660361b.webp)

A completed line - meaning a fully connected path going vertically or diagonally from one end of the board to the other - is worth it’s length times the value of the line. The maximum possible score is 307, which can be achieved in only 16 different ways.

![<p>Example of a board scored with 121 points.</p>](/assets/take-it-easy-ai/8c8f60bb8b01c671686baa7176b3aecf.webp)

If you want to take a shot at playing yourself, go to [take-it-easy.obrhubr.org](https://take-it-easy.obrhubr.org/). See if you can beat the AI!

## First Attempts

The game cannot be deterministically solved due to the huge state space. With 27 tiles, 19 of which are drawn each game and can be placed anywhere on the 19 tiles, there are $$ \approx 2.7 × 10^{23} $$ possible games, which is simply too much to fully explore.

$$ \binom{27}{19} \cdot 19! \approx 2.7 × 10^{23} \quad \text{possible games} $$

To establish a baseline performance, we’ll compare different basic strategies. A bot playing random moves only (plot 1) will score mostly 0. 

A greedy bot that places pieces randomly except if it can complete a line halves the number of games scoring 0 and ups the mean to 23 points (plot 2).

![<p>Comparing score distribution for: random move selection; naïve move selection and basic heuristics.</p>](/assets/take-it-easy-ai/3c7b284d848b00f3bb185031b844e2ab.webp)

To improve on that score, I wrote an evaluation function that captures the potential value of an uncompleted line. This basic heuristic scores lines that have a good chance of being finished higher than those that are already blocked, according to the number of pieces with the right line on them left.

This upgrade increases the mean score to about 142 points and completely eliminates 0 point games (plot 3), which is a massive improvement. But we can do better…

## A Neural Network Based Approach

After struggling to come up with better heuristics for a while I embraced the [Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) and looked into NN based techniques. 

After fooling around for a bit, I gave up due to my limited knowledge and searched for some prior work. I found [polarbart's awesome bot](https://github.com/polarbart/TakeItEasyAI), which I re-wrote and explored in depth as a learning experience.

Here are the final scores, which easily beat my previous bots.

![<p>Histogram showing the scores achieved by the model.</p>](/assets/take-it-easy-ai/ab818bbb2c94b770b631831db53a96c1.webp)

About a hundred hours of training and a significant jump in computational complexity gets us a median score of 168 points (28 more than the basic heuristics). The best score achieved also increases from 250 to 280.

## Inference

Instead of manually writing an evaluation function like before, the bot has a neural network score the board. This technique is a type of [Q-Learning](https://en.wikipedia.org/wiki/Q-learning): the next move is not only chosen based on immediate reward but also future rewards.

In the case of Take-It-Easy, the neural network spits out a probability distribution for the expected final score. This approach works so well because the distribution manages to capture the randomness of the game better than just the usual single score (see the [paper](https://arxiv.org/abs/1710.10044) referenced by polarbart).

![<p>State and probability distribution given by neural network for each possible next state.</p>](/assets/take-it-easy-ai/0befd680bfa2f5424a19901eb81c2b49.webp)

## Training

But the model has to learn to accurately estimate the probability distribution somehow… To make things even more difficult, Take-it-Easy gives us only limited immediate feedback (the reward for completing a line) while the final score can only be calculated at the end.

The [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation) allows us to bridge the gap between reward and final score. The evaluation function $$ \mathbb{Z} $$ is updated according to the immediate reward $$ r $$ and the probability distribution of the next state (according to optimal policy) noted $$ \mathbb{Z}(s') $$. 

$$ \mathbb{Z}(s) \sim \space r \space + \space \mathbb{Z}(s') \quad \text{(simplified)} $$

If you’re not at all used to the industry jargon, this may sound mostly like magic words (I certainly was very confused). In practice this means that during each round of training the model plays a lot of games. To update the NN, we train it on the current state as the input, with reward + probability distribution of the best next state as the output. Thus, with every move, we encode another tiny sliver of information (the reward).

The model kind of bootstraps itself, as each iteration learns from the previous one. Seeing this in action kind of felt like magic to me.

## Limits

While experimenting, I trained many model configurations, varying different parameters: hidden size, learning rate, epsilon, output size, dataset size, etc...

The results were all pretty consistent. Changes in any of the parameters didn’t affect performance and only reduced or increased the rate at which the model improved initially. But all models eventually hit the seemingly hard limit of ~167.

I wasted at least a couple hundred hours and a pretty sum renting GPUs for training, all in a futile attempt to increase the score (If you want to take a shot at training your own model, I provided a [Colab notebook](https://github.com/obrhubr/take-it-easy/tree/master?tab=readme-ov-file#on-google-colab)).

![<p>Comparison of the scores achieved during training and validation of different model configurations.</p>](/assets/take-it-easy-ai/9f4189729ae8c8c26ce255859d876a61.webp)

This hard limit on the score could either be the result of a pretty huge local minima that halts progress, or it could be evidence of the natural entropy of the game itself.

Similar to how an LLM can never be sure if the next word in the sentence “The house stood upon a“ is (it might be hill, mountain etc…) due to the [natural entropy of language](https://arxiv.org/pdf/2010.14701), there might not be a single optimal move in Take-it-Easy.

This intuitively makes sense: the random order of the pieces drawn means that there is never a “best” move. The game could just be too random for a player to achieve more than 167 points on average, even with the best possible strategy?

## Interpreting the Trained Model’s Parameters

I wanted to find out more about the strategies employed by the different models, in order to find out if they converged - and got stuck on - a consistent strategy. To visualise what effect on the score placing a piece on a tile would have, I mapped each input neuron’s weights to their corresponding tile and line on the board.

The mapping from board to neural network input is based on one-hot encoding. For each tile, we encode 9 bits of information about the piece on it: three lines per tile and three possible line values for each of them.

![<p>Visualising the one hot encoding of the tile &lt;9, 4, 6&gt;.</p>](/assets/take-it-easy-ai/ef9ecf1d95b309785222ee7a5ef49bb2.webp)

A red line means that placing a piece with that line on this tile influences the model’s first layer positively, while a blue line means the next layer is negatively influenced.

![<p>Graphic showing neuron weights mapped to their tile and corresponding line.</p>](/assets/take-it-easy-ai/9d71e4d30f19a7482362cc25303ead40.webp)

What is interesting is that the mapping of weights to lines is not at all universal. Every model shows a different pattern when visualised this way. This might be due to this not being a very reliable test, or…

The actual predicted score of the same board stays consistent (a few points maximum), no matter the model configuration. Therefore, this might be another clue that there isn’t a single best strategy and that Take-It-Easy is too random to score more than ~167 points on average.

## Open Questions

Going through polarbart’s code in detail, slowly reconstructing his model architecture and fiddling with different optimisations (or un-optimisations because of a lack of understanding…), helped me gain a lot of insights into this type of reinforcement learning. But there are a few things I don’t understand and maybe by sharing I’ll get an answer.

For those not familiar with loss metrics, usually loss starts out high, as the model quickly adapts to the training data, and then slowly reaches a minimum, not improving any further. Here, because of the constantly changing policy, like a moving target, the loss increases.

The loss staying high after its initial climb seems to further indicate that the game is truly capped at about 167 points due to randomness.

![<p>Loss over time during training of the different models.</p>](/assets/take-it-easy-ai/2c5f0c7081a792fb3d2ec3bf76f7f53a.webp)

What stood out to me is the small bump happening consistently across model configurations around iteration 20. It might be a critical turning point in model policy, or something else entirely? I would be very interested in an explanation (see my email below)!

