---
layout: page
title: "Prisoner’s Chessboard Puzzle"
time: 15 minutes
published: 2026-08-22
colortags: [{'id': '168fc2da-f463-41d6-b9a6-d26635055091', 'name': 'Math', 'color': 'brown'}, {'id': 'f50f3705-0c22-40e2-a074-91d12222a447', 'name': 'Puzzle', 'color': 'purple'}]
tags: ['Math', 'Puzzle']
permalink: chessboard-puzzle
favicon: chessboard-puzzle/favicon.png
excerpt: "This is my attempt at explaining a solution to the prisoner’s chessboard puzzle. The puzzle itself is straightforward: encode a position on an 8x8 chessboard using the 64 squares - the catch is, you can only flip a single coin on the given board to do so."
short: False
sourcecode: 
hn: 
math: True
---

A friend recently sent me [this video](https://www.3blue1brown.com/lessons/chessboard-puzzle/) by [3b1b](https://www.youtube.com/@3blue1brown) and challenged me to find a solution for the puzzle. I highly recommend taking a few minutes to watch the introduction and to think about it yourself.

My goal with this post is to put my thought-process to paper as an exercise in clear writing. And just maybe this perspective helps a reader learn something…

The final solution itself is identical to the one presented in the [follow-up vide](https://www.youtube.com/watch?v=as7Gkm7Y7h4)o by [Stand-up Maths](https://www.youtube.com/@standupmaths).

## The Setup

The puzzle goes as follows: You and your fellow inmate are offered a deal by the warden. You are separated into two cells. First, he presents you a chessboard. On each square he places a coin, flipped to either heads or tails. Then, he hides a key under one of the squares, showing you exactly where it is.

Your task is to choose a single coin to flip. The board is then handed to the other prisoner, who has to deduce the square under which the key is hidden only from the current state of the board.

You are allowed to agree on a protocol with the other prisoner beforehand, however once the board is brought in, no more communication is allowed at all.

You can assume the coins the warden places on the chessboard are randomly flipped (or even adversarially).

At first this sounds impossible, but there’s a very elegant solution that is able to handle all possible board configurations.

## The Solution

First off, to formalise this we want to look at the 64 coins on the board as a 64 bit array.

Our goal is to encode which square the key is hidden under, so our fellow inmate can guess correctly. We need 6 bits (as $$ 2^6 = 64 $$) to do so.

Our protocol will specify a way to read the board $$ b $$ and to decode a position from it $$ \text{dec}(b) $$.

The issue we are facing is that no matter which random configuration the board is in and which key position it currently encodes to, we need to be able to change it to any possible other position.

### The Toy Example

Let’s first think about a simplified case, with a board that has 4 squares. We only need 2 bits to encode the key position $$ k $$ (four possible squares), so we have 2 left for our encoding scheme.

If the warden hides the key under the first square, we want to encode $$ 00 $$, if it’s the last square, we want to encode $$ 11 $$ and so on and so forth.

Our first strategy might be “we just encode the position in the first two bits”. Assume the warden hides the key under the last square. He then randomly flips the coins and we get the following board: $$ 0000 $$.

![<p>The board 0000 as we get it from the warden.</p>](/assets/chessboard-puzzle/01fc70bcf0520b73daa26afe87772e9e.svg)

What do we do now? There’s no way to get to $$ 11XX $$ (where $$ X $$ is a don’t care) with only a single flip. So we are stuck.

We somehow need to design an encoding scheme that assigns board states to positions in a way that allows us to go from any of the 4 possible states to any other (in 3B1Bs video this is the colouring analogy).

![<p>A possible mapping of all 16 states to a key position (that doesn’t work, no way to get from blue 1000 to green in a single flip).</p>](/assets/chessboard-puzzle/7a8d3ee16e5fe24d045ac8e05bf9618b.svg)

Let’s reframe our goal in the following way: given the current board and the position $$ \text{dec}(b) $$ it decodes to, we need to get to $$ \text{dec}(b) = k $$ using a single flip.

In the previous example with $$ 0000 $$, we had $$ \text{dec}(0000) = 00 $$ and the key was $$ k = 11 $$. So we’d need to have a coin (or position on the board) that is equivalent to flipping both coins *at once*.

This needs to work for any bitwise difference between the decoded value and the key position. Another example: $$ \text{dec}(1100) = 11 $$ and $$ k = 01 $$, i.e. difference $$ 10 $$. Then by flipping the first position to get $$ b = 0100 $$ we can encode the correct key position.

In other words, we need to assign each possible bitwise difference a position that “controls” it. One such labelling for our simple 2x2 case could be: the first two bits control bit $$ \{0\} $$ and bit $$ \{1\} $$ respectively. Our 3rd bit controls the third possible subset $$ \{0,1\} $$.

![<p>We can encode any number of flips thanks to the carefully overlapped bits.</p>](/assets/chessboard-puzzle/9be3df5e138a52364c9a1632ca8c3e60.svg)

> Notice that the number of non-empty subsets of any sequence of $$ n $$ bits is $$ 2^n - 1 $$. So for two bits, we get $$ 2^2 - 1 = 3 $$ bits required.

Back to our example: we need to encode $$ 11 $$ from the state $$ 0000 $$. So we flip the 3rd bit, which we decided controls flipping both bits at once. So the board we hand to the other prisoner is $$ 0010 $$.

![<p>Flipping a single bit changes the encoded position from 00 to 11.</p>](/assets/chessboard-puzzle/70d9abbdd98a0e4311d5f7df64fe3977.svg)

He knows that 3rd bit flips the first two bits of the final position encoding and correctly guesses $$ 11 $$.

You can try to convince yourself that this is correct. We can get from any random starting point to the correct encoded position in one single flip (I’ll also provide a simple proof for the general case at the end).

There’s one edgecase though: what if the position is already correctly encoded? In that case, flip the last bit, as a sort of no-op. We don’t consider it during decoding anyways.

<div class="html_inline">
<style>
    .inline-container {
        width: 100%;
        margin: 0 auto;
    }

    .inline-grid {
        width: min(100%, 200px);
        aspect-ratio: 1;
        margin: 0 auto;

        display: grid;
        grid-template-columns: repeat(2, 1fr);
    }

    .inline-grid > div:nth-child(1),
    .inline-grid > div:nth-child(4) {
        background: #f0d9b5;
        --fg: #3a2f1c;
        --fg-muted: #7a6a4f;
    }

    .inline-grid > div:nth-child(2),
    .inline-grid > div:nth-child(3) {
        background: #b58863;
        --fg: #2a1d0e;
        --fg-muted: #e8d9c4;
    }

    .inline-grid-square {
        container: gridsquare / inline-size;
        position: relative;
        cursor: pointer;
        user-select: none;
        -webkit-user-select: none;
        -webkit-tap-highlight-color: transparent;
    }

    .inline-grid-square:focus-visible {
        outline: 2px solid #378add;
        outline-offset: -2px;
    }

    .inline-grid-coin {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);

        font-size: 42cqi;
        font-weight: 500;
        font-variant-numeric: tabular-nums;
        line-height: 1;
        color: var(--fg);
    }

    .inline-grid-bits {
        position: absolute;
        bottom: 4cqi;
        left: 6cqi;

        font-family: ui-monospace, monospace;
        font-size: 13cqi;
        line-height: 1;
        color: var(--fg-muted);
    }

    .inline-grid-key-container {
        position: absolute;
        bottom: 4cqi;
        right: 5cqi;

        font-size: 15cqi;
        line-height: 1;
    }

    .bottom-line {
        width: 100%;
        margin-top: 12px;

        font-size: 13px;
        line-height: 1.7;
        color: inherit;
        opacity: 0.75;
        text-align: center;
    }

    .bottom-line span {
        font-family: ui-monospace, monospace;
        font-variant-numeric: tabular-nums;
        color: #2c2c2a;
        font-weight: 500;
        opacity: 1;
        white-space: nowrap;
    }

    #inline-key-position {
        padding: 1px 5px;
        border-radius: 4px;

        background: #faeeda;
        color: #854f0b;
    }
    
    #inline-xor {
        color: inherit;
    }
