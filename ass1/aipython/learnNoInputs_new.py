# learnNoInputs.py - Learning ignoring all input features
# AIFCA Python3 code Version 0.8.0 Documentation at http://aipython.org

# Artificial Intelligence: Foundations of Computational Agents
# http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import math, random
from learnProblem import squared_error, absolute_error, log_loss, mean

def evaluate(train_size, predictor, error_measure, num_samples=10000, test_size=10 ):
    """return the average error when
   train_size is the number of training examples
   predictor(training) -> [0,1]
   error_measure(prediction,actual) -> non-negative reals
   """
    error = 0
    for sample in range(num_samples):
        p = random.random()
        training = [1 if random.random()<p else 0 for i in range(train_size)]
        prediction = predictor(training)
        test = (1 if random.random()<p else 0 for i in range(test_size))
        error += sum( error_measure(prediction,actual) for actual in test)/test_size
    return error/num_samples


def predict_mean(data):
    "predict the mean"
    return mean(data)
def predict_bounded_mean(data):
    "predict the mean (bounded away from 0/1)"
    amean = mean(data)
    if amean == 1:
        return 0.99
    elif amean == 0:
        return 0.01
    else:
        return amean
def predict_laplace(data):
    "predict using Laplace smoothing; start with "
    return mean(data,1,2)
def predict_mode(data, sum=0, count=0):
    "predict the mode (binary only)"
    for e in data:
        count += 1
        sum += e
    return 1 if sum*2>count else 0


    
def test_no_inputs():
    for train_size in [1,2,3,4,5,10,20,100,1000]:
        print("For training size",train_size,":")
        for error_measure in [squared_error, absolute_error, log_loss]:
            print("  For",error_measure.__doc__)
            for predictor in [predict_mean, predict_laplace, predict_mode, predict_bounded_mean]:
                print("    For",predictor.__doc__,"error is",evaluate(train_size, predictor, error_measure))

if __name__ == "__main__":
    test_no_inputs()
        
