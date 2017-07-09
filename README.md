[![Build Status](https://travis-ci.org/madhavajay/nd889.svg?branch=master)](https://travis-ci.org/madhavajay/nd889)
[![@madhavajay](https://img.shields.io/badge/twitter-@madhavajay-blue.svg?style=flat)](http://twitter.com/madhavajay)

# Udacity - Artificial Intelligence Nanodegree - nd889

![AIND](img/udacity_AIND.png)

# Foundations of AI - Term 1
## Projects and Labs

1. [Solve a Sudoku with AI](1_foundations/1_sudoku/README.md)
2. [Build a Game-Playing Agent](1_foundations/2_isolation/README.md)
3. [Lab: Teaching Pac-Man to Search](1_foundations/3_pacman/README.md)
4. [Lab: Simulated Annealing](1_foundations/4_simulated_annealing/README.md)
5. [Lab: Constraint Satisfaction N-Queens](1_foundations/5_nqueens/README.md)
6. [Implement a Planning Search](1_foundations/6_planning/README.md)
7. [Build a Sign Language Recognizer](1_foundations/7_recognizer/README.md)

# Deep Learning and Applications - Term 2
## Projects and Labs
1. MNIST
2. IMDB
3. CIFAR-10
4. [Dog Breed Classifier](2_deep_learning/4_dog_breed_classifier/README.md)

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
