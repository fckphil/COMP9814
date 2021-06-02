# cspExamples.py - Example CSPs
# AIFCA Python3 code Version 0.8.2 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2020.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import CSP, Constraint        
from operator import lt,ne,eq,gt


def queens(ri,rj):
    """ri and rj are different rows, return the condition that the queens cannot take each other"""
    def no_take(ci,cj):
        "is true if queen are (ri,ci) cannot take a queen are (rj,cj)"
        return ci != cj and abs(ri-ci) != abs(rj-cj)
    return no_take

def n_queens(n):
    """returns a CSP for n-queens"""
    columns = list(range(n))
    return CSP(
               {'R'+str(i):columns for i in range(n)},
                [Constraint(['R'+str(i),'R'+str(j)], queens(i,j)) for i in range(n) for j in range(n) if i != j])

from cspConsistency import Con_solver
qs = Con_solver(n_queens(5))
# qs.solve_one()
