import sklearn
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix
import numpy as np
import re
import csv
import operator
from nltk.stem import WordNetLemmatizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC

def main():
    stop_words = set(stopwords.words('english'))
    description = []
    category = []
    lemmatiser = WordNetLemmatizer()
    filtered_sentence=[]
    with open('api_csv.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        line = 0
        for row in csvReader:
            description.append(row[0])

            description[line] = description[line].strip()
            description[line] = description[line].lower()
            description[line]=re.sub(r'[^\x00-\x7F]+',' ', description[line])
            description[line] = re.sub(r'\d+','',description[line])
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(description[line])
            f=[w for w in tokens if not w in stop_words]
            singles = [lemmatiser.lemmatize(plural) for plural in f]
            filtered_sentence.append(singles)

            category.append(lemmatiser.lemmatize(row[1].strip().lower()))
            line = line + 1

    sentences=""
    for line in filtered_sentence:
        sentences=sentences + (' '.join(line)) + "&"

    finalList=sentences.split("&")
    vectorizer = TfidfVectorizer(min_df=2,max_df=0.95,max_features=16000,encoding='latin-1')

    termMat = vectorizer.fit_transform(finalList)
    freq = np.ravel(termMat.sum(axis=0))
    vocab = [v[0] for v in sorted(vectorizer.vocabulary_.items(),key=operator.itemgetter(1))]
    fdist = dict(zip(vocab,freq))

    sortedDict = sorted(fdist.items(),key=operator.itemgetter(1))
    #print(sortedDict)

    print(termMat.shape,len(category))
    trainData,testData,trainCategory,testCategory = train_test_split(termMat[:11199],category,test_size=0.30)
    cat=list(set(category))

    #SVM
    #clf=OneVsRestClassifier(LinearSVC())
    clf=sklearn.svm.LinearSVC()
    actual = clf.fit(trainData,trainCategory)
    predicted = actual.predict(testData)
    print('Without Cross Validation : ')
    print('SVM accuracy :' ,accuracy_score(testCategory,predicted)*100)
    confusionMat = confusion_matrix(testCategory, predicted)
    print('Confusion Matrix for SVM : ')
    print(confusionMat)
    total_classified = np.ravel(confusionMat.sum(axis=1))
    for i in range(len(confusionMat)):
        print('for category : ',cat[i],' correct classified  : ',confusionMat[i][i],' incorrectly classified : ',total_classified[i]-confusionMat[i][i])

    print(confusionMat.shape,len(cat))
    print(classification_report(testCategory,predicted))

    # Random Forest
    clf = RandomForestClassifier(n_estimators=500)
    actual = clf.fit(trainData, trainCategory)
    predicted = actual.predict(testData)
    print('Random Forest accuracy :', accuracy_score(testCategory, predicted)*100)
    confusionMat = confusion_matrix(testCategory, predicted)
    print('Confusion Matrix for Random Forest : ')
    print(confusionMat)
    total_classified = np.ravel(confusionMat.sum(axis=1))
    for i in range(len(confusionMat)):
        print('for category : ', cat[i], ' correct classified  : ', confusionMat[i][i], ' incorrectly classified : ',
              total_classified[i] - confusionMat[i][i])
    print(confusionMat.shape, len(cat))
    print(classification_report(testCategory, predicted))
   

    #Multinomial NB
    clf=MultinomialNB()
    actual = clf.fit(trainData, trainCategory)
    predicted = actual.predict(testData)
    print('Multinomial NB accuracy :', accuracy_score(testCategory, predicted)*100)
    confusionMat = confusion_matrix(testCategory, predicted)
    print('Confusion Matrix for Multinomial NB : ')
    print(confusionMat)
    total_classified = np.ravel(confusionMat.sum(axis=1))
    for i in range(len(confusionMat)):
        print('for category : ', cat[i], ' correct classified  : ', confusionMat[i][i], ' incorrectly classified : ',
              total_classified[i] - confusionMat[i][i])
    print(confusionMat.shape, len(cat))
    print(classification_report(testCategory, predicted))

if __name__ == '__main__':
    main()