from __future__ import annotations # For type hints in class methods
from Belief import Belief, Not, And, Or, If, Iff, EmptyClause
from Assignment import Assignment
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

    def to_cnf_set(self) -> list[list[Belief]]:
        """ Converts the belief to a set of clauses (set that can be interpreted as a CNFs). 
            This allows for the resolution algorithm to be applied,
            enabling it to iterate over the clauses and literals to resolve them.
        """

        beliefs = list(self.beliefs)

        if len(beliefs) == 0:
            return [[EmptyClause()]]
        
        if len(beliefs) == 1:
            return [[beliefs[0].to_cnf()]]
        
        ands = And(beliefs[0].to_cnf(), beliefs[1].to_cnf())

        for belief in beliefs[2:]:
            ands = And(ands, belief.to_cnf())

        return BeliefBase._flatten_cnf_and(ands, [])

    def _flatten_cnf_and(belief: Belief, current: list[list[Belief]]) -> list[list[Belief]]:
        """ Flattens an And belief to a list of beliefs. """
        new_current = current.copy()

        if not isinstance(belief, And):
            return new_current + [belief]

        if isinstance(belief.left, And):
            new_current += BeliefBase._flatten_cnf_and(belief.left, new_current)
        elif isinstance(belief.left, Or):
            new_current.append(BeliefBase._flatten_cnf_or(belief.left, new_current))
        else:
            new_current.append([belief.left])
        
        if isinstance(belief.right, And):
            new_current += BeliefBase._flatten_cnf_and(belief.right, new_current)
        elif isinstance(belief.right, Or):
            new_current.append(BeliefBase._flatten_cnf_or(belief.right, new_current))
        else:
            new_current.append([belief.right])

        return new_current
        
        
    def _flatten_cnf_or(belief: Or, current: list[Belief]) -> list[Belief]:
        """ Flattens an Or belief to a list of beliefs. 
            As it is assumed that the belief is in CNF, the Or should only contain literals.
        """
        new_current = current.copy()

        if isinstance(belief.left, Or):
            new_current += BeliefBase._flatten_cnf_or(belief.left, new_current)
        else:
            new_current.append(belief.left)

        if isinstance(belief.right, Or):
            new_current += BeliefBase._flatten_cnf_or(belief.right, new_current)
        else:
            new_current.append(belief.right)

        return new_current

    def entails(self, belief: Belief) -> bool:
        """ Checks if the belief follows from the belief base using the DPLL algorithm.
            Week 10: Testing entailment φ |= ψ, is done by testing unsatisfiability of φ ∧ ¬ψ
        """
        return self._dpll_satisfiable(self.expand(Not(belief))) == False

    def _dpll_satisfiable(base: BeliefBase) -> bool:
        clauses = base.to_cnf_set()
        symbols = [belief.get_variables() for belief in base.get_beliefs()]

        return BeliefBase._dpll(clauses, symbols, Assignment({}));

    def _dpll(clauses: list[list[Belief]], symbols: list[set[str]], model: Assignment) -> bool:
        if all(clause.eval(model) for clause in clauses):
            return True

        if not any(clause.eval(model) for clause in clauses):
            return False
    
        p, value = BeliefBase._find_pure_symbols(clauses, symbols, model)

        if p:
            return BeliefBase._dpll(clauses, symbols, model.extend(p, value))

        p, value = BeliefBase._find_unit_clause(clauses, symbols, model)

        if p:
            return BeliefBase._dpll(clauses, symbols, model.extend(p, value))

        p = symbols[0]
        rest = symbols[1:]

        return BeliefBase._dpll(clauses, rest, model.extend(p, True)) or BeliefBase._dpll(clauses, rest, model.extend(p, False))

    def _find_pure_symbols(clauses: list[list[Belief]], symbols: list[set[str]], model: Assignment):
        p = None

        for symbol in symbols:
            positive = False
            negative = False

            for clause in clauses:
                if symbol in clause:
                    positive = True
                if Not(symbol) in clause:
                    negative = True

            if positive != negative:
                p = symbol
                value = positive
                break
        
        return p, value

    def _find_unit_clause(clauses: list[list[Belief]], symbols: list[set[str]], model: Assignment):
        return p, value

def main():
    def print_cnf_set(cnf_set):
        return "[" + ", ".join([str(belief) for beliefs in cnf_set for belief in beliefs]) + "]"

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

    belief_base2 = BeliefBase(Not(a), Not(b), If(Not(a), Not(b)))
    print('base ' + str(belief_base2))
    print('cnf ' + print_cnf_set(belief_base2.to_cnf_set()))

    print()

if __name__ == "__main__":
    main()