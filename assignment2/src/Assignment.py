from __future__ import annotations

class Assignment:
    """ Represents a set of assignments to variables. """

    def __init__(self, assignments: dict[str, bool]) -> None:
        self.assignments = assignments

    def __getitem__(self, key: str) -> bool:
        return self.assignments[key]

    def __setitem__(self, key: str, value: bool) -> None:
        self.assignments[key] = value

    def __str__(self) -> str:
        return str(self.assignments)
    
    def get_all_assignments(beliefs: list) -> list[Assignment]:
        """ Returns all possible assignments. """
        return [Assignment({str(key): value for key, value in zip(beliefs, assignment)}) for assignment in [[True, False] * len(beliefs)]]
    
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