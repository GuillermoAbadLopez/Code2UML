"""main file of the example, defining the Parent and Child classes"""

class Parent():
    """Parent class"""
    
    def __init__(self, name: str, surname: str, height: float, weight: float, iq_coef: float):
        """Initialise the bus.

        Args:
            name (str): Name of the parent
            surname (str): First surname of the parent
            height (int): Height of the parent
            weight (int): Weight of the parent
            iq (int): IQ of the parent
        """
        self.name: str = name
        self.surname: str = surname
        self.height: float = height
        self.weight: float = weight
        self.iq_coef: float = iq_coef  


class Child():
    """Son class"""

    def __init__(self, name: str, parent1: Parent, parent2: Parent):
        """Initialise the bus.

        Args:
            name (str): Name of the son
            parent1 (Parent): Name of the first parent
            parent2 (Parent): Name of the second parent
        """
        self.name: str = name
        self.surname: str = parent1.surname + parent2.surname
        self.height: float = (parent1.height + parent2.height)/2
        self.weight: float = (parent1.weight + parent2.weight)/2
        self.iq_coef: float = (parent1.iq_coef + parent2.iq_coef)/2
  
  
# esther = Parent(name="esther", surname="lopez", height=180.0, weight=60.0, iq_coef= 120.0)
# juanchi = Parent(name="juanchi", surname="abad", height=160.0, weight=80.0, iq_coef= 120.0)

# guille = Child(name="guille", parent1=juanchi, parent2= esther)
