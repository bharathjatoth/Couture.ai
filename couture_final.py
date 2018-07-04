import couture_data
import xlrd
import pandas as pd
import gensim
import math
from gensim.summarization import summarize
from gensim.summarization.keywords import keywords
import numpy as np
import string
from nltk.corpus import stopwords

#stop words
stopset = set(stopwords.words('english')) 
def xlsx():
    x1 = xlrd.open_workbook(r'C:\Users\jatoth.kumar\Desktop\couture.ai.xlsx')
    x = x1.sheet_by_index(0)
    skip_rows = 1
    x2 = []
    for i in range(skip_rows,x.nrows):
        # print(x.cell(i,0).value)
        x2.append(x.cell(i,0).value)
    return x2
#to get the test cases from the file
tc = xlsx()

remove_punct_dict = dict((ord(punct), ' ')  for punct in string.punctuation)
test_data = []
for t1 in tc:
    print(t1)
    t = t1.split()
    t = [w.lower().translate(remove_punct_dict) for w in t if w not in stopset]
    print(t)
    t = ' '.join(t)
    print(t)
    test_data.append(t)
oh1 = ['Flared','Metallic accents at the waist','Mid Rise','Front insert pockets','The model is wearing a size larger for a comfortable fit','Back welt pockets','Poly moss','Machine wash']
#repeat same for the product details
oh = []
for t1 in oh1:
    print(t1)
    t = t1.split()
    t = [w.lower().translate(remove_punct_dict) for w in t if w not in stopset]
    print(t)
    t = ' '.join(t)
    print(t)
    oh.append(t)
print(oh)
w2v_model = gensim.models.KeyedVectors.load('Gword2vec.model')
w2v_model.init_sims(replace=True)

class PhraseVector:
    def __init__(self, phrase):
        self.vector = self.PhraseToVec(phrase)
    def ConvertVectorSetToVecAverageBased(self, vectorSet):
        return np.mean(vectorSet, axis=0)
    def PhraseToVec(self, phrase):
        cachedStopWords = stopwords.words("english")
        phrase = phrase.lower()
        wordsInPhrase = [word for word in phrase.split() if word not in cachedStopWords]
        vectorSet = []
        for aWord in wordsInPhrase:
            try:
                wordVector = w2v_model[aWord]
                vectorSet.append(wordVector)
            except:
                pass
        return self.ConvertVectorSetToVecAverageBased(vectorSet)
    def CosineSimilarity(self, otherPhraseVec):
        cosine_similarity = np.dot(self.vector, otherPhraseVec) / (np.linalg.norm(self.vector) * np.linalg.norm(otherPhraseVec))
        try:
            if math.isnan(cosine_similarity):
                cosine_similarity = 0
        except:
            cosine_similarity = 0
        return cosine_similarity


THRESHOLD_SCORE = 0.4
if __name__ == "__main__":
    print(len(tc))
    print(len(oh))
    scoreMatrix = [[0 for x in range(len(oh))] for y in range(len(tc))]
    l_scoreMatrix = []
    scoreMatrix_zero = [[0 for x in range(len(oh))] for y in range(len(tc))]
    l_scoreMatrix_zero = []
    print(scoreMatrix)
    for idxh1, h1 in enumerate(tc):
        # print(scoreMatrix)
        print(h1)
        for idxt, t in enumerate(oh):
            print(idxt,t)
            phraseVectorO = PhraseVector(h1)
            phraseVectorT = PhraseVector(t)
            print(idxt)
            # print(phraseVectorO.shape)
            similarityScore = phraseVectorT.CosineSimilarity(phraseVectorO.vector)
            print("Similarity Score 2: ", similarityScore)
            scoreMatrix[idxh1][idxt] = similarityScore
            if similarityScore < THRESHOLD_SCORE:
                scoreMatrix_zero[idxh1][idxt] = 0.0
            else:
                scoreMatrix_zero[idxh1][idxt] = similarityScore
        l_scoreMatrix.append(scoreMatrix)
        l_scoreMatrix_zero.append(scoreMatrix_zero)
    
