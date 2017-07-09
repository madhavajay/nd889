# -*- coding: utf-8 -*-
# Author: github.com/madhavajay
"""
These are various classes to select the optimal number of components in a
Hidden Markov Model to represent the sign language word translation problem.
"""
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict,
                 this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states,
                                    covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state,
                                    verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        # pylint: disable=broad-except
        except Exception:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN

    Lower BIC is better
    """

    # : BIC = −2 log L + p log N,
    # where L is the likelihood of the fitted model, p is the number of
    # parameters, and N is the number of data points. The term −2 log L
    # decreases with increasing model complexity (more parameters), whereas the
    # penalties 2p or p log N increase with increasing complexity.
    # The BIC applies a larger penalty
    # when N > e
    # 2 = 7.4.

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        lowest_bic = float('inf')
        best_model = None
        for n_components in range(self.min_n_components,
                                  self.max_n_components + 1):
            try:
                model = self.base_model(n_components)

                # BIC = −2 log L + p log N
                # L = log likelihood
                # p = number of parameters in model
                # N = number of data points

                logL = model.score(self.X, self.lengths)

                # p = n^2 + 2*d*n - 1
                # n = components (different to the big N)
                # d = features
                p = (n_components * n_components +
                     2 * model.n_features * n_components - 1)

                # BIC = −2 log L + p log N
                bic = -2 * logL + p * np.log(len(self.X))

                if bic < lowest_bic:
                    lowest_bic = bic
                    best_model = model
            # pylint: disable=broad-except
            # exceptions vary and occurs deep in other external classes
            except Exception:
                continue

        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application
    to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings.
    Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        highest_dic = float('-inf')
        best_model = None
        for n_components in range(self.min_n_components,
                                  self.max_n_components + 1):
            try:
                # train the whole model with this number of components
                model = self.base_model(n_components)
                # get the data for the word we are trying to score for
                X_word, lengths_word = self.hwords[self.this_word]
                # log likelihood of total model on all data with n_components
                # of predicting the target word
                target_logL = model.score(X_word, lengths_word)
            # pylint: disable=broad-except
            # exceptions vary and occurs deep in other external classes
            except Exception:
                continue

            antiLogL = 0
            word_count = 0
            for word in self.words:
                if word is not self.this_word:
                    # get the data for each other word
                    X_word, lengths_word = self.hwords[word]
                    try:
                        # score the log likelihood of the model misguessing
                        # this word instead
                        logL_word = model.score(X_word, lengths_word)
                        antiLogL += logL_word
                        word_count += 1

                    # pylint: disable=broad-except
                    # exceptions vary and occurs deep in other external classes
                    except Exception:
                        continue

            # DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
            # DIC = log likelihood - average log likelihood of other words
            dic = target_logL - (1 / (word_count - 1)) * antiLogL

            if dic > highest_dic:
                highest_dic = dic
                best_model = model

        return best_model


class SelectorCV(ModelSelector):
    '''
    select best model based on average log Likelihood of cross-validation folds
    '''

    def run_model(self, n_components, X_train, lengths_train, X_test,
                  lengths_test):
        model = GaussianHMM(n_components=n_components, covariance_type="diag",
                            n_iter=1000, random_state=self.random_state,
                            verbose=False).fit(X_train, lengths_train)
        logL = model.score(X_test, lengths_test)
        return logL

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # hide hmmlearn==0.2.0 warnings
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        best_model = None
        highest_average = float('-inf')
        n_splits = min(len(self.sequences), 3)

        for n_components in range(self.min_n_components,
                                  self.max_n_components + 1):
            total_logL = 0
            iterations = 0
            try:
                if n_splits > 1:
                    split_method = KFold(n_splits=n_splits)
                    seq_splits = split_method.split(self.sequences)
                    for cv_train_idx, cv_test_idx in seq_splits:
                        X_train, lengths_train = combine_sequences(
                            cv_train_idx, self.sequences)
                        X_test, lengths_test = combine_sequences(
                            cv_test_idx, self.sequences)

                        logL = self.run_model(n_components, X_train,
                                              lengths_train, X_test,
                                              lengths_test)

                        total_logL += logL
                        iterations += 1
                else:
                    logL = self.run_model(n_components, self.X, self.lengths,
                                          self.X, self.lengths)
                    total_logL += logL
                    iterations += 1

                average_logL = total_logL / iterations
                if average_logL > highest_average:
                    highest_average = average_logL
                    best_model = self.base_model(n_components)

            # pylint: disable=broad-except
            # exceptions vary and occurs deep in other external classes
            except Exception:
                continue

        return best_model
