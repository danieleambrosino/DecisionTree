class Node:
    def __init__(self, attribute, branches=None):
        self.attribute = attribute
        self.branches = [] if branches is None else branches

    def display(self, indent=0):
        name = self.attribute.name
        print('TEST', name)
        for branch in self.branches:
            if type(branch) is EqualBranch:
                binary_relation = '='
            elif type(branch) is LessEqualBranch:
                binary_relation = '<='
            elif type(branch) is GreaterBranch:
                binary_relation = '>'
            else:
                raise TypeError()

            print(' ' * 4 * indent, name, binary_relation, branch.value, '--->', end=' ')
            branch.next_node.display(indent + 1)


class Branch:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def compare(self, value):
        pass


class EqualBranch(Branch):
    def compare(self, value):
        return value == self.value


class LessEqualBranch(Branch):
    def compare(self, value):
        return value <= int(self.value)


class GreaterBranch(Branch):
    def compare(self, value):
        return value > int(self.value)


class Leaf:
    def __init__(self, value):
        self.value = value

    def display(self, indent=0):
        print('RESULT:', self.value)


class Precondition:
    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value

    def compare(self, value):
        pass


class EqualPrecondition(Precondition):
    def compare(self, value):
        return value == self.value


class LessEqualPrecondition(Precondition):
    def compare(self, value):
        return value <= int(self.value)


class GreaterPrecondition(Precondition):
    def compare(self, value):
        return value > int(self.value)


class Rule:
    def __init__(self, preconditions=None, postcondition=None):
        self.preconditions = [] if not preconditions else preconditions
        self.postcondition = postcondition

    def set_postcondition(self, postcondition):
        self.postcondition = postcondition

    def add_precondition(self, precondition):
        self.preconditions.insert(0, precondition)

    def get_new_rule_without_precondition(self, precondition):
        shrinked_preconditions = [precondition for precondition in self.preconditions]
        shrinked_preconditions.remove(precondition)
        return Rule(shrinked_preconditions, self.postcondition)
