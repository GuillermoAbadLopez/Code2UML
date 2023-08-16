class Child1:
    pass

class Child2:
    pass

class Parent:
    def __init__(self, surname: str):
        self.surname = surname


class Child(Child1, Child2):
    """Child class"""

    def __init__(self, name: str, parent1: Parent, parent2: Parent):
        """Initialise the AdoptedChild.

        Args:
            name (str): Name of the son
            parent1 (Parent): Name of the first parent
            parent2 (Parent): Name of the second parent
        """
        self.name: str = name
        self.surname: str = parent1.surname + parent2.surname
        self.height: float = 150.0
        self.weight: float = 120.0
        self.iq_coef: float = 70.0