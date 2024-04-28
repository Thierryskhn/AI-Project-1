To create a proposition (represented by an instance of the Belief class) there are two ways :

- use the constructors :
  a ∧ b is created with
  a = Belief("a")
  b = Belief("b")
  a_and_b = And(a, b)

  similarly, for any proposition:
  first create its variables with Belief("name") and then compose them with any Belief subclass.

- use sympy :
  create a proposition p using sympy and convert it using Belief.from_sympy(p)

It is then possible to create and use belief bases using these Beliefs :
bb1 = BeliefBase(a)
bb2 = BeliefBase(a, a_and_b)
bb3 = BeliefBase(a, b, a_and_b)
...
