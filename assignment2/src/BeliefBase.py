from __future__ import annotations # For type hints in class methods
from Belief import Belief, Not, And, Or, If, Iff

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
        self.beliefs.remove(belief)
        return self
    
    def expand(self, belief : Belief) -> BeliefBase: 
        """ Expands the belief base by adding the belief to the belief base. """
        self.beliefs.add(belief)
        return self
    
    def revise(self, belief: Belief) -> BeliefBase:
        """ Revises the belief base by contracting the negative belief base and then expanding it with the new belief. """
        self.contract(Not(belief))
        self.expand(belief)
        return self

def main():
    print()

    a = Belief("a")
    b = Belief("b")
    a_or_b = Or(a, b)
    d = Belief("d")
    belief_base = BeliefBase(a, b, a_or_b)
    print(belief_base)
    belief_base.expand(d)
    print(belief_base)
    belief_base.contract(a)
    print(belief_base)

    print()

if __name__ == "__main__":
    main()