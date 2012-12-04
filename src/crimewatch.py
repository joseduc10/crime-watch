import nltk
import random 

def kFoldCrossValidation(samples, k, randomize=False):
  """
   Splits a given dataset into k parts.
   k rounds of training and testing are run. In each round,
   the kth bucket of data is used for testing and the other
   k-1 parts are used for training the classifier.
   The function returns the average of the accuracy of each of 
   the k rounds

   samples: the dataset. A list of tuples.
   k:       the number of splits
   randomize: if True, the dataset will be copied to a new list
              and shuffled before running the test

   Returns:
     The average accuracy after running k rounds of training and testing
  """
  if randomize: 
    samples = list()
    random.shuffle(samples)

  accuracies = []

  for i in range(k):
    training = [x for j,x in enumerate(x) if j%k != i]
    testing = [x for j,x in enumerate(x) if j%k == i]

    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    accuracies.append(nltk.classify.accuracy(classifier,testing))
    del classifier
  
  return float(sum(accuracies))/len(accuracies) 

class ConfusionMatrix:
  def __init__(labels): 
    self.labels = {(l,i) for i,l in enumerate(labels)}
    self.matrix = [[0 for i in self.labels] for j in self.labels]
    self.degree = len(self.labels)

  def increment(self,row,col):
    self.matrix[self.labels[row],self.labels[col]]

  def accuracy(self):
    num = sum([self.matrix[i][j] for i in range(self.degree) for j in range(self.degree) if i == j])
    den = sum([i for j in self.matrix for i in j])
    
    if den > 0: return float(num)/den
    else: return -1

  def precision(label):
    num = self.matrix[self.labels[label]][self.labels[label]]
    den = sum([a[i][self.labels[label]] for i in range(self.degree)])
    return float(num)/den

  def recall(label):
    num = self.matrix[self.labels[label]][self.labels[label]]
    den = sum([a[self.labels[label]][i] for i in range(self.degree)])
    return float(num)/den

