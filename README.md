[![Build Status](https://travis-ci.org/madhavajay/nd889.svg?branch=master)](https://travis-ci.org/madhavajay/nd889)
[![@madhavajay](https://img.shields.io/badge/twitter-@madhavajay-blue.svg?style=flat)](http://twitter.com/madhavajay)

# Udacity - Artificial Intelligence Nanodegree - nd889

![AIND](img/udacity_AIND.png)

# Foundations of AI - Term 1
## Projects and Labs

1. [Solve a Sudoku with AI](1_foundations/1_sudoku/)
2. [Build a Game-Playing Agent](1_foundations/2_isolation/)
3. [Lab: Teaching Pac-Man to Search](1_foundations/3_pacman/)
4. [Lab: Simulated Annealing](1_foundations/4_simulated_annealing/)
5. [Lab: Constraint Satisfaction N-Queens](1_foundations/5_nqueens/)
6. [Implement a Planning Search](1_foundations/6_planning/)
7. [Build a Sign Language Recognizer](1_foundations/7_recognizer/)

# Deep Learning and Applications - Term 2
## Projects and Labs
1. MNIST
2. IMDB
3. CIFAR-10
4. [CNN Dog Breed Classifier](2_deep_learning/4_dog_breed_classifier/)
5. [RNN Apple Stock & Sherlock Holmes](2_deep_learning/5_rnn_stock_sherlock/)
6. [Lab: Affectiva SDK - Mimic Me!](2_deep_learning/6_cv_mimic_me/)

---

## Setup
This code uses the following:
- python 3.6
- [pylint](http://www.pylint.org) &amp; PEP 8 - Style Guide
- [mypy](http://mypy-lang.org) &amp; PEP 484 - Type Hints
- [pipenv](http://pipenv.org) &amp; PEP 508 - Dependency spec
- [pytest](http://pytest.org) - Tests

Install pipenv:
```bash
$ pip install pipenv
```

Change to project directory:
```bash
$ cd nd889
```

Initialize pipenv in python3 mode:
```bash
$ pipenv --three
```

Start pipenv shell
```bash
$ pipenv shell -c
```

Install project dependancies:
```bash
$ pipenv install
```

Run tests:
```bash
$ pytest
```
