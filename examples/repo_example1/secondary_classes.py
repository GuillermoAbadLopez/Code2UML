from base_classes import Child, Parent

class AdoptedChild(Child):
    """Son class"""

    def __init__(self, name: str, parent1: Parent, parent2: Parent):
        """Initialise the bus.

        Args:
            name (str): Name of the son
            parent1 (Parent): Name of the first parent
            parent2 (Parent): Name of the second parent
        """
        super().__init__(name=name, parent1=parent1, parent2=parent2)
        self.name: str = name
        self.surname: str = parent1.surname + parent2.surname
        self.height: float = 150.0
        self.weight: float = 120.0
        self.iq_coef: float = 70.0