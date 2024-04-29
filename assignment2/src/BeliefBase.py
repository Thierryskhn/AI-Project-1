from __future__ import annotations
from collections import defaultdict # For type hints in class methods
from Belief import Belief, Not, And, Or, If, Iff, EmptyClause
from functools import reduce

class BeliefBase:
    """ Represents a belief base. """
    
    def __init__(self, *beliefs: Belief) -> None:
        self.beliefs = set(beliefs)
        

    def beliefs_by_rank(self)-> dict:
        """
        Transforms the beliefs of the belief base into a dictionary with ranks as keys
        and lists of beliefs with the same rank as values.
        """
        rank_dict = defaultdict(list)
        for belief in self.beliefs:
            if(not belief.rank == None):
                rank_dict[belief.rank].append(belief)
        return dict(sorted(rank_dict.items(), reverse=True))
    
    def add_ranked_beliefs(self,belief:Belief)->None:
        if belief.get_rank != None:
            self.ranked_beliefs | {belief.rank,belief}
    
    def get_rank(self,belief:Belief)->int:
        """ The rank of a belief b is defined by the largest rank i such that b entails 
         the base set of all beliefs of rank at least i """
        if Belief.is_tautology : return 1 # a tautology has order 1
        # BeliefBase([]).entails(belief)
        beliefs = []
        ranked_beliefs = self.beliefs_by_rank()
        for rank in ranked_beliefs.keys:
            beliefs += ranked_beliefs.get(rank)
            if BeliefBase(*beliefs).entails(belief): return rank
        return 0 


    def update(self,belief: Belief, new_rank:int)-> None:
        if belief in self.beliefs :
            belief.set_rank(new_rank)
        else: self.beliefs.add(belief.set_rank(new_rank))

    def get_beliefs(self) -> set:
        """ Returns the beliefs in the belief base. """
        return self.beliefs

    def __str__(self) -> str:
        return "{" + ", ".join([str(belief) for belief in self.beliefs]) + "}"
    
    def contract(self, belief : Belief) -> BeliefBase: 
        """ Implements entrenchment based contraction. """
        if BeliefBase(*[]).entails(belief): return BeliefBase(*self.beliefs) #is a tautology
        new_beliefs = []
        rank = belief.rank
        for b in self.beliefs:
            if b.rank > belief :
                b_or_input = self.get_rank(Or(b,belief))
                if b_or_input == belief.rank:
                    new_beliefs.append(b.set_rank(rank))
        return BeliefBase(*new_beliefs)
    
    def expand(self,belief : Belief, new_rank: int) -> BeliefBase:
        #TODO based on priority order as well 
        if belief.check_rank(new_rank):
            if not BeliefBase(*[]).entails(Not(belief)): return BeliefBase(*self.beliefs) #not consistent
        if belief in self.beliefs and belief.rank < new_rank: BeliefBase(*self.beliefs) #lower rank
        new_beliefs = list(self.beliefs.copy())
        sorted(new_beliefs,reverse=True)
        for i, b in enumerate(self.beliefs):
            if Belief(*new_beliefs[0:i+1]).entails(belief):
                if new_rank >= b.rank:
                    new_beliefs.add(belief.set_rank(new_rank))
                else:
                    break

        return BeliefBase(*new_rank)
    
    def add(self, belief : Belief) -> BeliefBase: 
        """ Expands the belief base by adding the belief to the belief base. """
        new_beliefs = self.beliefs.copy()
        new_beliefs.add(belief)
        return BeliefBase(*new_beliefs)
    
    
    def revise(self, belief: Belief,rank:int) -> BeliefBase:
        """ Revises the belief base by contracting the negative belief base and then expanding it with the new belief. """
        if belief.check_rank:
            new_beliefbase = BeliefBase(*self.beliefs)
            new_beliefbase.contract(Not(belief))
            new_beliefbase.expand(belief,rank)
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
        return self.resolution(self.add(Not(belief))) 

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

    a = Belief("a",0.5)
    b = Belief("b",0.4)
    a_or_b = Or(a, b,0.5)
    d = Belief("d",0.6)
    belief_base = BeliefBase(a, b, a_or_b,d)
    print(belief_base.beliefs_by_rank())
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