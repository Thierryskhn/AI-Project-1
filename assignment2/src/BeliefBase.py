from __future__ import annotations # For type hints in class methods
from Belief import Belief, Not, And, Or, If, Iff, EmptyClause
from functools import reduce

class BeliefBase:
    """ Represents a belief base. """
    
    def __init__(self, *beliefs: Belief) -> None:
        self.beliefs = set(beliefs)

    def get_beliefs(self) -> set:
        """ Returns the beliefs in the belief base. """
        return self.beliefs

    def __str__(self) -> str:
        return "{" + ", ".join([str(belief) for belief in self.beliefs]) + "}"
    
    def contract(self, belief : Belief) -> BeliefBase: 
        """ Contracts the belief base by removing the belief from the belief base. """
        #TODO base it on priority order
        new_beliefs = self.beliefs.copy()
        new_beliefs.remove(belief)
        return BeliefBase(*new_beliefs)
    
    def expand(self, belief : Belief) -> BeliefBase: 
        """ Expands the belief base by adding the belief to the belief base. """
        new_beliefs = self.beliefs.copy()
        new_beliefs.add(belief)
        return BeliefBase(*new_beliefs)
    
    def revise(self, belief: Belief) -> BeliefBase:
        """ Revises the belief base by contracting the negative belief base and then expanding it with the new belief. """
        new_beliefbase = BeliefBase(*self.beliefs)
        new_beliefbase.contract(Not(belief))
        new_beliefbase.expand(belief)
        return new_beliefbase
    
    ## TODO: keep?
    def to_cnf_set(self) -> list[list[Belief]]:
        """ Converts the belief to a set of clauses (set that can be interpreted as a CNFs). 
            This allows for the resolution algorithm to be applied,
            enabling it to iterate over the clauses and literals to resolve them.
        """
        beliefCNFs = [belief.to_cnf() for belief in self.beliefs]
        ands = reduce(lambda b1, b2: And(b1, b2), beliefCNFs)

        if isinstance(ands, And):
            return self._to_list_and(ands)

        return [{ands}]

    ## TODO: keep?
    def _to_list_and(self, belief: Belief):
        """ Takes a CNF belief and converts it to a list of the clauses,
            where each clause is a set of the literals (Beliefs or their negations).
        """
        if isinstance(belief, And):
            return self._to_list_and(belief.left) + self._to_list_and(belief.right)
        elif isinstance(belief, Or):
            return [self._to_set_or(belief)]
        else:
            return [{belief}]
    
    ## TODO: keep?
    def _to_set_or(self, belief: Belief):
        """ Takes a DNF belief and converts it to a set of the clauses. """
        if isinstance(belief, Or):
            return self._to_set_or(belief.left) | self._to_set_or(belief.right)
        else:
            return {belief}

    def entails(self, belief: Belief) -> bool:
        """ Checks if the belief follows from the belief base using resolution. """
        return self.resolution(self.expand(Not(belief)))

    def resolution(self, beliefbase: BeliefBase) -> bool:
        """ Implements the resolution algorithm. """

        # Initial clauses contain the negated belief and the existing beliefs
        clauses = self.to_cnf_set()
        
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    resolvents = self.resolve_pair(clauses[i], clauses[j])
                    if EmptyClause() in resolvents:
                        return True  # Empty clause found, contradiction, so belief follows
                    new_clauses.extend(resolvents)
            if set(new_clauses).issubset(set(clauses)):
                return False  # No new clauses generated, no contradiction found
            clauses.extend(new_clauses)

    def resolve_pair(clause1: list[Belief], clause2: list[Belief]) -> list[Belief]:
        """ Resolves two clauses to produce new resolvents. """
        resolvents = []
        for belief1 in clause1:
            for belief2 in clause2:
                if belief1 == Not(belief2) or Not(belief1) == belief2:
                    resolvents.append(list(set(clause1 + clause2) - {belief1, belief2}))
        return resolvents

def main():
    def print_cnf_set(cnf_set):
        return "[" + ", ".join(['{' + ", ".join([str(c) for c in clause]) + '}' for clause in cnf_set]) + "]"

    print()

    a = Belief("a")
    b = Belief("b")
    a_or_b = Or(a, b)
    d = Belief("d")
    belief_base = BeliefBase(a, b, a_or_b)
    print(belief_base)
    belief_base = belief_base.expand(d)
    print(belief_base)
    belief_base = belief_base.contract(a)
    print(belief_base)

    print("to_cnf_set:")
    print(BeliefBase(Belief("a")))
    print(print_cnf_set(BeliefBase(Belief("a")).to_cnf_set()))

    print(belief_base)
    print(print_cnf_set(belief_base.to_cnf_set()))

    belief_base2 = BeliefBase(*[c.to_cnf() for c in [Not(a), Not(b), Not(a_or_b), And(a, b)]])
    print(belief_base2)
    print(print_cnf_set(belief_base2.to_cnf_set()))

    print()

if __name__ == "__main__":
    main()