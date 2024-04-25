from BeliefBase import BeliefBase, _dpll, _find_pure_symbols, _find_unit_clause, entails
from Belief import Belief, Not, And, Or, If, Iff

class BeliefBaseContractionTests:

    def __init__(self, beliefBase : BeliefBase):
        self.beliefBase = beliefBase    

    #TODO : We might have to change the way by adding to every B ".beliefs" 

    def closure(B: BeliefBase, belief: Belief):
        """ Tests the closure of the belief base. """

        #TODO : Make a better closure because we cannot do it right now. 
        #Maybe we can't do it because it is computationally expensive.
        print("Closure test")
        assert(B.contract(belief) == Cn(B))
        
    def success(belief: Belief, B: BeliefBase):
        """Tests if the outcome does not contain the belief"""
        nothingBase = BeliefBase()
        if not(nothingBase.entails(belief)):
            #should be false
            assert(not(B.contract(belief).entails(belief)))
    
    def inlusion(belief: Belief, B: BeliefBase):
       """Tests if the outcome is a subset of the original set""" 
       assert(B.contract(belief).beliefs.isssubset(B.beliefs))
    
    def vacuity(belief: Belief, B: BeliefBase):
        """Tests if the incoming sentence is not in the original set then there is no effect""" 
        if not B.entails(belief) :
            assert(B.contract(belief).beliefs == B.beliefs)
    
    def extensionality(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests if the outcomes of contracting with equivalent sentences are the same"""

        nothing = BeliefBase()
        if(nothing.entalis(Iff(belief1, belief2))):
            assert(B.contract(belief1).beliefs == B.contract(belief2).beliefs)
    
    def recovery(belief: Belief, B: BeliefBase):
        """Contraction leads to the loss of as few previous beliefs as possible""" 
        #TODO just check in which way it works and it's cool
        assert(B.issubset(B.contract(belief).expand(belief)))

    def conjunctive_inclusion(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the conjunctive inclusion property""" 
        if(belief1 not in B.contract(And(belief1, belief2))):
            assert(B.contract(And(belief1, belief2)).issubset(B.contract(belief1)))
    
    def conjunctive_overlap(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the conjunctive overlap property"""
        #TODO arranger ce test
        assert(B.contract(belief1).beliefs
               .intersection(B.contract(belief2).beliefs)
               .issubset(B.contract(And(belief1, belief2)).beliefs))

class BeliefBaseRevisionTests:

    def closure(B: BeliefBase, belief: Belief):
        """ Tests the closure of the belief base. """
        #TODO: may be impossible due to the computotionnal cost of creating the belief set 
        assert(B.revise(belief) == Cn(B.revise(belief)))
    
    def success(B: BeliefBase, belief: Belief):
        """Tests if the belief is in the belief base after revision"""
        assert(belief in B.revise(belief).beliefs)

    def inclusion(B: BeliefBase, belief: Belief):
        """Tests if the outcome is a subset of the original set""" 
        assert(B.revise(belief).beliefs.issubset(B.expand(belief)))
    
    def vacuity(B: BeliefBase, belief: Belief):
        """Tests if the incoming sentence is not in the original set then there is no effect""" 
        if B.entails(belief):
            assert(B.revise(belief).beliefs == B.beliefs)

    def extensionality(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests if the outcomes of contracting with equivalent sentences are the same"""
        nothing = BeliefBase()
        if(nothing.entalis(Iff(belief1, belief2))):
            assert(B.revise(belief1) == B.revise(belief2))

    def superexpansion(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the superexpansion property""" 
        assert(B.revise(And(belief1, belief2)).issubset(B.revise(belief1).expand(belief2)))

    def subexpansion(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the subexpansion property""" 
        if Not(belief1) not in Cn(B.revise(belief2)):
            assert(B.revise(belief2).expand(belief1).isssubset(B.revise(And(belief1, belief2))))