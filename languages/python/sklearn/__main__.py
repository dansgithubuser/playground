from sklearn import svm

import random

def make_sample(noise=1, dims=10):
    return [random.uniform(0, noise) for _ in range(dims)]

relevant = [make_sample(2) for i in range(100)]
irrelevant = [make_sample(1) for i in range(1000)]

classifier = svm.SVC()
classifier.fit(relevant + irrelevant, [1] * len(relevant) + [0] * len(irrelevant))

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
print('true positive', true_positive)
print('false negative', false_negative)
print('true negative', true_negative)
print('false positive', false_positive)
