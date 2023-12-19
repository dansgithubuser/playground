from sklearn import svm
from sklearn.inspection import permutation_importance

import random

def make_sample(noise=[1], dims=10):
    result = []
    for i in range(dims):
        if i >= len(noise):
            m = noise[-1]
        else:
            m = noise[i]
        result.append(random.uniform(0, m))
    return result

relevant = [make_sample([5, 1, 2]) for i in range(100)]
irrelevant = [make_sample([2, 2, 1]) for i in range(1000)]
features = relevant + irrelevant
labels = [1] * len(relevant) + [0] * len(irrelevant)

classifier = svm.SVC()
classifier.fit(features, labels)

true_positive = 0
false_negative = 0
true_negative = 0
false_positive = 0
for label in classifier.predict(relevant):
    if label == 1:
        true_positive += 1
    else:
        false_negative += 1
for label in classifier.predict(irrelevant):
    if label == 0:
        true_negative += 1
    else:
        false_positive += 1
print('RESULT QUALITY')
print('true positive', true_positive)
print('false negative', false_negative)
print('true negative', true_negative)
print('false positive', false_positive)
print()
print('FEATURE IMPORTANCE')
importance = permutation_importance(classifier, features, labels)
for i in reversed(importance.importances_mean.argsort()):
    print(f'{i} {importance.importances_mean[i]:.5f}')
