from __future__ import annotations
from itertools import product

class Assignment:
    """ Represents a set of assignments to variables. """

    def __init__(self, assignments: dict[str, bool]) -> None:
        self.assignments = assignments

    def __getitem__(self, key: str) -> bool:
        return self.assignments[key]

    def __setitem__(self, key: str, value: bool) -> None:
        self.assignments[key] = value

    def __str__(self) -> str:
        return "{" + str(', '.join([f"{key}: {value}" for key, value in self.assignments.items()])) + "}"
    
    def extend(self, key: str, value: bool) -> Assignment:
        """ Returns a new assignment with the given key and value. """
        assignments = self.assignments.copy()
        assignments[key] = value
        return Assignment(assignments)

    def get_all_assignments(*beliefs) -> list[Assignment]:
        """ Returns all possible assignments. """
        values = [True, False]
        return [Assignment(dict(zip(beliefs, assignment))) for assignment in product(values, repeat=len(beliefs))]

def main():
    print()

    assignment = Assignment({"a": True, "b": False, "c": True})
    print(assignment)
    print(assignment["a"])
    print(assignment["b"])
    print(assignment["c"])
    assignment["a"] = False
    print(assignment)

    print()

if __name__ == "__main__":
    main()