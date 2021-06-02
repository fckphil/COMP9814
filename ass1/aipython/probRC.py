from probGraphicalModels import Graphical_model, Inference_method
from probFactors import Factor
from utilities import dict_union

class RC(Inference_method):
    """The class that queries graphical models using recursive conditioning

    gm is graphical model to query
    """


   
    def __init__(self,gm=None):
        self.gm = gm
        self.cache = {CacheElt({},[]):1}
        self.max_display_level = 3

    def query(self,var,obs={},elim_order=None):
        """computes P(var|obs) where
        var is a variable
        obs is a variable:value dictionary
        elim_order is a list of the non-observed non-query variables in gm"""
        if var in obs:
            return {val:(1 if val == obs[var] else 0) for val in var.domain}
        else:
           if elim_order == None:
                elim_order = [v for v in self.gm.variables if (v not in obs) and v != var]
           unnorm = [self.rc(dict_union({var:val},obs), self.gm.factors, elim_order) for val in var.domain]
           p_obs = sum(unnorm)
           return {val:pr/p_obs for val,pr in zip(var.domain, unnorm)}


    def rc(self, context, factors, elim_order):
        """ returns the number \sum_{elim_order} \prod_{factors} given assignments in context
        context is a variable:value dictionary
        factors is a list of factors
        elim_order is a list of variables in factors that are not in context
        """
        self.display(1,"calling rc,",(context,factors))
        ce = CacheElt(context, factors)   # key for the appropriate cache entry
        if ce in self.cache:
            self.display(2,"rc cache lookup")
            return self.cache[ce]
#        if factors == []:  # needed if you don't have forgetting and caching
#            return 1
        elif vars_not_in_any_factor := [var for var in context if not any(var in fac.variables for fac in factors)]:
             # forget variables not in any factor
            self.display(2,"rc forgetting variables", vars_not_in_any_factor)
            return self.rc({key:val for (key,val) in context.items() if key not in vars_not_in_any_factor},
                            factors, elim_order)
        elif to_eval := [fac for fac in factors if all(v in context for v in fac.variables)]:
            # evaluate factors when all variables are assigned
            self.display(2,"rc evaluating factors")
            val = prod(fac.get_value(context) for fac in to_eval)
            if val == 0:
                return 0
            else:
             return val * self.rc(context, [fac for fac in factors if fac not in to_eval], elim_order)
        elif len(comp := connected_components(context, factors, elim_order)) >= 1:
            # there are disconnected components
            self.display(2,"splitting into conected components",comp)
            return(prod(self.rc(context,f,eo) for (f,eo) in comp))
        else:
            assert elim_order, "elim_order should not be empty to get here"
            total = 0
            var = elim_order[-1]
            self.display(2, "rc branching on", var)
            for val in var.domain:
                total += self.rc(dict_union({var:val},context), factors, elim_order[:-1])
            self.cache[ce] = total
            self.display(2, "rc branching on", var,"returning", total)
            return total


    def rc0(self, context, factors, elim_order):
        """simplest search algorithm"""
        self.display(1,"calling rc,",(context,factors))
        if elim_order == []:
            # evaluate factors when all variables are assigned
            self.display(2,"rc evaluating factors")
            return prod(fac.get_value(context) for fac in factors) 
        else:
            total = 0
            var = elim_order[-1]
            self.display(2, "rc branching on", var)
            for val in var.domain:
                total += self.rc0(dict_union({var:val},context), factors, elim_order[:-1])
            self.display(2, "rc branching on", var,"returning", total)
            return total

def connected_components(context, factors, elim_order):
    """returns a list of (f,e) where f subset of factors and e subset of elim_order
    such that each element shares the same variables that are disjoint from other elements.
    """
    seed = factors[0]
    other_factors = set(factors[1:])
    to_check = [seed]
    component_factors = set()  # factors in first connected component
    component_variables = set(seed.variables)
    while to_check != []:
        next_fac = to_check.pop()
        component_factors.add(next_fac)
        new_vars = set(next_fac.variables) - component_variables - context.keys()
        for var in new_vars:
            to_check.append([f for f in other_factors if any(v not in component_variables and v not in context for v in f.variables)])
            other_factors.difference_update(to_check) # set difference
    bn1v.display(3,"In connected_components","component_factors",component_factors,"component_variables",component_variables,"other_factors",other_factors)
    if other_factors:
        return [(factors, elim_order)]
    else:
        return ( [(component_factors,[e for e in elim_order if e in component_variables])]
                      + connected_components(context, other_factors, [e for e in elim_order if e not in component_variables]) )
    
        
def prod(en):
    res = 1
    for e in en:
        res *= e
    return res


class CacheElt(object):
    """The elements in the cache for recursive conditioning. 
    It should contain the context and the factors and must be hashable.
    """
    def __init__(self,context,factors):
        self.context = context
        self.frozen_factors = frozenset(factors)
        self.hash_val = hash((frozenset((var,val) for (var,val) in self.context.items()), self.frozen_factors))

    def __hash__(self):
        return self.hash_val

    def __eq__(self,other):
        return isinstance(other, CacheElt) and self.context == other.context and self.frozen_factors == other.frozen_factors

from probGraphicalModels import bn1, A,B,C
bn1v = RC(bn1)
## bn1v.query(A,{})
## bn1v.query(C,{})
## Inference_method.max_display_level = 3   # show more detail in displaying
## Inference_method.max_display_level = 1   # show less detail in displaying
## bn1v.query(A,{C:True})
## bn1v.query(B,{A:True,C:False})

from probGraphicalModels import bn2,Al,Fi,Le,Re,Sm,Ta
bn2v = RC(bn2)    # answers queries using variable elimination
## bn2v.query(Ta,{})
## Inference_method.max_display_level = 0   # show no detail in displaying
## bn2v.query(Le,{})
## bn2v.query(Ta,{},elim_order=[Sm,Re,Le,Al,Fi])
## bn2v.query(Ta,{Re:True})
## bn2v.query(Ta,{Re:True,Sm:False})

from probGraphicalModels import bn3, Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet
bn3v = RC(bn3)
## bn3v.query(Shoes_wet,{})
## bn3v.query(Shoes_wet,{Rained:True})
## bn3v.query(Shoes_wet,{Grass_shiny:True})
## bn3v.query(Shoes_wet,{Grass_shiny:False,Rained:True})

