# Bayes Filter 2D

***This class activity is to be done as individuals, not with partners nor with teams.***

## How to get started →

Begin by reading this entire writeup and making sure you have a good understanding of it. Next, spend some time planning how you’re going to approach the problem. 

### Introduction

---

In this activity, you'll explore the principles of Bayesian reasoning as applied to robotics. You will guide a virtual robot across a 2D grid, using Bayesian filters to integrate prior knowledge with new sensor data. The objective is to gain a foundational understanding of how robots interpret and respond to their environment amidst uncertainty. This exercise underscores the importance of probability and decision-making in the domain of robotics.

### Bayesian Estimation

The methods robots interact with the real world are not perfect, as a result, we need to treat the information we receive and the actions we make with a bit of skepticism. This is where Bayesian reasoning comes in, where we use information about our priors combined with new information we receive, to understand our current state, the posterior. A Bayes filter applies the principal of Bayesian reasoning to create a belief update process that combines the prior and new information, either incoming sensor or outgoing movement information. It’s a Markov process that only depends on the current state and newly received information. Using a sequence of observations and actions, the Bayes filter can keep track of the robot even with noisy data. 

### Action Model (Motion Model)

The action model, also known as the motion model, describes how an agent’s state changes due to its actions. It predicts the next state given the current state and a specific action. This model is often represented as a probability distribution P(s′∣s,a), where s is the current state, a is the action taken, and s′ is the resulting state.

In this activity an example action model is treated as follows
```python
action = [0.2,0.6,0.2]
Probability of moving 0 steps: 0.2
Probability of moving 1 step: 0.6
Probability of moving 2 steps: 0.2
```

**When the robot is at the edge of the grid, the impossible probabilities get added to the next possible action. Eg. if the world was a linear grid of 5 blocks [0,1,2,3,4] and the robot is at block 3, if it received an action of R, the probability of a 2 step is not possible (5 does not exist) thus the probability of a 1 step increases from 0.6 to 0.8 (IMPORTANT DISTINCTION). If the robot was at block 0 with an action of L then the only possible move is a 0 move (since there is no way to come from -1 or -2 (IMPORTANT DISTINCTION). Thus the probability of 0 step becomes 1.0**

### Observation Model

The observation model defines how likely an observation is, given a particular state. It captures the probability P(o∣s), where o is the observation and s is the state. The observation model accounts for sensor noise or inaccuracies, meaning that even if the system is in a particular state, the observed measurement may not always perfectly reflect it.

In this activity an example observation model is treated as follows
```python
observation = [0.1,0.2,0.4,0.2,0.1]
idx = i
Probability of observing a correct value at i: 0.4
Probability of observing a correct value at i-1, i+1: 0.2 each
Probability of observing a correct value at i-2, i+2: 0.1 each
```

> For edge cases when an observation lies outside the array, add the probabilities to the closest valid observation

## Objectives

- Understand how to do Bayesian Inference
- Implementing a simple Grid Bayes Filter example
  
## Resources

- [Bayes Filter Intro](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa13/slides/bayes-filters.pdf)
- [Robotik - Ep.1: Intro to State Estimation and Bayes Filter](https://rrwiyatn.github.io/blog/robotik/2020/05/03/intro-to-state-estimation-and-bayes-filter.html)


## What we provide

- Sample ROS2 package that handles the subscriptions and plotting node of the most recent belief array

## What to submit

You must submit a package with the following structure:

```bash
bayesian_estimation
├── bayesian_estimation
│   ├── bayesian_estimation.py # Code to compute the new beliefs
│   └── __init__.py
├── launch
│   └── bayesian_estimation.launch.py # Launch file to spawn the sample plotter. (No change necessary)
├── package.xml
├── README.md
├── resource
│   └── bayesian_estimation
├── setup.cfg
├── setup.py
└── test
    ├── test_copyright.py
    ├── test_flake8.py
    └── test_pep257.py
```

*Please make sure you adhere to the structure above, if your package doesn’t match it the grader will give you a **zero***



### Grading considerations

- **Late submissions:** Carefully review the course policies on submission and late assignments. Verify before the deadline that you have submitted the correct version.
- **Environment, names, and types:** You are required to adhere to the names and types of the functions and modules specified in the release code. Otherwise, your solution will receive minimal credit.

## Getting Started

Update the `setupModels` function with the correct probabilities. Refer the models above
```python
def setupModels(self):
    # Initialize the arrays for action 
    # and observation probabilities
    self.action_probs = None
    self.obs_probs = None
```

The `Bayes_Estimator` node provided in the template `bayesian_estimation.py` file consists of a Subscriber `/robot` of the type `std_msgs/String`. This subscriber will listen to published strings and if the format is correct, call the appropriate function with the appropriate data.

Eg. if the subscriber receives a string `"Rn"` then means an action update in the right direction n times. `"R2 D2 L2 U2"` means right twice, down twice, left twice and then finally up twice. You can change the order and count as required. 

If the string contains substrings of the form `"Xn"` means a sensor update. The first part is the observation direction, and the 2nd part is the index. Thus, for `"X10"`, all grid cells where X = 10 and its neighbors will be updated. X <= 7 and X>=13 will be 0 since (8,9,10,11,12) are the only valid locations. String can also be `"Y10"` or `"X10 Y10"`.

## Part 1 - Action Update

```python
def action_update(self, motion):
    '''
    Args:
    motion: string of direction of action.
    Can only be 'U', 'D', 'L', 'R'
    
    Function estimationCb() in this file calls this function 
    when it receives an action command n times. 
    Uses the current belief (self.belief) and the action 
    to compute the new belief.
    
    Returns:
    new_belief: numpy array of new belief after action update
    '''
```

The action update is defined in the following function. Input is the cardinal direction of motion. It uses the defined action model for computation. Upon running this part, your distribution should spread.

**Performing action update decreases maximum probability (but the total sum remains 1).**

## Part 2 - Observation Update
```python
def observation_update(self, obs):
    '''
    Args:
    obs: string of observation. Is of the form 'Xn' or 'Yn' 
    where n is index of the observation.
    X10 means that the sensor thinks that all X values with index 10 
    are likely to be true. 
    Y5 would mean that all Y values with index 5 are 
    likely to be true.
    
    Function estimationCb() in this file calls this function 
    when it receives an observation command. Uses the current belief 
    (self.belief) and the observation to compute the new belief.
    
    Returns:
    new_belief: numpy array of new belief after sensor update
    '''
```

The observation updated is defined as mentioned. The `obs` parameter is of the form `"Xn"` or `"Yn"`. `n` indicates the relevant index of the observation and `X/Y` define the direction. Upon running this, your distribution should contract.

**Note: The sum of all the beliefs should be equal to 1, as total probability is equal to 1. Therefore, the beliefs after every calculation have to be normalized.**

**Performing observation update increases maximum probability (but the total sum changes) thus it requires normalization.**


## Demonstration
Video: https://youtu.be/Fdrw080pqTQ


# Submission and Assessment

---

Submit your code using the Github upload feature on [autolab](https://autolab.cse.buffalo.edu). 

**Note: Make sure your code complies to all instructions, especially the naming conventions. Failure to comply will result in zero credit.**

You will be graded on the following. Penalties are listed under each point, absolute values, w.r.t activity total.

1. Action Update (50%)
    - If beliefs don't add upto 1 (-25%)
    - Edge case not accounted for (-25%)
2. Observation Update (50%)
    - If beliefs don't add upto 1 (-25%)
    - Relevant rows/columns not affected (-25%)

