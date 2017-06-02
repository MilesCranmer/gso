""" This file organizes the different answers from each query result to load
"""

from gso import search_google

def load_up_answers(question, language='', answers=5):
    """ Load up answers from a question to Google

    Args:
        
        question: String question, what you would google for

        language: (optional) specific language inferred from filename

        answers: (optional, default 5) the number of answers to load
            
    Returns:
        
        res: a list of JSON (for each answer), parsed from stack overflow
    """
    query = search_google(question, language=language)
