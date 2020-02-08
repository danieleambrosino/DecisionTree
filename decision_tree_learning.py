from tree_structures import *
from attributes import *
from evaluators import DiscreteAttributeEvaluator, NumericAttributeEvaluator
from statistics import mode, StatisticsError
from math import inf
from random import choice


class DecisionTreeLearner:
    def __init__(self, training_set, validation_set, test_set, goal):
        self.training_set = training_set
        self.validation_set = validation_set
        self.test_set = test_set
        self.goal = goal
        self.tree = None

    def build_tree(self):
        def get_most_frequent_value(examples):
            goal_values = [example[self.goal.index] for example in examples]
            try:
                most_frequent_value = mode(goal_values)
            except StatisticsError:
                most_frequent_value = choice(goal_values)
            return most_frequent_value

        def same_classification(examples):
            goal_values = [example[self.goal.index] for example in examples]
            initial_value = goal_values[0]
            for value in goal_values:
                if value != initial_value:
                    return False
            return True

        def get_best_node(examples, attributes):
            best_node = None
            best_remainder = inf
            for attribute in attributes:
                if type(attribute) is DiscreteAttribute:
                    evaluator = DiscreteAttributeEvaluator(examples, attribute, self.goal)
                elif type(attribute) is NumericAttribute:
                    evaluator = NumericAttributeEvaluator(examples, attribute, self.goal)
                else:
                    continue

                node, remainder = evaluator.get_evaluated_node()
                if remainder < best_remainder:
                    best_node = node
                    best_remainder = remainder
            return best_node

        def remove_attribute(attribute, attributes):
            attributes_as_list = list(attributes)
            attributes_as_list.remove(attribute)
            return tuple(attributes_as_list)

        def split_examples(examples, node):
            subsets = []
            if type(node.branches[0]) is EqualBranch:
                for value in node.attribute.values:
                    exs = [example for example in examples if example[node.attribute.index] == value]
                    subsets.append(exs)
            elif type(node.branches[0]) in (LessEqualBranch, GreaterBranch):
                left_subset = [example for example in examples if
                               example[node.attribute.index] <= node.branches[0].value]
                right_subset = [example for example in examples if
                                example[node.attribute.index] > node.branches[1].value]
                subsets.append(left_subset)
                subsets.append(right_subset)
            else:
                raise Exception("Invalid branch")
            return subsets

        def learn(examples, attributes, parent_examples=()):
            if len(examples) == 0:
                most_frequent_value = get_most_frequent_value(parent_examples)
                return Leaf(most_frequent_value)
            elif same_classification(examples):
                return Leaf(examples[0][self.goal.index])
            elif len(attributes) == 0 or (len(attributes) == 1 and type(attributes[0]) is GoalAttribute):
                most_frequent_value = get_most_frequent_value(examples)
                return Leaf(most_frequent_value)
            else:
                root = get_best_node(examples, attributes)
                shrinked_attributes = remove_attribute(root.attribute, attributes)
                splitted_examples = split_examples(examples, root)
                for branch, examples_subset in zip(root.branches, splitted_examples):
                    subtree = learn(examples_subset, shrinked_attributes, examples)
                    branch.next_node = subtree
                return root

        self.tree = learn(self.training_set.examples, self.training_set.attributes)

    def prune_tree(self):
        def convert_tree(node):
            if type(node) is Leaf:
                return [Rule(postcondition=node)]
            elif type(node) is Node:
                subtree_rules = []
                for branch in node.branches:
                    rules = convert_tree(branch.next_node)

                    if type(branch) is EqualBranch:
                        precondition = EqualPrecondition(node.attribute, branch.value)
                    elif type(branch) is LessEqualBranch:
                        precondition = LessEqualPrecondition(node.attribute, branch.value)
                    elif type(branch) is GreaterBranch:
                        precondition = GreaterPrecondition(node.attribute, branch.value)
                    else:
                        raise TypeError("Unknown branch type")

                    for rule in rules:
                        rule.add_precondition(precondition)
                        subtree_rules.append(rule)
                return subtree_rules

        def get_rule_accuracy(rule):
            suitable_examples = 0
            correct_classifications = 0
            for index, example in enumerate(self.validation_set.examples):
                suitable = True
                for precondition in rule.preconditions:
                    if not precondition.compare(example[precondition.attribute.index]):
                        suitable = False
                        break
                if not suitable:
                    continue
                else:
                    suitable_examples += 1
                    if rule.postcondition.value == example[self.goal.index]:
                        correct_classifications += 1
                    # del validation_examples[index]
            if not suitable_examples:
                return 0
            return correct_classifications / suitable_examples

        def evaluate_rule(rule, accuracy=None):
            accuracy = get_rule_accuracy(rule) if not accuracy else accuracy

            if len(rule.preconditions) == 1:
                return rule, accuracy

            best_rule = rule
            best_accuracy = accuracy
            for precondition in rule.preconditions:
                shrinked_rule = rule.get_new_rule_without_precondition(precondition)
                current_accuracy = get_rule_accuracy(shrinked_rule)
                if current_accuracy > best_accuracy:
                    best_accuracy = current_accuracy
                    best_rule = shrinked_rule

            if best_accuracy > accuracy:
                best_rule, best_accuracy = evaluate_rule(best_rule, best_accuracy)
            return best_rule, best_accuracy

        rules = convert_tree(self.tree)

        for index, rule in enumerate(rules):
            pruned_rule, accuracy = evaluate_rule(rule)
            rules[index] = [pruned_rule, accuracy]

        for index, (rule, accuracy) in enumerate(rules):
            if accuracy == 0:
                rules.pop(index)

        rules.sort(key=lambda x: x[1], reverse=True)
        self.tree = rules

    def get_accuracy(self):
        def evaluate_example_tree(node, example):
            if type(node) is Leaf:
                return node.value == example[self.goal.index]
            if type(node) is Node:
                for branch in node.branches:
                    if branch.compare(example[node.attribute.index]):
                        return evaluate_example_tree(branch.next_node, example)

        def tree_accuracy():
            total = 0
            correct = 0

            for example in self.test_set.examples:
                total += 1
                result = evaluate_example_tree(self.tree, example)
                if result:
                    correct += 1

            return correct / total

        def evaluate_example_rules(example):
            for (rule, accuracy) in self.tree:
                suitable = True
                for precondition in rule.preconditions:
                    if not precondition.compare(example[precondition.attribute.index]):
                        suitable = False
                        break
                if not suitable:
                    continue
                if example[self.goal.index] == rule.postcondition.value:
                    return True
            return False

        def rules_accuracy():
            total = 0
            correct = 0

            for example in self.test_set.examples:
                total += 1
                result = evaluate_example_rules(example)
                if result:
                    correct += 1

            return correct / total

        if type(self.tree) is Node or type(self.tree) is Leaf:
            return tree_accuracy()
        elif type(self.tree) is list:
            return rules_accuracy()
        else:
            raise TypeError("Unknown tree type")
