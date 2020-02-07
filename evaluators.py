from tree_structures import Node, EqualBranch, LessEqualBranch, GreaterBranch
from math import log, inf
from config import reduce_split_points, split_points_threshold


class AttributeEvaluator:
    def __init__(self, examples, attribute, goal):
        self.examples = examples
        self.attribute = attribute
        self.goal = goal
        self.examples_count = len(examples)

    def get_evaluated_node(self):
        pass

    @staticmethod
    def get_entropy(probability):
        if probability == 0 or probability == 1:
            return 0
        else:
            return -(probability * log(probability, 2) + (1 - probability) * log((1 - probability), 2))


class DiscreteAttributeEvaluator(AttributeEvaluator):
    def get_evaluated_node(self):
        def get_remainder():
            remainder = 0
            for value in self.attribute.values:
                current_value_examples = [example for example in self.examples if
                                          example[self.attribute.index] == value]
                current_value_examples_count = len(current_value_examples)
                if not current_value_examples_count:
                    continue
                current_value_positive_examples_count = len([example for example in current_value_examples if
                                                             example[self.goal.index] == self.goal.value])

                weight = current_value_examples_count / self.examples_count
                entropy = self.get_entropy(current_value_positive_examples_count / current_value_examples_count)

                remainder += weight * entropy
            return remainder

            # positive_examples_count = len(
            #     [example for example in self.examples if example[self.goal.index] == self.goal.value])
            # goal_entropy = self.get_entropy(positive_examples_count / self.examples_count)
            # attribute_remainder = get_remainder()
            # return goal_entropy - attribute_remainder

        branches = [EqualBranch(value) for value in self.attribute.values]
        node = Node(self.attribute, branches)
        remainder = get_remainder()
        return node, remainder


class NumericAttributeEvaluator(AttributeEvaluator):
    def get_evaluated_node(self):
        def get_best_split_point_and_remainder():
            def get_split_point_candidates():
                sorted_examples = sorted(self.examples, key=lambda x: x[self.attribute.index])
                split_point_candidates = []
                for i in range(self.examples_count - 1):
                    if sorted_examples[i][self.attribute.index] == sorted_examples[i + 1][self.attribute.index]:
                        continue
                    if sorted_examples[i][self.goal.index] != sorted_examples[i + 1][self.goal.index]:
                        split_point_candidates.append((sorted_examples[i + 1][self.attribute.index] + sorted_examples[i][self.attribute.index]) / 2)
                split_point_candidates = sorted(list(set(split_point_candidates)))

                def reduce_split_point_candidates(split_points, threshold):
                    split_points_count = len(split_points)
                    if split_points_count <= threshold:
                        return split_points
                    step = split_points_count // (threshold + 1)
                    reduced_split_points = []
                    index = 0
                    for index in range(step, split_points_count - step, step):
                        reduced_split_points.append(split_points[index])
                    return reduced_split_points

                if reduce_split_points:
                    return reduce_split_point_candidates(split_point_candidates, split_points_threshold)
                else:
                    return split_point_candidates

            split_point_candidates = get_split_point_candidates()
            if len(split_point_candidates) > 100:
                print("Evaluating %d split points, this may take a while..." % len(split_point_candidates))
            if not split_point_candidates:
                split_point_candidates = [self.examples[0][self.attribute.index]]

            best_split_point = None
            best_remainder = inf

            for split_point in split_point_candidates:
                left_subset = [example for example in self.examples if example[self.attribute.index] <= split_point]
                right_subset = [example for example in self.examples if example[self.attribute.index] > split_point]

                left_subset_count = len(left_subset)
                left_subset_positive_examples_count = len(
                    [example for example in left_subset if example[self.goal.index] == self.goal.value])

                right_subset_count = len(right_subset)
                right_subset_positive_examples_count = len(
                    [example for example in right_subset if example[self.goal.index] == self.goal.value])

                if left_subset_count != 0:
                    left_branch_remainder = ((left_subset_count / self.examples_count) * self.get_entropy(
                        left_subset_positive_examples_count / left_subset_count))
                else:
                    left_branch_remainder = 0

                if right_subset_count != 0:
                    right_branch_remainder = ((right_subset_count / self.examples_count) * self.get_entropy(
                        right_subset_positive_examples_count / right_subset_count))
                else:
                    right_branch_remainder = 0

                remainder = left_branch_remainder + right_branch_remainder

                if remainder < best_remainder:
                    best_split_point = split_point
                    best_remainder = remainder

            return best_split_point, best_remainder

        split_point, remainder = get_best_split_point_and_remainder()
        left_branch = LessEqualBranch(split_point)
        right_branch = GreaterBranch(split_point)
        branches = [left_branch, right_branch]
        node = Node(self.attribute, branches)
        return node, remainder
