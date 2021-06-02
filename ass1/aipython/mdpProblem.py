# mdpProblem.py - Representations for Markov Decision Processes
# AIFCA Python3 code Version 0.8.6 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2020.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from utilities import argmaxd
import random

class MDP(object):
    """A Markov Decision Process. Must define:
    self.states the set (or list) of states
    self.actions the set (or list) of actions
    self.discount a real-valued discount
    """
    
    def P(self,s,a):
        """Transition probability function
        returns a dictionary of {s1:p1} such that P(s1 | s,a)=p1. Other probabilities are zero.
        """
        raise NotImplementedError("P")   # abstract method

    def R(self,s,a):
        """Reward function R(s,a)
        returns the expected reward for doing a in state s.
        """
        raise NotImplementedError("R")   # abstract method

    def vi(self,n, v0=None):
        """carries out n iterations of value iteration starting with value function v0.
        Returns a Q-function, value function, policy
        """
        assert n>0,"You must carry out at least one iteration of vi. n="+str(n)
        v = v0 if v0 is not None else {s:0 for s in self.states}
        for i in range(n):
            q = {s: {a: self.R(s,a)+self.discount*sum(p1*v[s1]
                                                          for (s1,p1) in self.P(s,a).items())
                      for a in self.actions}
                 for s in self.states}
            v = {s: max(q[s][a] for a in self.actions)
                  for s in self.states}
        pi = {s: argmaxd(q[s])
                  for s in self.states}
        return q,v,pi
    
    def avi(self,n):
          Q = {s:{a:0 for a in self.actions} for s in self.states}
          for i in range(n):
              s = random.choice(self.states)
              a = random.choice(self.actions)
              Q[s][a] = self.R(s,a) + self.discount * sum(p1*max(Q[s1][a1] for a1 in self.actions)
                                                  for (s1,p1) in self.P(s,a).items())
          return Q
    
