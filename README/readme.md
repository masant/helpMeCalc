helpMeCalc!

helpMeCalc! consists in a webpage that reunite some web applications ables to help engineering students
to calculate some problems. In the platform, it is possible return some calculations results and some plots.
In this initial version, it is possible to calculate Root Locus, Bode Diagram, Complex Numbers Conversions and Step Response, but,
the idea is improve this project as fast as possible.

All the project was build using Python (Flask), , HTML (w/ Jinja2), CSS and some basics of Javascript.
For plotting it was used matplotlib + mpld3 for root locus and bode; and bokeh (step response).
All topics about control theory, I use the (awesome) library control, that has a lot of complete solutions for this area.

I had to do some changes in the functions control.rlocus and control.bode:

control.rlocus
- I have to add the function to return the variable 'f' (plot figure) besides the other variables.
- I have to change the default plot color to green.

control.bode
- I have to add the function to return the variable 'f' (plot figure) besides the other variables.

This project have been my CS50x 2020 final project, where I could learn a lot about some computer science topics. My objective doing
this course was improve my programming skills and I can affirm that I, absolutely, get this goal! I'm way more confortable to
program in C, Python, HTML and CSS and, besides, I have learned some Javascript basic topics. But the idea behind CS50 is not
teach me a specific programming language but more than this: it teaches me the necessary theory to learn any programming language.

But I have much more to learn, this is just the beginning for more complex knowledges.

This was CS50 for me!