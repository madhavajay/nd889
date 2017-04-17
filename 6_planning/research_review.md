## Udacity - Artificial Intelligence Nanodegree - nd889

# Research Review - Historical Developments in AI Planning and Search

## The First Robot
![Shakey](img/shakey.jpg)

Planning "is about the decision making performed by intelligent creatures like robots, humans, or computer programs when trying to achieve some goal. It involves choosing a sequence of actions that will (with a high likelihood) transform the state of the world, step by step, so that it will satisfy the goal. The world is typically viewed to consist of atomic facts (state variables), and actions make some facts true and some facts false." **[\[1\]](#user-content-references)**

In 1971, Richard E. Fikes and Nils J. Nilsson published a paper in Artificial Intelligence, a then new journal on the topic of AI, entitled: "STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving".

Their new problem-solving program called STRIPS (STanford Research Institute Problem Solver) implemented in LISP was a member of the class of
problem solvers that search a space of "world models" to find one in which a
given goal is achieved.

They claimed that for any world model, there exists a set of applicable operators, each of which transforms the world model to some other world model. **[\[2\]](#user-content-references)**

This and earlier developments from Fikes and Nilsson such as the greatly improved graph search algorithm named A* Search **[\[3\]](#user-content-references)** would go on to provide the basis for "Shakey the robot" the first mobile robot with the ability to perceive and reason about its surroundings. **[\[4\]](#user-content-references)**

## Graph Theory
![Graph](img/graph.jpg)

In 1995, Avrim Blum and Merrick Furst created Graphplan "a general-purpose planner for STRIPS-style domains, based on ideas used in graph algorithms."

Given a problem statement, Graphplan explicitly constructs and annotates a compact structure called a Planning Graph, in which a plan is a kind of "flow" of truth-values through the graph.

This graph has the property that useful information for constraining search can quickly be propagated through the graph as it is being built. Graphplan then exploits this information in the search for a plan. **[\[5\]](#user-content-references)**

Traditional AI planners did very little compilation but after Graphplan, which was the first compiling planner, at AIPS (Artificial Intelligence Planning Systems) '98 nearly all AI planners were using a variety of compilation techniques with great success. **[\[6\]](#user-content-references)**

As time went on, improvements to STRIPS were made, in particular the attempt at standardizing AI planning languages with PDDL (Planning Domain Definition Language).

PDDL was created to express the "physics" of a domain. What predicates there are, what actions are possible, what the structure of compound actions is, and what the effects of actions are. **[\[7\]](#user-content-references)**

Although the core of PDDL is STRIPS, the ability to express objects in domains using type structures and constrain these with predicates provide many of the extensions proposed in ADL (Action description language). **[\[8\]](#user-content-references)**

## Probabilistic Planning
![Monte Carlo Localization](img/mcl.jpg)

Although these ideas and formalisms worked quite well for classical planning, in particular deterministic and observable state spaces, there soon began a need for novel solutions to non-deterministic problems.

According to AAAI (Association For The Advancement Of Artificial Intelligence) the classic paper Monte Carlo Localization: Efficient Position Estimation for Mobile Robots from 1999 provides one such advancement in solving the non-deterministic problem of robot localization by the application of probabilistic state estimation using Monte Carlo Localization. **[\[9\]](#user-content-references)**

The paper co-written by Udacity's own Sebastian Thrun, provides a memory and computation efficient algorithm which utilizes random sampling to represent a robots belief state. By allowing for faster sampling MCL can incorporate more frequent sensor data which results in higher accuracy. **[\[10\]](#user-content-references)**

## Planetary Rovers
![Planetary Rover](img/rover.jpg)

Fast forward to 2016 and ICAPS accepted papers such as PARIS: A Polynomial-Time, Risk-Sensitive Scheduling Algorithm for
Probabilistic Simple Temporal Networks with Uncertainty are making strides in solving temporal uncertainty problems faced by planetary rovers, providing a linear problem encoding for typical temporal uncertainty models, outperforming current state of the art algorithms and optimised to run on limited resource hardware. **[\[11\]](#user-content-references)**

In addition the winner of the ICAPS Influential Paper Award 2016 was A Planning Heuristic Based on Causal Graph Analysis, a paper from 2004 which demonstrates that improvements on relaxed requirements heuristic search methods can be achieved by replacing STRIPS with The SAS+ Planning Formalism.

This alternative avoids problems where the STRIPS algorithm often loses vital information when ignoring "delete lists" during relaxed heuristics, which results in problems like dead ends in the search space. **[\[12\]](#user-content-references)**

## Conclusion
The field of Planning and Search has developed and changed dramatically over the past 50 years, from the humble beginnings of the first mobile decision making robot with percepts, shakey; through algorithm and language development, the merging of the AIPS and ECP bi-annual conferences into the ICAPS conference, ideas in probabilistic and non-deterministic planning, through to today's cutting edge advancements destined for humanity's farthest and most difficult planning frontier, space exploration.


# References

[1] [A brief overview of AI planning](https://users.ics.aalto.fi/rintanen/planning.html)

[2] [STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving](http://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/strips.pdf)

[3] [A Formal Basis for the Heuristic Determination of Minimum Cost Paths](http://ai.stanford.edu/~nilsson/OnlinePubs-Nils/PublishedPapers/astar.pdf)

[4] [SRI International - Timeline of Innovation](https://www.sri.com/work/timeline-innovation/timeline.php?timeline=computing-digital#!&innovation=shakey-the-robot)

[5] [Graphplan home page](http://www.cs.cmu.edu/~avrim/graphplan.html)

[6] [Plan compilation](http://www.cs.cmu.edu/~jcl/compileplan/compiling_planner.html)

[7] [The Planning Domain Definition Language](http://icaps-conference.org/ipc2008/deterministic/data/mcdermott-et-al-tr-1998.pdf)

[8] [PDDL Background](https://www.cs.cmu.edu/afs/cs/project/jair/pub/volume20/fox03a-html/node2.html)

[9] [AAAI Classic Paper Award](http://www.aaai.org/Awards/classic.php)

[10] [Monte Carlo Localization: Efficient Position Estimation for Mobile Robots](http://robots.stanford.edu/papers/fox.aaai99.pdf)

[11] [PARIS: A Polynomial-Time, Risk-Sensitive Scheduling Algorithm for Probabilistic Simple Temporal Networks with Uncertainty](http://www.aaai.org/ocs/index.php/ICAPS/ICAPS16/paper/view/13138/12687)

[12] [A Planning Heuristic Based on Causal Graph Analysis](http://www.aaai.org/Papers/ICAPS/2004/ICAPS04-021.pdf)
