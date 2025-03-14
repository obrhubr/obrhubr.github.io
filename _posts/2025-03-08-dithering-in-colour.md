---
layout: page
title: "Dithering in Colour"
time: 5 minutes
published: 2025-03-08
colortags: [{'id': '65ba48da-4c0d-4f9f-b81b-030901b44c27', 'name': 'Computer Graphics', 'color': 'purple'}]
tags: ['Computer Graphics']
permalink: dithering-in-colour
favicon: dithering-in-colour/favicon.png
excerpt: "Inspired by multiple posts on dithering, I set out to create a correct implementation of Atkinson dithering with support for RGB colour palettes. The post also outlines implementing linearising the colour-space and correcting for human perception."
short: False
sourcecode: "https://github.com/obrhubr/ditherpy"
math: False
image: assets/dithering-in-colour/preview.png
---

After reading a post on the HN frontpage from [amanvir.com](https://amanvir.com/blog/writing-my-own-dithering-algorithm-in-racket) about dithering, I decided to join in on the fun. Here’s my attempt at implementing Atkinson dithering with support for colour palettes and correct linearisation.

## Dithering into arbitrary palettes

The linked post from [Aman](https://amanvir.com/) does an excellent job of explaining dithering into a black and white palette using [Atkinson Dithering](https://en.wikipedia.org/wiki/Atkinson_dithering). I can also recommend [surma.dev](https://surma.dev/things/ditherpunk/)’s post, he explains more than just error diffusion (for example [ordered dithering](https://en.wikipedia.org/wiki/Ordered_dithering)).

However both of them convert their input images to grayscale before dithering. If the sum of the pixel and the accumulated error is lighter than the threshold, they pin it to pure white, otherwise to pure black: `colour = 255 if colour >= 127 else 0`.

But why restrict ourselves to monochromatic palettes? Instead of converting the image to grayscale before dithering, we could use any palette!

![Albrecht Dürer painting dithered in RGB, CMYK and a Gameboy-like palette.](/assets/dithering-in-colour/ac75c25ee4e9c198f8bc50fd41863557.png)

To dither into “black and white”, we simply compared the scalar value of the pixel to a threshold. If we want to work with colours, we will have to account for all channels (red, green and blue values of the pixel). Instead of a simple comparison between two scalars, we have to find the closest colour 3d (colour) space. 

For each distinct colour in the palette, the distance to the pixel’s colour is computed using euclidean distance. We also accumulate the error for each colour channel individually, similar to what is done in monochrome error diffusion dithering.

![Distance in 3d colour space.](/assets/dithering-in-colour/c57d6c5d831cb40c5012fe0eaa8b254b.webp)

If you want to play with dithering and different palettes yourself, check out [ditherit.com](http://ditherit.com/), which has a pretty nice web interface.

## Linearising

We have just committed a mortal sin of image processing. I didn’t notice it, you might not have noticed either, but colour space enthusiasts will be knocking on your door shortly. 

First, we failed to linearise the sRGB input image, which results in overly bright dithered outputs. And second, we didn’t take into account human perception, as green is perceived brighter than red for example.

Images are usually stored in the sRGB colour space, which is gamma encoded. An issue arises when we want to quantitatively compare brightness in sRGB. Because it’s not a linear colour space, the difference in brightness going from `10` to `20` is not the same as from `100` to `110`, for example.

![Dithering a black-to-white gradient will be wrong without linearising first.](/assets/dithering-in-colour/de84179f42083d526fa2dda86f65c664.png)

This means that dithering in sRGB directly will produce results that are too bright. Before dithering, we need to linearise the image - convert to a linear colour-space.

[Surma explains linearisation pretty well](https://surma.dev/things/ditherpunk/) and you should also check out [this stackoverflow answer](https://stackoverflow.com/questions/596216/formula-to-determine-perceived-brightness-of-rgb-color/56678483#56678483), which is very thorough. [This post from John Novak](https://blog.johnnovak.net/2016/09/21/what-every-coder-should-know-about-gamma/) is the best explanation of gamma you can find and I recommend reading it.

If we also want to take human perception into account, we need to assign different weights to each channel. By scaling the colours before comparing, we preserve [perceptual luminance](https://en.wikipedia.org/wiki/Grayscale#Colorimetric_(perceptual_luminance-preserving)_conversion_to_grayscale). The linked Wikipedia post lists the following values: `0.2126 R + 0.7152 G + 0.0722 B`.

The two following comparisons should illustrate the kind of errors not linearising produces. If the linearised version looks wrong to you, try opening it on a larger monitor in it’s original size and check your gamma settings.

![Comparison of Dürer’s Young Hare in the original, linearised and dithered and dithered but not linearised versions.](/assets/dithering-in-colour/640cc78e6577a09ea1b8939babf11f85.png)

![Comparison of an RGB gradient, the linearised and dithered gradient and the dithered gradient, without linearisation.](/assets/dithering-in-colour/c4bea55843250ca603319425db14466f.png)

If you want to play with a correct implementation, there is the [dither](https://github.com/makew0rld/dither) library and the corresponding command line utility [didder](https://github.com/makew0rld/didder) from [makew0rld](https://github.com/makew0rld). Check out the [authors explanation about linearisation on his blog](https://www.makeworld.space/2021/02/dithering.html).

If you want to play with my python implementation, [check it out on GitHub](https://github.com/obrhubr/ditherpy).

## Pitfalls to avoid

Correct luminance when dithering is very important if you want to preserve the image’s original appearance. If you just care about the aesthetic of dithering, feel free to skip it of course. There are a few pitfalls I have discovered while writing this post, and others were helpfully pointed out by various [HN commenters](https://news.ycombinator.com/item?id=43315029). Thank you!

Downsizing or modifying the scale of the image is likely to mess with the dithering, especially scaling down while using anything but linear interpolation. Another factor that might make the results look off is incorrect gamma settings on the monitor used to view the image. Phones are often the worst offenders here, as they combine wrong gamma with small screens and bad downscaling.

Error diffusion and linear colour spaces are tricky. Using an Atkinson dither results in an image that is too dark, as only `6/8th` of the error are diffused:

![Comparison of Atkinson’s and Floyd-Steinberg’s diffusion matrix.](/assets/dithering-in-colour/3ac81d80f16b88d8a912b8b8e03f42f3.webp)

This results in images that appear darker. Floyd-Steinberg on the other hand, fully diffuses the error and doesn’t behave badly. I am not sure if Atkinson considered linearisation while working on his algorithm at Apple, but that’s speculation on my side. Hopefully someone can point me in the right direction here!

Here’s the black and white gradient from before, but comparing Atkinson and Floyd-Steinberg, both in a linearised colour space:

![Comparison of Atkinson and Floyd-Steinberg dithering with a black and white gradient.](/assets/dithering-in-colour/b421b2e982b5efd0d86c4d24fd11bce6.png)

You can clearly see how the missing `2/8th` make darker greys disappear.

TL;DR; Linearise the image’s colour space before dithering, consider perceptual luminance while selecting the closest colour from your palette and apply gamma-correction before exporting the results.

<br/>

*This has become more of a link collection than a post. But I hope that someone finds it helpful to have all resources and a basic explanation in one place… If you know more than me about colours and noticed any errors, please reach out!*

<br/>

