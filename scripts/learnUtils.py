###### Imports

### Pandas
print ("   Import pandas")
import pandas as pd
from pandas import Series,DataFrame

# numpy, matplotlib, seaborn
print ("   Import numpy")
import numpy as np

# machine learning
print ("   Import sciki-learn...")
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split


def getDataBase(df_name, verbose, nRows=None):

    if(verbose): print (" getDataBase: Looking for df ",df_name)
    df = pd.read_csv(df_name, nrows=nRows)
    if(verbose): print (" getDataBase: Sucessfully found it")
    if(verbose and nRows): print (" getDataBase: Got "+str(nRows)+" rows")
    return df


def printDF(dataF):

    print ("\n *** printDF ")
    print (" First five rows:")
    print (dataF.head())
    print (" Info:")
    dataF.info()
    print (" *** end of prinDF\n")


def prepTrainSet(dataFrame,toTrainFor,cuts=False):

    print ("\n*****************")
    print ("Prep training set")

    X_df = dataFame.copy()

    if cuts:
        for cut in cuts:
            if cut not in list(dataFrame): continue
            print ("   Drop",cut)
            X_df = X_df.drop(cut,axis=1)
    
    if toTrainFor in list(dataFrame): 
        X_df = X_df.drop(toTrainFor, axis=1)    
        Y_df = dataFrame[toTrainFor]
        return (X_df, Y_df)
    else:
        return X_df

    
def doML(X_train_raw, Y_train_raw, type):

    if type=="logreq":
        print ("Doing logistic regression")
        machineLearner = LogisticRegression()
        
    elif type=="randomForest":
        print ("Doing random forest")
        machineLearner = RandomForestClassifier(n_estimators=100)
        
    else:
        print("No machine learner option")
        return

    X_train, X_test, Y_train, Y_test = train_test_split(X_train_raw, Y_train_raw, test_size=0.4,random_state=3)
    
    machineLearner.fit(X_train, Y_train)
    machineLearner.score(X_train, Y_train)
    print (" doML: ", machineLearner.score(X_test, Y_test))
    

