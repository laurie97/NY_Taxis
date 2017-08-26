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
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
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


def prepTrainSet(dataFrame,target,inVars):

    print ("\n*****************************")
    print (  "***** Prep training set *****")
    print (  "*****************************")
    
    X_df = dataFrame.copy()

    ### Check all the invars you asked for are there
    for inVar in inVars:
        if inVar not in list(dataFrame):
            print ("  ERROR learnUtils:prepTrainSet: variable",inVar,"does not exist")
            return
        
    ### If target
    if target in list(dataFrame): 
        X_df = X_df.drop(target, axis=1)    
        Y_df = dataFrame[target]
    else:
        Y_df = False

    print ("     What are the in Vars")
    for var in list(X_df):
        if var not in inVars:
            #print ("   learnUtils:prepTrainSet: - drop",var)
            X_df = X_df.drop(var,axis=1)
        else:
            print ("   learnUtils:prepTrainSet: + keep",var)   
    
    if target in list(dataFrame):  return (X_df, Y_df)
    else:     return  X_df


def prepTrainSetCuts(dataFrame,toTrainFor,cuts=False):

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

    
def doML(X_train, Y_train, type):

    if "mlp":
        machineLearner = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 1), random_state=1)
    
    else:
        print("No machine learner option")
        return

    ## Notation to emphasise that we are splitting up what is called train in the main code
    X_train_train, X_train_test, Y_train_train, Y_train_test = train_test_split(X_train, Y_train, test_size=0.4,random_state=3)
    
    machineLearner.fit(X_train_train, Y_train_train)
    machineLearner.score(X_train_train, Y_train_train)
    print (" doML: ", machineLearner.score(X_train_test, Y_train_test))
    