</style>

<div class="inline-container">
    <div class="inline-grid">
        <div id="inline-grid-1" class="inline-grid-square" role="button" tabindex="0" aria-pressed="false">
            <div class="inline-grid-coin" id="inline-coin-1" data-value="0">0</div>
            <div class="inline-grid-bits">00</div>
            <div class="inline-grid-key-container" id="inline-key-1"></div>
        </div>
        <div id="inline-grid-2" class="inline-grid-square" role="button" tabindex="0" aria-pressed="false">
            <div class="inline-grid-coin" id="inline-coin-2" data-value="0">0</div>
            <div class="inline-grid-bits">01</div>
            <div class="inline-grid-key-container" id="inline-key-2"></div>
        </div>
        <div id="inline-grid-3" class="inline-grid-square" role="button" tabindex="0" aria-pressed="false">
            <div class="inline-grid-coin" id="inline-coin-3" data-value="0">0</div>
            <div class="inline-grid-bits">10</div>
            <div class="inline-grid-key-container" id="inline-key-3"></div>
        </div>
        <div id="inline-grid-4" class="inline-grid-square" role="button" tabindex="0" aria-pressed="false">
            <div class="inline-grid-coin" id="inline-coin-4" data-value="0">0</div>
            <div class="inline-grid-bits">11</div>
            <div class="inline-grid-key-container" id="inline-key-4"></div>
        </div>
    </div>
    <div id="inline-calculation" class="bottom-line" aria-live="polite" aria-atomic="true">
        The board currently encodes position <span id="inline-key-position">00</span>:
        <span id="inline-xor">no coins, so 00</span>
    </div>
</div>

