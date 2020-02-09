from dataset import DataSet
from decision_tree_learning import DecisionTreeLearner
from config import *
import matplotlib.pyplot as plt
from time import process_time
from statistics import mean

if reduce_split_points:
    print("[WARNING] Split point reduction is activated! The maximum threshold is set to", split_points_threshold)
    print("          You can turn off this option in config.py")

"""Import datasets"""

training_set = DataSet()
training_set.set_attributes(attributes)
print("Importing training set from", training_set_file_path)
training_set.import_csv_file(training_set_file_path)

validation_set = DataSet()
validation_set.set_attributes(attributes)
print("Importing validation set from", validation_set_file_path)
validation_set.import_csv_file(validation_set_file_path)

test_set = DataSet()
test_set.set_attributes(attributes)
print("Importing test set from", test_set_file_path)
test_set.import_csv_file(test_set_file_path)

"""Save results for plotting"""

x_axis = []
before_pruning_accuracies = []
after_pruning_accuracies = []
pruning_times = []

print("Test started!")

for training_set_size in range(8, 100):
    x_axis.append(training_set_size)
    before_pruning_accumulate = []
    after_pruning_accumulate = []
    pruning_times_accumulate = []
    for i in range(20):
        validation_set_size = training_set_size // 2
        test_set_size = (training_set_size // 4) * 3

        # print("[NOTICE] Training set size is set to", training_set_size)
        # print("[NOTICE] Validation set size is set to", validation_set_size)
        # print("[NOTICE] Test set size is set to", test_set_size)

        training_set.shuffle_examples(training_set_size)
        validation_set.shuffle_examples(validation_set_size)
        test_set.shuffle_examples(test_set_size)

        decision_tree_learner = DecisionTreeLearner(training_set, validation_set, test_set, goal)

        # print("Generating tree...")
        decision_tree_learner.build_tree()

        # print("Tree generated!")

        accuracy = decision_tree_learner.get_accuracy()
        # print("Before-pruning accuracy: %.2f%%" % (accuracy * 100))
        before_pruning_accumulate.append(accuracy)

        # print("Pruning tree... this may take a while...")
        start = process_time()
        decision_tree_learner.prune_tree()
        elapsed_time = process_time() - start
        # print("Elapsed time: %f seconds" % elapsed_time)
        pruning_times_accumulate.append(elapsed_time)

        accuracy = decision_tree_learner.get_accuracy()
        # print("After-pruning accuracy: %.2f%%" % (accuracy * 100))
        after_pruning_accumulate.append(accuracy)
    before_pruning_accuracies.append(mean(before_pruning_accumulate))
    after_pruning_accuracies.append(mean(after_pruning_accumulate))
    pruning_times.append(mean(pruning_times_accumulate))

plt.xlabel('Training set size')
plt.ylabel('Accuracy on test set')
plt.plot(x_axis, before_pruning_accuracies)
plt.plot(x_axis, after_pruning_accuracies)
plt.show()

# fig, (ax1, ax2) = plt.subplots(2)
# ax1.set(xlabel='Training dataset size', ylabel='Accuracy on test set')
# ax1.plot(x_axis, before_pruning_accuracies)
# ax1.plot(x_axis, after_pruning_accuracies)
# ax2.set(xlabel='Training dataset size', ylabel='Pruning time (seconds)')
# ax2.plot(x_axis, pruning_times)
# plt.show()
