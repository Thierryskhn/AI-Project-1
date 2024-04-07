from Assignment import Assignment

class Belief:
    """ Represents a belief in propositional logic. Variables are represented by their names, as strings. """

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return assignment[self.name]

class Not(Belief):
    """ Represents the negation of a belief's proposition.  """

    def __init__(self, belief: Belief) -> None:
        self.belief = belief

    def __str__(self) -> str:
        return "¬" + str(self.belief)

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return not self.belief.evaluate(assignment)

class And(Belief):
    """ Represents the conjunction of two beliefs' proposition. """
    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " ∧ " + str(self.right) + ")"

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

class Or(Belief):
    """ Represents the disjunction of two beliefs' proposition. """

    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " v " + str(self.right) + ")"

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

class If(Belief):
    """ Represents the implication of two beliefs' proposition. """

    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " → " + str(self.right) + ")"

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return not self.left.evaluate(assignment) or self.right.evaluate(assignment)

class Iff(Belief):
    """ Represents the biconditional of two beliefs' proposition. """
    
    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " ↔ " + str(self.right) + ")"

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

def main():
    print()

    a = Belief("a")
    b = Belief("b")
    c = Belief("c")
    d = Belief("d")
    print(And(a, b))
    print(Or(a, b))
    print(If(a, b))
    print(Iff(a, b))
    print(Not(a))
    print(Not(And(a, If(b, c))))

    print()

if __name__ == "__main__":
    main()