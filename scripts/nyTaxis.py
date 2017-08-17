###### Imports
print (" ****** Importing stuff ****")
print (" Import plotUtils...")
import plotUtils
print (" Import learnUtils...")
from learnUtils import *

import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-v","--verbose", dest='verbose', action='store_true', default=True, help="Verbose mode")
parser.add_argument("--nRows",  dest='nRows', default=None, type=int, help="How many rows")
args = parser.parse_args()


def doDateTime(dt_raw,debug=False):
    ## e.g. 2016-03-14 17:32:30
    dt = datetime.strptime(dt_raw, '%Y-%m-%d %H:%M:%S')
    weekdays=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    timeHr=float(dt.time().strftime("%H"))+float(dt.time().strftime("%M"))/60
    weekday=weekdays[dt.weekday()]
    month=dt.month
    #print ("\ndoDateTime: timeHr decimal",timeHr, weekday, month)
    return [timeHr, weekday, month]

           
def main():

    ### Get data-bases
    print ("\n ***************************")
    print ("\n **** getting Data Bases ***")
    trainName="data/train.csv"
    testName="data/test.csv"
    
    train_df = getDataBase(trainName, args.verbose, nRows=args.nRows)
    pd.to_datetime(train_df['pickup_datetime'])
    
    if (args.verbose): print ("main: doing adjustment to minutes")
    train_df['trip_duration_mins'] = train_df.apply( lambda row: (row['trip_duration']*0.016666), axis=1)
    #if (args.verbose): print ("main: doing adjustment to passenger count")
    #train_df['passenger_count_laurie'] = train_df.apply( lambda row: (1 if (row['passenger_count']==0) else "5+" if row['passenger_count']>=5 else row['passenger_count'] ), axis=1)
    #if (args.verbose): print ("main: doing adjustment to dateTime")
    
    
    #train_df['initHour']  = train_df.apply( lambda row: int(doDateTime(row['pickup_datetime'])[0]), axis=1)
    #train_df['initTime']  = train_df.apply( lambda row: doDateTime(row['pickup_datetime'])[0], axis=1)
    #train_df['initDay']   = train_df.apply( lambda row: doDateTime(row['pickup_datetime'])[1], axis=1)
    #train_df['initMonth'] = train_df.apply( lambda row: doDateTime(row['pickup_datetime'])[2], axis=1)

   
    printDF(train_df)
    #test_df  = getDataBase(testName, args.verbose)
   
    print ("\n *************************** \n")


    print ("\n ***************************")
    print ("\n **** doing some plots ***")
    

    train_plotter=plotUtils.PandaPlotter(train_df,"trip_duration_mins")

    #train_plotter.plotTarget() 
    
    #plotCols=[["passenger_count_laurie",[1,2,3,4,'5+']],['initHour'], ['initDay'], ['initMonth'] ]
    #for col in plotCols:
    #    if (args.verbose): print (" main: doObjectPlot for ",col[0])
    #    try:    train_plotter.doObjectPlot(col[0],order=col[1])
    #    except: train_plotter.doObjectPlot(col[0])
              
    train_plotter.doHeatmapPlot("pickup_longitude","pickup_latitude")
    
if __name__ == "__main__":

    main()
    print (" \n*******  Done *********\n")
