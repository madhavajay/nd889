# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""
This is a function to determine the probabilities and best guesses for a test
set against a dictionary of word: model pairs
"""

import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

    :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
    :param test_set: SinglesData object
    :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # return probabilities, guesses
    all_xlengths = test_set.get_all_Xlengths()
    for _, data_tuple in all_xlengths.items():
        x_vals, lengths = data_tuple
        words = {}
        for word, model in models.items():
            try:
                words[word] = model.score(x_vals, lengths)
            # pylint: disable=broad-except
            # exceptions vary and occurs deep in other external classes
            except Exception:
                words[word] = float('-inf')
        probabilities.append(words)

    guesses = [max(probs, key=probs.get)
               for probs in probabilities]
    return probabilities, guesses
