from __future__ import annotations
import inspect

from Assignment import Assignment
from sympy import symbols
from sympy.logic.boolalg import to_cnf, Equivalent, Implies, And as AndSympy, Or as OrSympy, Not as NotSympy, Boolean

from functools import reduce

class Belief:
    """ Represents a belief in propositional logic. Variables are represented by their names, as strings. """

    def from_sympy(boolean: Boolean) -> Belief:
        """ Returns the belief from a sympy boolean. """
        if isinstance(boolean, Belief):
            return boolean

        if isinstance(boolean, Equivalent):
            return reduce(lambda curr, next: Iff(Belief.from_sympy(curr), Belief.from_sympy(next)), boolean.args)
        elif isinstance(boolean, Implies):
            return If(Belief.from_sympy(boolean.args[0]), Belief.from_sympy(boolean.args[1]))
        elif isinstance(boolean, AndSympy):
            return reduce(lambda curr, next: And(Belief.from_sympy(curr), Belief.from_sympy(next)), boolean.args)
        elif isinstance(boolean, OrSympy):
            return reduce(lambda curr, next: Or(Belief.from_sympy(curr), Belief.from_sympy(next)), boolean.args)
        elif isinstance(boolean, NotSympy):
            return Not(Belief.from_sympy(boolean.args[0]))
        elif boolean == True:
            return ValidClause()
        elif boolean == False:
            return EmptyClause()
        else:
            return Belief(boolean.name)

    def to_sympy(self) -> Boolean:
        """ Returns the belief in sympy format. """
        if isinstance(self, Iff):
            return Equivalent(self.left.to_sympy(), self.right.to_sympy())
        elif isinstance(self, If):
            return Implies(self.left.to_sympy(), self.right.to_sympy())
        elif isinstance(self, And):
            return AndSympy(self.left.to_sympy(), self.right.to_sympy())
        elif isinstance(self, Or):
            return OrSympy(self.left.to_sympy(), self.right.to_sympy())
        elif isinstance(self, Not):
            return NotSympy(self.belief.to_sympy())
        elif isinstance(self, ValidClause):
            return True
        elif isinstance(self, EmptyClause):
            return False
        else:
            return symbols(self.name)

    def to_cnf(self) -> Belief:
        return Belief.from_sympy(to_cnf(self.to_sympy()))

    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Belief) and self.name == other.name
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        if self.name not in assignment.keys():
            return None

        return assignment[self.name]

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return {self.name}

class ValidClause(Belief):
    """ Represents a valid clause, i.e. a tautology. """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "⊤"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, ValidClause)
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return True

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return set()

class EmptyClause(Belief):
    """ Represents an empty clause, i.e. a contradiction. """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "⊥"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, EmptyClause)
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return False

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return set()

class Not(Belief):
    """ Represents the negation of a belief's proposition.  """

    def __init__(self, belief: Belief) -> None:
        self.belief = belief

    def __str__(self) -> str:
        return "¬" + str(self.belief)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Not) and self.belief == other.belief
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        if self.belief.evaluate(assignment) == None:
            return None

        return not self.belief.evaluate(assignment)

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return self.belief.get_variables()

class And(Belief):
    """ Represents the conjunction of two beliefs' proposition. """
    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " ∧ " + str(self.right) + ")"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, And) and ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))
    
    def __hash__(self) -> int:
        return hash(str(self)) + hash(str(And(self.right, self.left)))
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        if self.left.evaluate(assignment) == None or self.right.evaluate(assignment) == None:
            return None

        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return self.left.get_variables() | self.right.get_variables()

class Or(Belief):
    """ Represents the disjunction of two beliefs' proposition. """

    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " v " + str(self.right) + ")"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Or) and ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))
    
    def __hash__(self) -> int:
        return hash(str(self)) + hash(str(Or(self.right, self.left)))

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        if self.left.evaluate(assignment) == None and self.right.evaluate(assignment) == False or self.right.evaluate(assignment) == False and self.left.evaluate(assignment) == None:
            return None

        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return self.left.get_variables() | self.right.get_variables()

class If(Belief):
    """ Represents the implication of two beliefs' proposition. """

    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " → " + str(self.right) + ")"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, If) and self.left == other.left and self.right == other.right
    
    def __hash__(self) -> int:
        return hash(str(self))

    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return  Not(self.left).evaluate(assignment) or self.right.evaluate(assignment)

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return self.left.get_variables() | self.right.get_variables()

class Iff(Belief):
    """ Represents the biconditional of two beliefs' proposition. """
    
    def __init__(self, left: Belief, right: Belief) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return "(" + str(self.left) + " ↔ " + str(self.right) + ")"
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Iff) and ((self.left == other.left and self.right == other.right) or (self.left == other.right and self.right == other.left))

    def __hash__(self) -> int:
        return hash(str(self)) + hash(str(Iff(self.right, self.left)))
    
    def evaluate(self, assignment: Assignment) -> bool:
        """ Evaluates the belief given an assignment to variables. """
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def get_variables(self) -> set[str]:
        """ Returns the variables in the belief. """
        return self.left.get_variables() | self.right.get_variables()

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

    print("\nget_variables:")
    a_and_b = And(a, b)
    print(a_and_b)
    print(a_and_b.get_variables())

    not_b_and_a_or_d_if_c = And(Or(a, If(c, d)), Not(b))
    print(not_b_and_a_or_d_if_c)
    print(not_b_and_a_or_d_if_c.get_variables())
    print(Or(a, not_b_and_a_or_d_if_c).get_variables())

    print("\nto_sympy:")
    print(not_b_and_a_or_d_if_c)
    print(not_b_and_a_or_d_if_c.to_sympy())
    
    print("\nfrom_sympy:")
    print(not_b_and_a_or_d_if_c)
    print(Belief.from_sympy(not_b_and_a_or_d_if_c.to_sympy()))

    print("\nto_cnf:")
    print(not_b_and_a_or_d_if_c)
    print(not_b_and_a_or_d_if_c.to_cnf())

    print()

if __name__ == "__main__":
    main()