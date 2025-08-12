---
layout: page
title: "Voter Fraud in my Online Poll for the School Canteen"
time: 6 minutes
published: 2024-11-12
colortags: [{'id': '11658a68-3c22-4966-b5fe-93f7c296ba7e', 'name': 'Data Analysis', 'color': 'green'}, {'id': '26e3acab-0124-4773-a185-49dd8760c91c', 'name': 'API', 'color': 'orange'}, {'id': 'b4957fab-6b30-4589-a430-e71f10a30aeb', 'name': 'Web Development', 'color': 'purple'}]
tags: ['Data Analysis', 'API', 'Web Development']
permalink: school-canteen-ratings
favicon: school-canteen-ratings/favicon.png
excerpt: "I’m not sure you can really call someone rating their least favourite dish with 1/5 in an informal poll on my website voter fraud, but I sure felt like a detective uncovering a crime while looking through my logs and analytics. It also makes me look better than saying: “I allowed voting multiple times because of lacking security.”"
short: False
sourcecode: 
hn: 
math: False
image: assets/school-canteen-ratings/preview.png
---

I love building things on the internet, because people will interact with your stuff. They’ll mess with it through any and all mediums that someone creative might find. Exposing an API? Someone will misuse it! You’ll fix it, only for them to discover a different hole. You’re playing Whac-a-Mole with a person you’ve never seen, but you’re slowly puzzling together an idea of who they might be and what they’re like.

In this particular case, I discovered the lonely campaign of a user against their least favourite dish, flooding my feedback poll with negative votes.

<br/>

I re-visited my school recently to pick up a few documents after graduation. While waiting, I found a sticker, hiding on the far end of one of the outdoor lunch tables. What I had found were the last remnants of my first website that saw real users.

![<p>Sticker asking for ratings from the students with a QR code linking to the site.</p>](/assets/school-canteen-ratings/7fe95e07ca0d296ab6621de4fbe027b8.webp)

During my tenure in the student council there was a shift towards a more vegetarian regime, introducing no-meat days for example. Some people complained very vocally about the new policy, so our canteen’s direction wanted to gauge the students' reactions to the new menus.

I saw the perfect opportunity to get some real-world programming experience and thought why not build a website. After some hiccups, the site ran for 2 months and collected a total of 337 votes. In the grand scheme of things, that wasn’t a lot of people - but I had fun and learned a lot.

## Minimal Infrastructure

I built the site completely in Typescript, using NextJS for the front-end and ExpressJs on the back-end. Because this was supposed to be temporary and I had no idea how much data I would end up with, I went with a NoSQL Firebase solution and server-less hosting on Google Cloud. 

The server-less approach paid off - quite literally - and I forked over a total of 3.11€ to Google Cloud, excluding the domain.

## How to collect Feedback

After scanning one of the QR codes placed all over the canteen, students would access the following portal. They would select the menu they choose today - one of the 3 menus offered that particular day. They would then rate if from 1-5 and finally select which grade they are in.

![<p>Walk through of the app from a user’s perspective.</p>](/assets/school-canteen-ratings/a5d8f896a012abb25c92c8fbd8ceab86.webp)

In order to incentivise people to vote everyday, they needed to get something back from the site too. After rating today’s food, students were then able to see what others thought and how the votes evolved live. This also created some fun discussions when opinions on certain meals differed wildly.

![<p>Dashboard showing some meal’s statistics.</p>](/assets/school-canteen-ratings/e93df8d9b6adde83f81525027a7ad91b.webp)

## Some security Measures

While this was a school website, I still considered the threat model of a technically versed student trying to fuck with my results. Also, even more benign user interactions like accidental repeated voting should not be counted. I was proven right when I later discovered evidence of someone actually trying to manipulate the results.

I couldn’t require login, as this would increase friction too much and nobody would vote. So I had to find another way to block people from voting twice, both from their device and through the API. Preventing API access could have been accomplished - admittedly only by defence in depth - through a CSRF token loaded when requesting the page. But since I had already decided to split front-end and back-end, this would have been more complicated for what it was worth.

My first line of defence against people getting creative in order to vote twice was to simply store a cookie containing a UUID after they voted. If they tried to vote twice,  instead of notifying them that they had already voted, I discarded it silently on the back-end. This would give those that simply wanted to try manipulating the results a quick “success”, while preventing them from digging deeper to circumvent my defences.

I didn’t record the rejected voting attempts sadly, so I don’t know the true number of people just sitting there, thinking they had out-smarted the stupid guy that set up the site.

Some people managed to vote multiple times, either by clearing their cookies or by switching to incognito. I was able to count these duplicates thanks to a second layer of defense. In addition to the token, I also started storing a fingerprint and the voter’s IP server-side, along with their request.

![<p>Graph comparing unique votes vs. unfiltered votes over time.</p>](/assets/school-canteen-ratings/551da1abb8b2f5ee05c1cc8675abdd8f.webp)

On one of the final days that the site was live (the 11th of May), you can see an explosion in votes, but the unique count tells a different story. About two thirds of the votes were cast from the same device. 

More incriminating is the absence of a user token for each of the votes, something which couldn’t have happened, had the public front-end been correctly used.

This targeted disinformation campaign, flooding the meal’s ratings with 1/5s, was conducted against the truly worthy target of the “Topfenschmarn”, a sweet pancake made from curd, enjoyed with berries (see [this site for an example](https://www.milch.com/de/rezepte/topfenschmarrn-mit-zwetschkenroester-88/)). Usually this is a tasty delicacy, but our canteen indeed often butchered it.

I forgive this vigilante for his methods because of his clearly noble intentions, saving the next generation of pupils from this dish. It is also very funny to imagine someone clearing their browser’s cookies 27 times just to tarnish the reputation of a pancake.

## Analysing the Votes

So what are the most liked meals our school canteen offered? The most popular meal, with a perfect score were chicken wings - perhaps unsurprisingly for a school canteen.

If you look at the amount of green (vegetables) in the most popular and then the most unpopular meals, it doesn’t take a data scientist nor a sophisticated model to spot a trend.

 | Meal (translated) | Avg. Score | 
 | ---- | ---- | 
 | Chicken Wings | 5.0 | 
 | Pizza with salami | 4.5 | 
 | Ribs | 4.5 | 
 | … | … | 
 | Stir-fried vegetables and rice | 2.5 | 
 | Pork medallion with barley | 2.0 | 
 | Winter vegetable stir-fry | 1.7 | 

The data indeed confirms that vegetarian meals were rated, on average, almost an entire point lower than meals containing meat in some form or another, but mostly grilled or fried.

 | Vegetarian | Average Score | 
 | ---- | ---- | 
 | No | 3.80335 | 
 | Yes | 2.89559 | 

Sometimes you don’t discover new things when doing data analysis, sometimes you only confirm what you already knew. But it’s nice when intuition and the facts line up - even though it came at the expense of more healthy and balanced meals at school…

