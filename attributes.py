class Attribute:
    def __init__(self, index, name):
        self.index = index
        self.name = name


class DiscreteAttribute(Attribute):
    def __init__(self, index, name, values):
        super().__init__(index, name)
        self.values = values


class NumericAttribute(Attribute):
    def __init__(self, index, name):
        super().__init__(index, name)


class GoalAttribute(DiscreteAttribute):
    def __init__(self, index, name, values, value):
        super().__init__(index, name, values)
        self.value = value
