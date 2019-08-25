# Rumaro - An AI Image Analyzer

Rumaro uses AI to recognize emotions, apparel, body pose and activity in images, 
and measures how they affect audience engagement. ie. likes and comments.

>This started out as one of my weekend side hustles and was initially meant to be launched as a paid SAAS. But, on 
researching more about the privacy concerns, Instagrams restrictive APIs and mixed results from the initial tests I 
decided to scrape the idea and just Open Source it instead.

## Setup
1. Install the dependencies 
`pip install -r requirements.txt`
2. Run all the unit tests `pytest`
3. Run the actual analysis `python run_rumaro.py --instagram_id <INSTA_ID>`

### The why?

With Rumaro, I tried to identify *what* really made photos special!

I hypothesised that - Photos which the user liked, i.e photos which were more desirable could be identified using AI 
models and the key _features_ which made them special could be thus identified. 

I thought the Racy-ness, Body Pose and 
Apparel could be easily identified using Deep Learning and these would be the *only* features which would be driving the
social media engagement. 

### The how?

![Drag Racing](images/algo_dg.png)

![Drag Racing](images/block_db.png)

### Jumping off the sinking ship. 

But, unfortunately as I moved forward with the project I discovered that the coorelation between the different features
and the engagement was very weak. Also, this project had nightmarish privacy concerns which made it extremely difficult
to monetise and market. 

In retrospect it seems really obvious that the plan was a bit flawed from the square one. 
🤷🏽‍♂️

Ehh... I did get to play around with a lot of Deep Learning APIs, so all was good.   