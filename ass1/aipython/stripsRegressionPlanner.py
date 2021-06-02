# stripsRegressionPlanner.py - Regression Planner with STRIPS actions
# AIFCA Python3 code Version 0.8.6 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2020.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from searchProblem import Arc, Search_problem

class Subgoal(object):
    def __init__(self,assignment):
        self.assignment = assignment
        self.hash_value = None
    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(frozenset(self.assignment.items()))
        return self.hash_value
    def __eq__(self,st):
        return self.assignment == st.assignment
    def __str__(self):
        return str(self.assignment)

from stripsForwardPlanner import zero

class Regression_STRIPS(Search_problem):
    """A search problem where:
    * a node is a goal to be achieved, represented by a set of propositions.
    * the dynamics are specified by the STRIPS representation of actions
    """

    def __init__(self, planning_problem, heur=zero):
        """creates a regression search space from a planning problem.
        heur(state,goal) is a heuristic function; 
           an underestimate of the cost from state to goal, where
           both state and goals are feature:value dictionaries
        """
        self.prob_domain = planning_problem.prob_domain
        self.top_goal = Subgoal(planning_problem.goal)
        self.initial_state = planning_problem.initial_state
        self.heur = heur

    def is_goal(self, subgoal):
        """if subgoal is true in the initial state, a path has been found"""
        goal_asst = subgoal.assignment
        return all(self.initial_state[g]==goal_asst[g]
                   for g in goal_asst)

    def start_node(self):
        """the start node is the top-level goal"""
        return self.top_goal

    def neighbors(self,subgoal):
        """returns a list of the arcs for the neighbors of subgoal in this problem"""
        goal_asst = subgoal.assignment
        return [ Arc(subgoal, self.weakest_precond(act,goal_asst), act.cost, act)
                 for act in self.prob_domain.actions
                 if self.possible(act,goal_asst)]

    def possible(self,act,goal_asst):
        """True if act is possible to achieve goal_asst.

        the action achieves an element of the effects and
        the action doesn't delete something that needs to be achieved and
        the preconditions are consistent with other subgoals that need to be achieved
        """
        return ( any(goal_asst[prop] == act.effects[prop]
                    for prop in act.effects if prop in goal_asst) 
                and all(goal_asst[prop] == act.effects[prop]
                        for prop in act.effects if prop in goal_asst)
                and all(goal_asst[prop]== act.preconds[prop]
                        for prop in act.preconds if prop not in act.effects and prop in goal_asst)
                )

    def weakest_precond(self,act,goal_asst):
        """returns the subgoal that must be true so goal_asst holds after act
        should be:   act.preconds | (goal_asst - act.effects)
        """
        new_asst = act.preconds.copy()
        for g in goal_asst:
            if g not in act.effects:
                new_asst[g] = goal_asst[g]
        return Subgoal(new_asst)

    def heuristic(self,subgoal):
        """in the regression planner a node is a subgoal.
        the heuristic is an (under)estimate of the cost of going from the initial state to subgoal.
        """
        return self.heur(self.initial_state, subgoal.assignment)

from searchBranchAndBound import DF_branch_and_bound
from searchMPP import SearcherMPP 
from stripsProblem import problem0, problem1, problem2, blocks1, blocks2, blocks3

# SearcherMPP(Regression_STRIPS(problem1)).search()   #A* with MPP
# DF_branch_and_bound(Regression_STRIPS(problem1),10).search() #B&B

