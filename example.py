import os
from gso import load_up_answers, load_up_questions
import stackexchange

#for result in load_up_questions("How to write a bubble sort", "python"):
    #print result
    #break

SE_KEY = os.environ["SE_KEY"]

question_id = 895371
so = stackexchange.Site(stackexchange.StackOverflow)
