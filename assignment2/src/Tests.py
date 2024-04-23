from BeliefBase import BeliefBase, Cn
from Belief import Belief, Not, And, Or, If, Iff

class BeliefBaseContractionTests:

    def __init__(self, beliefBase : BeliefBase):
        self.beliefBase = beliefBase    

    def closure(B: BeliefBase, belief: Belief):
        """ Tests the closure of the belief base. """
        print("Closure test")
        assert(B.contract(belief) == Cn(B))
        
    def success(belief: Belief, B: BeliefBase): 
        if belief not in Cn():
            #should be false
            assert(not(belief in Cn(B.contract(belief))))

    def inlusion(belief: Belief, B: BeliefBase):
       """Tests if the outcome is a subset of the original set""" 
       assert(B.contract(belief) in B)
    
    def vacuity(belief: Belief, B: BeliefBase):
        """Tests if the incoming sentence is not in the original set then there is no effect""" 
        if belief not in Cn(B):
            assert(B.contract(belief) == B)
    
    def extensionality(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests if the outcomes of contracting with equivalent sentences are the same""" 
        if(Iff(belief1, belief2) in Cn()):
            assert(B.contract(belief1) == B.contract(belief2))
    
    def recovery(belief: Belief, B: BeliefBase):
        """Contraction leads to the loss of as few previous beliefs as possible""" 

        #TODO just check in which way it works and it's cool
        assert(B in B.contract(belief).expand(belief))

    def conjunctive_inclusion(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the conjunctive inclusion property""" 
        if(belief1 not in B.contract(And(belief1, belief2))):
            assert(B.contract(And(belief1, belief2)) in B.contract(belief1))
    
    def conjunctive_overlap(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the conjunctive overlap property"""
        #TODO arranger ce test
        assert(union(B.contract(belief1).beliefs, B.contract(belief2).beliefs) in B.contract(And(belief1, belief2)).beliefs)

class BeliefBaseRevisionTests:

    def closure(B: BeliefBase, belief: Belief):
        """ Tests the closure of the belief base. """
        assert(B.revise(belief) == Cn(B.revise(belief)))
    
    def success(B: BeliefBase, belief: Belief):
        """Tests if the belief is in the belief base after revision"""
        assert(belief in B.revise(belief).beliefs)

    def inclusion(B: BeliefBase, belief: Belief):
        """Tests if the outcome is a subset of the original set""" 
        assert(B.revise(belief) in B.expand(belief))
    
    def vacuity(B: BeliefBase, belief: Belief):
        """Tests if the incoming sentence is not in the original set then there is no effect""" 
        if belief not in Cn(B):
            assert(B.revise(belief) == B)

    def extensionality(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests if the outcomes of contracting with equivalent sentences are the same"""
        if(Iff(belief1, belief2) in Cn()):
            assert(B.revise(belief1) == B.revise(belief2))

    def superexpansion(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the superexpansion property""" 
        assert(B.revise(And(belief1, belief2)) in B.revise(belief1).expand(belief2))

    def subexpansion(belief1: Belief, belief2: Belief, B: BeliefBase):
        """Tests the subexpansion property""" 
        if Not(belief1) not in Cn(B.revise(belief2)):
            assert(B.revise(belief2).expand(belief1) in B.revise(And(belief1, belief2)))