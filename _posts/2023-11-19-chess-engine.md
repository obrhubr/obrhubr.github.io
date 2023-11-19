---
layout: page
title: How to build a chess engine and fail

time: 9 minute
published: 2023-11-17

tags: CS C# Engines
excerpt: A Chess-AI is something every programmer should build at least once and [Sebastian Lague’s](https://www.youtube.com/@SebastianLague) [competition](https://www.youtube.com/watch?v=iScy18pVR58) was the perfect opportunity for me to do so. Constrained to 1024 tokens I wanted to implement an evaluation function similar to that of Stockfish’s NNUE but heavily simplified. And instead of using a complex feed-forward algorithm to train the neural network I wanted to optimise the parameters using a genetic algorithm that relied on historical Stockfish data. However, I quickly realised why the model Stockfish uses has 50MBs of data and would not fit into my small bot for the competition…
---

# How to try to build a chess engine and fail

(View the sourcecode and a more detailed writeup about the project at [https://github.com/obrhubr/chess-challenge-participation/](https://github.com/obrhubr/chess-challenge-participation/))

## What is the current state of chess engines?

A Chess-AI is something of a rite of passage for every software engineer, as is a snake clone or a calculator console application. If you did not try to build one yet, you are certainly missing out (or preserving your own sanity, whatever you prefer). Between the [chessprogrammingwiki.org](https://www.chessprogramming.org/Main_Page) and other online ressources this is now a pretty well explored field, but that is not to say that innovation is impossible and nothing changed since the days of Deep Blue (the first ever chess computer the officially beat a grandmaster). 

In recent years Stockfish, the most advanced computer chess engine, has gotten a major upgrade in the form of a NNUE, a fast neural network of sorts which is used as it’s evaluation function. An evaluation function does exactly what it sounds like, it is used by the engine to evaluate the current position.

Today I would group chess engines into two categories: “explore the most possibilities as fast as possible” (Stockfish) and “have a very sophisticated evaluation function in the form of a neural network” (Leela Chess Zero).

## What is left for amateurs, such as myself then?

Sebastian Lague has the perfect answer to that question: a [competition](https://www.youtube.com/watch?v=iScy18pVR58) that imposes an arbitrary limit on the length of your engines code. To be exact every participant has a maximum of 1024 tokens at his disposal to craft the best chess bot they can. Sounds like a lot, or extremely little depending on your conception of tokens. In this case a token is the smallest unit the compiler can see, with some exceptions. Therefore your 28 character Java like variable `ChessEngineBotThinkingBoardGamePiecePlayerMoverFactory` will only count as a single token, while `{` also counts as one. You also cannot load external files or use certain functions to extract variable names, which is enforced by limiting the allowed namespaces.

## Trying to improve the evaluation function

This limitation prevents the implementation of any neural networks or complex evaluation functions necessary for chess engines of the second type described above. This naturally would lead participants to choose to implement an efficient algorithm to search as much of the game tree as possible.

Despite this, I wanted to do something akin to knowledge distillation, inspired by the NNUE of Stockfish, that uses the current board as an input and by applying the weights and biases of the model it comes up with a number.

If, instead of using a complex network, we used a single 8x8 grid of weights for each type of piece, we could distill the game knowledge of powerful engines into a very small number of bytes. This evaluation function could then still be “plug and play” with a traditional Minimax engine and give our engine a crucial competitive advantage, while still staying inside the allowed 1024 tokens.

**(To anyone familiar with chess engine programming, this is essentially a ****[PST](https://www.chessprogramming.org/Piece-Square_Tables)****, a piece square table. What's new here is the way it's values will be fine-tuned.)**

## The Idea

A very basic approach to an evaluation function is to add up the values of each piece a player has on the board and get the difference between these values for both players, which gives a score. Instead of assigning a static value to each type of piece (8 for a queen, 3 for a knight etc…) we weight their value based on their position on the field. One basic improvement we could make is to increase the value of a pawn the further it progresses up the board.

![Untitled](/assets/chess-engine/2c42617a_Untitled.png)

Instead, copying the idea of the NNUE, we “train” our model on a lot of games and could come up with very sophisticated weighting strategies. We assign a value to every square of the board a piece could stand on, and do that for every type of piece. To evaluate a position, we would only need to add the value of the squares every piece stands on.

For the implementation, we would need to save the weights of each square of each piece to an array. To evaluate we take a bitboard (`1` means a piece is present on the square, `0` indicates that no piece is there) representing the different pieces on the board as an array, and multiply it and the model’s weights together. The result would be a board with only the values of the squares left, that have a piece currently standing on them. Summing the values of the 6 different boards (6 piece types: pawn, knight, bishop, rook, queen, king) together for each player and subtracting them gives us a value in the format of the classic stockfish evaluation: `-1.5` for example to represent black winning by a certain margin, `+7.9` to represent white having a very powerful advantage.

![Untitled](/assets/chess-engine/c2d560c4_Untitled.png)

## Implementing the genetic algorithm and training

The question that remains is that of setting the value for each of the squares of the boards. Here, a tried and tested technique of machine learning seemed perfect: genetic algorithms. The issue with traditional techniques of training machine learning models in this context is that there are no nodes and edges to tune the values of using back and forward propagation.

Genetic algorithms on the contrary don’t use these more sophisticated techniques, and just mutate the values of the boards randomly between generations, always selecting the best of the current generation. Our training would therefore look something like this: we instantiate the model with randomly selected numbers between some boundary. We then evaluate these “weights” to assign a fitness to each and at the end we select the very best. We then slightly but still randomly mutate the values to create 500 or more children and test their fitness again. 

![Untitled](/assets/chess-engine/cd258d6b_Untitled.png)

We repeat this for a few hundred generations and we would be left with a single model that has been optimized for the fitness function. 

Now we have the issue of defining an appropriate fitness function, to make sure we really chose the models that have the best chance of producing accurate evaluations. To do this I downloaded a large number of lichess and chess engine games from the internet in PGN format. PGN stands for “portable game notation” and it encodes chess games into a series of moves with a bit of metadata.


```javascript
[Event "F/S Return Match"]
...
[White "Fischer, Robert J."]
[Black "Spassky, Boris V."]
[Result "1/2-1/2"]

1. e4 { [%eval 0.17] [%clk 0:00:30] } 1... c5 { [%eval 0.19] [%clk 0:00:30] } 
2. Nf3 { [%eval 0.25] [%clk 0:00:29] } 2... Nc6 { [%eval 0.33] [%clk 0:00:30] } 
[...]
13. b3 $4 { [%eval -4.14] [%clk 0:00:02] } 13... Nf4 $2 { [%eval -2.73] [%clk 0:00:21] } 0-1
```

I then extracted the evaluation for each position and stored these for training, resulting in a few hundreds of thousands of lines of chess positions. 

This seemingly random string is actually a [FEN](https://de.wikipedia.org/wiki/Forsyth-Edwards-Notation) string, which stores the position of each chess pieces, therefore encoding the board. Paired with the evaluation that a powerful chess engine assigned to it, this was the perfect dataset to train my own engine.


```json
{
    "positions": [
        {
            "fen": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            "eval": 0.19
        }
	]
}
```

The fitness function would consist of evaluating a position with the values of the boards that the model has and taking the difference of that and the actual evaluation of the position. To get the best child in a generation we would then take the one with the lowest overall score, which means it has evaluated the positions closest to the actual evaluation.

## Disappointing results

My enthusiasm for this idea quickly ebbed away very quickly once I realised how long training would take and also how bad the first dozen generations really were. Plugging in the values of the best models produced mediocre results, even against very weak opponents.

What was wrong? Distilling the knowledge stored in the [NNUE](https://tests.stockfishchess.org/nns), which is pretty small but still about 50MBs large, into only 24576 values was too much. The loss of context that my implementation had by design was crippling it’s ability. The different boards for each piece that make up the model do not consider their position relative to other pieces. Moving the queen to c6 would be evaluated as equally good, whether it blundered the queen to a pawn or delivered a beautiful checkmate.

But adding the additional context that stockfish provides it’s NNUE was simply not possible for the amount of tokens that the challenge bestowed upon us.

## How does the NNUE solve this problem?

![Untitled](/assets/chess-engine/f15a6ae6_Untitled.png)

Stockfish’s NNUE is essentially made up of a heavily overparametrised input layer and a simple 4 layer network behind it. What this means is that instead of using bitboards representing the positions of the different pieces as inputs and applying the weights and biases, it instead gives the NNUE the positions of every single piece in relation to every single king position. This provides the network the necessary context to evaluate the position, which our simplified version lacked. (1)

Concretely this translates to a model architecture consisting of 2x45056 inputs. It has two sides, one for the side that currently moves and the opposing side. Where does 45056 come from? For each of the two input halves, there are 11 other piece types to consider in relation to the king of the current side and there are then 64 squares a piece could be on for 64 squares the king could be on.

For example, if white is to move, there are 11 other piece types (W Queen, W Rook, W Bishop, W Knight, W Pawn, B King, B Queen, B Rook, B Bishop, B Knight, B Pawn) that have to be taken into account. For each of the pieces on the board, we would then get the pair of `(king position, piece positions)`, and activate the corresponding input node of the network.

![Untitled-2023-11-03-1915](/assets/chess-engine/3d0a095a_Untitled-2023-11-03-1915.png)

This graphic from the [chessprogrammingwiki.org](https://www.chessprogramming.org/Main_Page) nicely summarises the reset of the model architecture.

![HalfKAv2](/assets/chess-engine/82e86e6a_HalfKAv2.png)

This architecture also allows the highly optimised evaluation of the network that makes stockfish so fast. As long as the king does not move, you only have to update a single input node to recompute the evaluation for each move.

## How could the shortcomings be remediated?

While the ultra-high rate of compression from 2x45065 inputs to only 6x8x8 is clearly too high, a more conservative approach might be able to identify unused or less impactful inputs or nodes in the stockfish NNUE to apply a “pruning” of sorts. Some positions such as (…, pa1) and others where the pawns would have to walk backwards are not even possible and **I assume naively** could easily be removed from the network.

<br/>

**Bibliography:**

- (1) [https://github.com/official-stockfish/nnue-pytorch/blob/master/docs/nnue.md#what-is-nnue](https://github.com/official-stockfish/nnue-pytorch/blob/master/docs/nnue.md#what-is-nnue)

- [https://www.chessprogramming.org/Stockfish_NNUE](https://www.chessprogramming.org/Stockfish_NNUE)

- [https://stockfishchess.org/blog/2020/introducing-nnue-evaluation/](https://stockfishchess.org/blog/2020/introducing-nnue-evaluation/)

