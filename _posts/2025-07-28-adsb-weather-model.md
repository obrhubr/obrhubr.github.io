---
layout: page
title: "Weather Model based on ADS-B"
time: 5 minutes
published: 2025-07-28
colortags: [{'id': '3ae6c24b-2f55-4b55-b301-e6a188641b06', 'name': 'Hardware', 'color': 'brown'}, {'id': '4d828319-e872-4062-beb9-f33802df07e8', 'name': 'Programming', 'color': 'gray'}, {'id': '0cfab4e1-efd5-4a79-8c8b-4bcf4f343208', 'name': 'Airplanes', 'color': 'purple'}]
tags: ['Hardware', 'Programming', 'Airplanes']
permalink: adsb-weather-model
favicon: adsb-weather-model/favicon.png
excerpt: "Each second thousands of planes send messages about their location and flight data - in ADS-B messages. These are intended to prevent mid-air collisions, but we can exploit the aggregated data to map out atmospheric conditions. By deriving the wind speed from the broadcast flight data, we can model wind speed and direction."
short: False
sourcecode: 
hn: "https://news.ycombinator.com/item?id=44734515"
math: False
image: assets/adsb-weather-model/preview.png
---

I recently bought an [RTL-SDR](https://kagi.com/search?q=rtl%20sdr) dongle and an antenna to receive [ADS-B](https://en.wikipedia.org/wiki/Automatic_Dependent_Surveillance%E2%80%93Broadcast) messages. These are short packets of data, broadcast by every plane in the sky, to inform others of their position, heading, speed and other flight data. The transmission of these messages is mandatory for aircraft, as it prevents mid-air accidents.

![RTL-SDR dongle and antenna for receiving ADS-B messages.](/assets/adsb-weather-model/e6b2f00e433f8f4645ff81252684f7c7.webp)

They are also unencrypted, which means anyone can listen to them. All you need is an antenna and a dongle to ingest the data on your PC (pictured above), which can be bought for less than 100$. The incoming data can then be processed by software like [readsb](https://github.com/wiedehopf/readsb) which decodes the messages.

You can choose to broadcast your own data to central servers like the [ADS-B Exchange](https://globe.adsbexchange.com/), like many hobbyists do. Thanks to them, we can visualise just about every aircraft currently in the sky. They also provide access to historic data.

![Screenshot from the ADS-B Exchange showing airborne planes on the US east coast.](/assets/adsb-weather-model/e022c10e7061ed48c64ffe8ce56ee1e8.webp)

One way these massive amounts of data can be used is to make cool visualisation, like [Clickhouse did](https://github.com/ClickHouse/adsb.exposed). We’re going to do something a bit different.

## How does ADS-B Work

ADS-B messages are (usually) [transmitted by a mode S transponder](https://aviation.stackexchange.com/questions/89700/whats-the-relation-between-ads-b-and-mode-s) on the frequency 1090 MHz. Pulse position modulation is used to encode these messages as they transmit digital data (If you want to read about analog signal transmission, you can read my recent post on [FM radio](https://obrhubr.org/fm-radio)).

The excellent book [“The 1090 Megahertz Riddle”](https://mode-s.org/1090mhz/) by [Junzi Sun](https://junzis.com/) goes into a lot of detail about ADS-B and how it works.

## Collecting Data

By aggregating and processing the messages about position and heading, we can build a very crude meteorological model! All the work in this blog post is based on this [paper](https://journals.plos.org/plosone/article/file?id=10.1371%2Fjournal.pone.0205029&type=printable) (code available at [github.com/junzis/meteo-particle-model](https://github.com/junzis/meteo-particle-model)). See also the [paper](https://erichorvitz.com/planesenors.pdf) by [Erich Orvitz](https://erichorvitz.com/) about a similar system ([from HN](https://news.ycombinator.com/item?id=44734515#44764111)).

ADS-B messages contain information about both ground speed (measured using a GPS) and airspeed (which is the plane’s speed relative to the surrounding air, measured by on-board sensors).

![Diagram showing how the wind speed and angle can be calculated from the air speed, ground speed, heading and track.](/assets/adsb-weather-model/a5e4dc769821c50e7e8d41397f1ac318.webp)

The ADS-B messages also contain the current heading and the track angle of the plane. The heading of the plane is direction the nose points in, while the track is the direction it moves in. These can diverge due to the wind shifting the plane from it’s actual course.

The difference between the vectors formed by (air speed, heading) and (ground speed, track) is the wind vector. By calculating this difference, we can infer wind speed at every point.

By combining this data from thousands of aircraft all over the sky we can build a little wind model that quite accurately simulates real wind conditions.

The paper by Junzi Sun also describes how to extract temperature and pressure from the data sent by the aircraft. By combining this with traditional meteorological models, [weather agencies can improve their forecasts](https://www.flightradar24.com/blog/b2b/flightradar24-and-met-office/).

## Building a Model

In order to test out the model, I first had to gather some data. After a quite measly run using my own antenna, I switched to [ADS-B Exchange’s historical data](https://www.adsbexchange.com/products/historical-data/). I pulled a total of 1.84 GB covering the 30th of April 2024.

Again, all credit goes to the authors of the paper, I only wrote some plumbing code to wrangle the data into a usable format and added some features to the visualisation for this blog post.

The model places the aircraft on a big grid. For each one, it spawns 300 particles scatter around it, which are initialised with the wind vector calculated for the aircraft. At each step, the particles are updated by a random walk.

![Annotated diagram from Junzi Sun’s paper showing the particles spawned in and subsequent sampling.](/assets/adsb-weather-model/a5e0d93e17b4acdf36abe84083aceb8f.webp)

To visualise the wind vectors, we need to measure the speed for each square of the map’s grid. To do this, we sample the particles for each square and take their average velocity vector. The more particles in a square, the higher the accuracy.

After letting the model run for a while, I got the following GIF - notice the outline of Europe in the background.

![GIF showing the wind over Europe over the span of about 5 hours.](/assets/adsb-weather-model/d38df532c7598f2589001c686b2c6742.gif)

Each frame contains data from about 650 aircraft. The step size of the simulation was set to 15 minutes - which is quite a lot. The density plot visualises the accuracy - more aircraft, higher accuracy. As this is during the night, there is less activity, which results in less data for the model.

## How Accurate is the Model?

While the wind vectors certainly do look interesting and somewhat realistic, are they really accurate? To compare the output of the simulation with real wind conditions, I found [Cameron Beccario](https://nullschool.net/)’s earth-wide wind visualisation at [earth.nullschool.net](https://earth.nullschool.net/).

![Comparison between my model and the reference model powered by GFS.](/assets/adsb-weather-model/176acdba386f449c4e6f9b31f35fd2c7.webp)

The comparison is not exact, but it’s pretty close. I tried to match up the same countries in both images and the height of the aircraft in my model is about 11km while the data on the right is for 250 hPa ([nullschool.net](https://earth.nullschool.net/about.html) says 250 hPa corresponds to about 10,500m).

You can recognise the same high-speed winds over the Mediterranean (from Greece to Turkey), where the speed even matches up quite closely - our model predicting 50 m/s (180 km/h) and the reference showing 152 km/h.

I’d say that’s a success!

I tried my best to replicate the style of the reference model to make a final visualisation.

![My data visualised in the style of ](/assets/adsb-weather-model/8d14febeec1386cffa94602688a18a2b.gif)

My data visualised in the style of [earth.nullschool.net](http://earth.nullschool.net/).