<script>
(function () {
    const board = document.querySelector('.inline-grid');
    const encodedPosition = document.getElementById('inline-key-position');
    const calc = document.getElementById('inline-xor');

    const squares = Array.from(board.querySelectorAll('.inline-grid-square'));
    const coins = squares.map(sq => sq.querySelector('.inline-grid-coin'));
    const keys = squares.map(sq => sq.querySelector('.inline-grid-key-container'));

    const currentBits = squares.map(() => 0);
    const width = Math.ceil(Math.log2(squares.length));

    const bin = n => n.toString(2).padStart(width, '0');

    function render() {
        const live = currentBits
            .map((bit, i) => (bit ? i : -1))
            .filter(i => i >= 0);

        const position = live.reduce((acc, i) => acc ^ i, 0);

        keys.forEach((k, i) => { k.textContent = i === position ? '\u{1F5DD}\u{FE0F}' : ''; });

        encodedPosition.textContent = bin(position);

        calc.textContent = live.length
            ? live.map(bin).join(' \u2295 ') + ' = ' + bin(position)
            : 'no coins, so ' + bin(0);
    }

    function toggle(index) {
        const next = currentBits[index] ^ 1;

        currentBits[index] = next;
        coins[index].textContent = next;
        coins[index].dataset.value = next;
        squares[index].setAttribute('aria-pressed', next === 1);

        render();
    }

    board.addEventListener('click', (e) => {
        const square = e.target.closest('.inline-grid-square');
        if (!square) return;

        const index = squares.indexOf(square);
        if (index === -1) return;

        toggle(index);
    });

    render();
})();
</script>
</div>

### Generalising

We can now try to generalise this to the entire chessboard. We have 6 bits to encode, so we need $$ 2^6 - 1 = 63 $$ “switches” or positions to represent all possible differences (plus 1 for the no-op, which is the neutral element, as we’ll see). The $$ 2^n - 1 $$ comes from the fact we are counting non-empty subsets of the set of positions that can be flipped $$ \{0, 1, 2, 3, 4, 5\} $$.

Another way to see that we need 64 squares is that the binary numbers 0-63 effectively go through all possible 6 bit combinations in order!

To solve the puzzle, we agree on a mapping from position to flipped bits beforehand with our fellow inmate. Then, we identify the bit difference and flip the right coin to encode the key’s position. Done.

This also points us in the direction of an easier position $$ \leftrightarrow $$ bits mapping. Instead of having to agree on which position flips what subset, we just make use of the convenience of binary. As we’ve seen before, the binary numbers from 0-63 go through all possible bit combinations. We can use the square’s number in binary as the label.

Position 11 for example (which is $$ 001011 $$ in binary) flips bits 0, 1 and 3. Position 0 is our neutral element, it flips the empty set of bits. 

The implementation of decode is then reduced to XORing the numbers of positions set to `1` with each other (read this [great article on XOR](https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/xor/) for a refresher). So for the board $$ 0101 $$, which decodes to position 3, we’d get $$ \text{dec}(0101) = 1_{10} \oplus 3_{10} = 01_{2} \oplus 11_{2} = 10_{2} = 2_{10} $$. But this is still equivalent to our original idea: we just flip the bits associated with each position for which the coin shows $$ 1 $$.

Encoding also becomes trivial. Find what is currently encoded, XOR with the key position and flip the bit with the number that comes out.

Some of you might have already recognised that this is suspiciously similar to [hamming codes](https://en.wikipedia.org/wiki/Hamming_code). The similarities are there: hamming codes allow correcting up to one bitflip of corruption, while we want to be able to return to the right “codeword” (encoded position) with one flip.

Where a hamming code with 63 bits (a $$ (63, 57) $$ code) has 6 parity bits, we have 6 data bits and 57 “parity bits”.

### Proof

It’s quite easy to prove that this solution works in all cases constructively.

Take $$ \Delta = \text{dec}(b) \oplus k $$ the difference between the binary encodings (6 bit length) of both. That difference is a 6 bit binary number itself, encoding in which positions they differ.

But by construction, our board has a single position $$ i $$ which represents flipping exactly those $$ \Delta $$ bits. Thus we found a contradiction.

In the XOR construction, that bit $$ i = \Delta $$, as each positions flips it’s “own bits”.

To make it a bit more explicit: no matter if position $$ i $$ is already flipped or not, by flipping it again, we’ll invert exactly the bits it covers.

## Hamming Codes and Linear Algebra

We can call bit 0 the neutral element because we do in fact have a group here, $$ \mathbb{Z}_2^6 $$. XOR corresponds to addition. We can also look at this as a vector space in 6 dimensions.

I’m definitely not qualified to give an introduction to Hamming Code Linear Algebra though, so I’ll [point you to 3B1B](https://www.youtube.com/watch?v=X8jsijhllIA&t=171s) again.

## Some Extra Material

I found [this proof](https://sigh.github.io/puzzles/prisoners-chessboard) of the XOR solution quite nice.

A puzzle similar in spirit is described and solved over on [thenumb.at](http://thenumb.at/)’s blog in the post [Hamming Hats](https://thenumb.at/Hamming-Hats/).

