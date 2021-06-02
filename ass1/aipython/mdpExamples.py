# mdpExamples.py - MDP Examples
# AIFCA Python3 code Version 0.8.6 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2020.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from mdpProblem import MDP

class party(MDP): 
    """Simple 2-state, 2-Action Partying MDP Example"""
    def __init__(self, discount=0.9):
        self.states = {'healthy','sick'}
        self.actions = {'relax', 'party'}
        self.discount = discount

    def R(self,s,a):
        "R(s,a)"
        return { 'healthy': {'relax': 7, 'party': 10},
                 'sick':    {'relax': 0, 'party': 2 }}[s][a]

    def P(self,s,a):
        "returns a dictionary of {s1:p1} such that P(s1 | s,a)=p1. Other probabilities are zero."
        phealthy = {  # P('healthy' | s, a)
                     'healthy': {'relax': 0.95, 'party': 0.7},
                     'sick': {'relax': 0.5, 'party': 0.1 }}[s][a]
        return {'healthy':phealthy, 'sick':1-phealthy}


class tiny(MDP):
    def __init__(self, discount=0.9):
        self.actions = ['right', 'upC', 'left', 'upR']
        self.states = [(x,y) for x in range(2) for y in range(3)]
        self.discount = discount

    def P(self,s,a):
        """return a dictionary of {s1:p1} if P(s1 | s,a)=p1. Other probabilities are zero.
        """
        (x,y) = s
        if a == 'right':
            return {(1,y):1}
        elif a == 'upC':
            return {(x,min(y+1,2)):1}
        elif a == 'left':
            if (x,y) == (0,2): return {(0,0):1}
            else: return {(0,y): 1}
        elif a == 'upR':
            if x==0:
                if y<2: return {(x,y):0.1, (x+1,y):0.1, (x,y+1):0.8}
                else:  # at (0,2)
                    return {(0,0):0.1, (1,2): 0.1, (0,2): 0.8}
            elif y < 2: # x==1
                return {(0,y):0.1, (1,y):0.1, (1,y+1):0.8}
            else: # at (1,2)
               return {(0,2):0.1, (1,2): 0.9}

    def R(self,s,a):
        (x,y) = s
        if a == 'right':
            return [0,-1][x]
        elif a == 'upC':
            return [-1,-1,-2][y]
        elif a == 'left':
            if x==0:
                return [-1, -100, 10][y]
            else: return 0
        elif a == 'upR':
            return [[-0.1, -10, 0.2],[-0.1, -0.1, -0.9]][x][y]
                # at (0,2) reward is   0.1*10+0.8*-1=0.2
                
class grid(MDP):
    """ dx * dy grid with rewarding states"""
    def __init__(self, discount= 0.9, dx=10, dy=10):
        self.dx = dx # size in x-direction
        self.dy = dy # size in y-direction
        self.actions = ['up', 'down', 'right', 'left']
        self.states = [(x,y) for x in range(dy) for y in range(dy)]
        self.discount = discount
        self.rewarding_states = {(3,2):-10, (3,5):-5, (8,2):10, (7,7):3}
        self.fling_states = {(8,2), (7,7)}
 
    def intended_next(self,s,a):
        """returns the next state in the direction a.
        This is where the agent will end up if to goes in its intended_direction (which it does with probability 0.7)
        """
        (x,y) = s
        if a=='up':
            return (x,  y+1 if y+1 < self.dy else y)
        if a=='down':
            return (x,  y-1 if y > 0 else y)
        if a=='right':
            return (x+1 if x+1 < self.dx else x,y)
        if a=='left':
            return (x-1 if x > 0 else x,y)

    def P(self,s,a):
        """return a dictionary of {s1:p1} if P(s1 | s,a)=p1. Other probabilities are zero.
        Corners are tricky because different actions result in same state.
        """
        if s in self.fling_states:
            return {(0,0): 0.25, (self.dx-1,0):0.25, (0,self.dy-1):0.25, (self.dx-1,self.dy-1):0.25}
        res = dict()
        for ai in self.actions:
            s1 = self.intended_next(s,ai)
            ps1 = 0.7 if ai==a else 0.1
            if s1 in res: # occurs in corners
                res[s1] += ps1
            else:
                res[s1] = ps1           
        return res       

    def R(self,s,a):
         if s in self.rewarding_states:
             return self.rewarding_states[s]
         else:
             (x,y) = s
             rew = 0 # rewards from crashing 
             if y==0: ## on bottom.
                 rew += -0.7 if a == 'down' else -0.1
             if y==self.dy-1: ## on top.
                 rew += -0.7 if a == 'up' else -0.1
             if x==0: ## on left
                 rew += -0.7 if a == 'left' else -0.1
             if x==self.dx-1: ## on right.
                 rew += -0.7 if a == 'right' else -0.1
             return rew
                
# Try the following:
# pt = party()
# pt.vi(1)
# pt.vi(100)

# gr = grid()
# q,v,pi = gr.vi(100)
# q[(7,2)]

