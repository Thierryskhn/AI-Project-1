from Belief import Belief, Not, And, Or, If, Iff

class BeliefBase:
    """ Represents a belief base. """
    
    def __init__(self, *beliefs: Belief) -> None:
        self.beliefs = set(beliefs)

    def add_belief(self, belief: Belief) -> None:
        """ Adds a belief to the belief base. """
        self.beliefs.add(belief)

    def remove_belief(self, belief: Belief) -> None:
        """ Removes a belief from the belief base. """
        self.beliefs.remove(belief)

    def get_beliefs(self) -> set:
        """ Returns the beliefs in the belief base. """
        return self.beliefs

    def __str__(self) -> str:
        return "{" + ", ".join([str(belief) for belief in self.beliefs]) + "}"

def main():
    print()

    a = Belief("a")
    b = Belief("b")
    c = Or(a, b)
    d = Belief("d")
    belief_base = BeliefBase(a, b, c)
    print(belief_base)
    belief_base.add_belief(d)
    print(belief_base)
    belief_base.remove_belief(a)
    print(belief_base)

    print()

if __name__ == "__main__":
    main()