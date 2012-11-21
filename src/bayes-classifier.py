import sys
import nltk
import random
import marshal

def document_features(document,word_features): 
    document_words = set(document) 
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def main():
    categories = ['ALL OTHER OFFENSES', 'ARSON', 'ASSAULT OFFENSES',
              'BREAKING AND ENTERING', 'BURGLARY', 'COUNTERFEITING',
              'DESTRUCTION OF PROPERTY', 'DISORDERLY CONDUC',
              'DRIVING UNDER THE INFLUENCE', 'DRUG', 'DRUNKENNESS',
              'EMBEZZLEMENT', 'HOMICIDE OFFENSES', 'KIDNAPPING',
              'LARCENY', 'LIQUOR LAW VIOLATIONS', 'MOTOR VEHICLE THEFT',
              'PEEPING TOM', 'PORNOGRAPHY', 'ROBBERY', 'RUNAWAY',
              'SEX OFFENSES', 'DISORDERLY CONDUCT']

    categoryId = {str(j+1):i for j,i in enumerate(categories)}
    
    infname=sys.argv[1]   #crime data. Use /data/processed/DC/train-test-data/all-dc-data
    outfname=sys.argv[2]  #file to save the classifier
    inf=open(infname,'r')
    crimes = list()
    
    print "Reading data from file"
    for line in inf:
        if len(line.strip()) < 10: continue  #line is too short to classify
        tokens = line.strip().split(',')
        #try:
        crimes.append(([w for w in tokens[0].split()], categoryId[tokens[1]]))
        #except:
        #    print line; sys.exit()
    random.shuffle(crimes)
    inf.close()
    del inf
    print "Done"

    crimewords = [w for c in crimes for w in c[0]]
    all_words = nltk.FreqDist(w.lower() for w in crimewords)
    word_features = all_words.keys()[:2000]
    del crimewords
    del all_words

    crimes = crimes[:10000]
    print "Getting features"
    featuresets = [(document_features(d,word_features), c) for (d,c) in crimes]
    print "Done. Total data points available:", len(featuresets)
    del crimes
    
    print "Training classifier"
    seventyPercentIndex = int(len(featuresets)*0.7)
    #train_set, test_set = featuresets[:seventyPercentIndex], featuresets[seventyPercentIndex:]
    classifier = nltk.NaiveBayesClassifier.train(featuresets)
    print "Done"
    del featuresets
    
    #print "Getting accuracy"
    #print nltk.classify.accuracy(classifier, test_set)
    #print "Done"

    print "Saving classifier"
    outf = open(outfname, 'wb')
    marshal.dump(classifier, outf)
    outf.close()
    print "Done"
    
if __name__=="__main__": main()
