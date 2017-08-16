print ("   matplotlib")
import matplotlib
matplotlib.use("Agg")
print ("   matplotlib.pyplot")
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

print ("   seaborn")
import seaborn as sns
sns.set_style('whitegrid')

import numpy as np
###%matplotlib inline

def linePlot(dataFrame, category, plotName, hue=None):

    facet = sns.FacetGrid(dataFrame, hue=hue,aspect=2)
    facet.map(sns.kdeplot,category,shade=True)
    facet.set(xlim=(0, ))
    if(hue): facet.add_legend()
    
    facet.savefig(plotName)
    facet.set(yscale="log")
    facet.savefig(plotName.replace(".","_logy."))
    
class PandaPlotter(object):
    
    def __init__(self, dataFrame, targetCategory):
        self.dataFrame      = dataFrame
        self.targetCategory = targetCategory

    def plotTarget(self):

        print (" plotTarget: Plotting", self.targetCategory)
        ## Line plot of overall distribution
        plotName="plots/target_"+self.targetCategory+".png"
        #linePlot(self.dataFrame, self.targetCategory, plotName)
        #print (" plotTarget: Printed to: ", plotName)

        fig, (ax1, ax2, ax3 ) = plt.subplots(3, 1)
        bins = np.linspace(0, 120, 120)
        LogMin, LogMax = np.log10(self.dataFrame[self.targetCategory].min()),np.log10(self.dataFrame[self.targetCategory].max())
        logBins = np.logspace(LogMin, LogMax,10)
        print (" plotTarget: Plot 1")
        sns.distplot(self.dataFrame[self.targetCategory],ax=ax1,bins=bins, kde=False)
        ax1.set(xlim=(0,120) )
        
        print (" plotTarget: Plot 2")
        sns.distplot(self.dataFrame[self.targetCategory],ax=ax2,bins=bins, kde=False)
        ax2.set(xlim=(0,120) )
        ax2.set_yscale('log')

        print (" plotTarget: Plot 3")
        sns.distplot(self.dataFrame[self.targetCategory],ax=ax3,bins=logBins, kde=False)
        ax3.set_yscale('log')
        ax3.set_xscale('log')


        
        fig.savefig(plotName)
        print (" output to", plotName)

        
                        
    def doPlotSmall(self, category, order=None):

        if category not in list(self.dataFrame): return

        print ("\n**********************")
        print (" doPlotSmall: Running!")
        print (" doPlotSmall: cat", category)
        print (" doPlotSmall: target", self.targetCategory)

        # only in self.dataFrame, fill the two missing values with the most occurred value, which is "S".
        #self.dataFrame[category] = self.dataFrame[category].fillna("S")

        # plot
        sns.factorplot(category,self.targetCategory, data=self.dataFrame,size=4,aspect=3)

        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        print ("order",order)
        sns.countplot(x=category, data=self.dataFrame, ax=ax1, order=order)
        ax1.set_yscale('log')
        
        ##sns.countplot(x=self.targetCategory, hue=category, data=self.dataFrame, order=[1,0], ax=axis2)

        # group by category and get the mean and std_dev of target
        group_cat= self.dataFrame[[category, self.targetCategory]].groupby([category],as_index=False).mean()
        ax2.set_ylim(bottom=0.5)
        group_cat_mean   =  group_cat.mean()
        #group_cat_stddev =  group_cat.std()
        #sns.barplot(x=category, y=self.targetCategory, data=group_cat,ax=ax2)
        sns.boxplot(x=category, y=self.targetCategory, data=self.dataFrame,ax=ax2, order=order)
        ax2.set(ylim=(0,40) )
        
        plotName="plots/output_"+category+".png"
        fig.savefig(plotName)
        print (" output to", plotName)
        return
        
        facet = sns.FacetGrid(self.dataFrame, hue=self.targetCategory, aspect=4)
        facet.map(sns.kdeplot,category,shade=True)
        facet.set(xlim=(0,120), yscale="log")
        facet.add_legend()
        plotName="plots/output_facet"+category+".png"
        fig.savefig(plotName)

    def doPlotLarge(self, category):

        if category not in list(self.dataFrame): return

        # Fare
        print (" \n**********************")
        print (" doPlotLarge")
        print (" Category of ", category)

        # only for test_df, since there is a missing category values
        try:
            self.dataFrame[category].fillna(self.dataFrame[category].median(), inplace=True)
        except:
            self.dataFrame[category].fillna(self.dataFrame[category].mode(), inplace=True)

        # convert from float to int
        self.dataFrame[category] = self.dataFrame[category].astype(int)

        facet = sns.FacetGrid(self.dataFrame, hue=self.targetCategory,aspect=4)
        facet.map(sns.kdeplot,category,shade= True)
        facet.set(xlim=(0, 120))
        facet.add_legend()

        plotName="plots/output"+category+".png"
        facet.savefig(plotName)
        print (" output to ", plotName)
