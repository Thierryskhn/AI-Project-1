from __future__ import annotations
from collections import defaultdict # For type hints in class methods
from Belief import Belief, Not, And, Or, If, Iff, EmptyClause
from Assignment import Assignment
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
        if not belief in self.beliefs:
            return self

        new_beliefs = []
        rank = belief.rank
        for b in self.beliefs:
            if b.rank > belief :
                b_or_input = self.get_rank(Or(b,belief))
                if b_or_input == belief.rank:
                    b.set_rank(rank)
                    new_beliefs.append(b)
        return BeliefBase(*new_beliefs)
    
    def expand(self, belief: Belief) -> BeliefBase: 
        """ Expands the belief base by adding the belief to the belief base. """
        new_beliefs = self.beliefs.copy()
        new_beliefs.add(belief)
        return BeliefBase(*new_beliefs)
    
    def add(self, belief : Belief) -> BeliefBase: 
        """ Expands the belief base by adding the belief to the belief base. """
        new_beliefs = self.beliefs.copy()
        new_beliefs.add(belief)
        return BeliefBase(*new_beliefs)

    def revise(self, belief: Belief,) -> BeliefBase:
        """ Revises the belief base by contracting the negative belief base and then expanding it with the new belief. """
        new_beliefbase = BeliefBase(*self.beliefs)
        new_beliefbase.contract(Not(belief,rank))
        new_beliefbase.expand(belief,rank)
        return new_beliefbase

    def to_cnf_list(self) -> list[list[Belief]]:
        """ Converts the belief to a list of clauses (each clause is a list of literals).
            This allows for the DPLL algorithm to be applied,

            Example: if the CNF is (a v b) ∧ (¬a v b), the output will be [[a, b], [¬a, b]]
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
            new_current.append(BeliefBase._flatten_cnf_or(belief.left))
        else:
            new_current.append([belief.left])
        
        if isinstance(belief.right, And):
            new_current += BeliefBase._flatten_cnf_and(belief.right, new_current)
        elif isinstance(belief.right, Or):
            new_current.append(BeliefBase._flatten_cnf_or(belief.right))
        else:
            new_current.append([belief.right])

        return new_current
        
        
    def _flatten_cnf_or(belief: Or) -> list[Belief]:
        """ Flattens an Or belief to a list of beliefs. 
            As it is assumed that the belief is in CNF, the Or should only contain literals.
        """
        new_current = []

        if isinstance(belief.left, Or):
            new_current += BeliefBase._flatten_cnf_or(belief.left)
        else:
            new_current.append(belief.left)

        if isinstance(belief.right, Or):
            new_current += BeliefBase._flatten_cnf_or(belief.right)
        else:
            new_current.append(belief.right)

        return new_current

    def entails(self, belief: Belief) -> bool:
        """ Checks if the belief follows from the belief base using the DPLL algorithm.
            Week 10: Testing entailment φ |= ψ, is done by testing unsatisfiability of φ ∧ ¬ψ
        """
        return BeliefBase._dpll_satisfiable(self.expand(Not(belief))) == False

    def _dpll_satisfiable(base: BeliefBase) -> bool:
        clauses = base.to_cnf_list()
        symbols =  {variable for belief in base.get_beliefs() for variable in belief.get_variables()}

        return BeliefBase._dpll(clauses, symbols, Assignment({}));

    def _dpll(clauses: list[list[Belief]], symbols: set[str], model: Assignment) -> bool:

        if all(any(belief.evaluate(model) is True for belief in clause) for clause in clauses):
            return True

        if any(all(belief.evaluate(model) is False for belief in clause) for clause in clauses):
            return False

        p, value = BeliefBase._find_pure_symbols(clauses, symbols, model)

        if p is not None:
            return BeliefBase._dpll(clauses, symbols - {p}, model.extend(p, value))

        p, value = BeliefBase._find_unit_clause(clauses, symbols, model)

        if p is not None:
            return BeliefBase._dpll(clauses, symbols - {p}, model.extend(p, value))

        p, *rest = symbols

        return BeliefBase._dpll(clauses, rest, model.extend(p, True)) or BeliefBase._dpll(clauses, rest, model.extend(p, False))

    def _find_pure_symbols(clauses: list[list[Belief]], symbols: set[str], model: Assignment) -> tuple[str, bool]:
        p = None
        value = None

        for symbol in symbols:
            positive = False
            negative = False

            for clause in clauses:
                if Belief(symbol) in clause:
                    positive = True
                if Not(Belief(symbol)) in clause:
                    negative = True

            if positive != negative:
                p = symbol
                value = positive
                break
        
        return p, value

    def _find_unit_clause(clauses: list[list[Belief]], symbols: set[str], model: Assignment):
        p = None
        value = None

        return p, value

def main():
    cnf_tests()
    entailment_tests()
    ...

def cnf_tests():
    def print_cnf_set(cnf_set):
        return "[" + ", ".join(["[" + ", ".join([str(literal) for literal in clause]) + "]" for clause in cnf_set]) + "]"

    print("\nCNF tests:")

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
    print('base ' + str(BeliefBase(Belief("a"))))
    print('cnf ' + print_cnf_set(BeliefBase(Belief("a")).to_cnf_list()))

    print('base ' + str(belief_base))
    print('cnf ' + print_cnf_set(belief_base.to_cnf_list()))

    belief_base2 = BeliefBase(Not(a), Not(b), If(Not(a), Not(b)))
    print('base ' + str(belief_base2))
    print('cnf ' + print_cnf_set(belief_base2.to_cnf_list()))

    print()

def entailment_tests():
    print("\nEntailment tests:")

    a = Belief("a")
    b = Belief("b")
    c = Belief("c")
    d = Belief("d")
    belief_base = BeliefBase(a, b, c, d)
    print("\nBelief base: " + str(belief_base))
    print(str(a) + ": " + str(belief_base.entails(a)) + " should be True")
    print(str(Not(a)) + ": " + str(belief_base.entails(Not(a))) + " should be False")
    print(str(And(a, b)) + ": " + str(belief_base.entails(And(a, b))) + " should be True")
    print(str(And(a, Not(b))) + ": " + str(belief_base.entails(And(a, Not(b)))) + " should be False")
    print(str(And(a, And(b, c))) + ": " + str(belief_base.entails(And(a, And(b, c)))) + " should be True")
    print(str(And(And(a, b), Not(c))) + ": " + str(belief_base.entails(And(And(a, b), Not(c)))) + " should be False")
    print(str(And(And(a, b), And(c, d))) + ": " + str(belief_base.entails(And(And(a, b), And(c, d)))) + " should be True")
    print(str(And(And(a, b), And(And(c, d), Not(d)))) + ": " + str(belief_base.entails(And(And(a, b), And(And(c, d), Not(d))))) + " should be False")

    belief_base2 = BeliefBase(Not(a), Not(b), If(Not(a), Not(b)))
    print("\nBelief base 2: " + str(belief_base2))
    print(str(Not(a)) + ": " + str(belief_base2.entails(Not(a))) + " should be True")
    print(str(a) + ": " + str(belief_base2.entails(a)) + " should be False")
    print(str(Not(b)) + ": " + str(belief_base2.entails(Not(b))) + " should be True")
    print(str(a) + ": " + str(belief_base2.entails(b)) + " should be False")
    print(str(If(Not(a), Not(b))) + ": " + str(belief_base2.entails(If(Not(a), Not(b)))) + " should be True")
    print(str(If(a, Not(b))) + ": " + str(belief_base2.entails(If(a, Not(b)))) + " should be True")
    print(str(If(Not(a), b)) + ": " + str(belief_base2.entails(If(Not(a), b))) + " should be False")
    print(str(If(a, b)) + ": " + str(belief_base2.entails(If(a, b))) + " should be True")

    nothing = BeliefBase()
    print("\nBelief base 3: " + str(nothing))

    print(str(a) + ": " + str(nothing.entails(a)) + " should be False")
    print(str(Not(a)) + ": " + str(nothing.entails(Not(a))) + " should be False")
    print(str(And(a, b)) + ": " + str(nothing.entails(And(a, b))) + " should be False")
    print(str(And(a, Not(b))) + ": " + str(nothing.entails(And(a, Not(b)))) + " should be False")
    print(str(And(a, And(b, c))) + ": " + str(nothing.entails(And(a, And(b, c)))) + " should be False")
    print(str(Iff(a, a)) + ": " + str(nothing.entails(Iff(a, a))) + " should be True")
    print(str(Iff(a, c)) + ": " + str(nothing.entails(Iff(a, c))) + " should be False")

    print()

if __name__ == "__main__":
    main()