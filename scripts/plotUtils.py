print ("   matplotlib")
import matplotlib
matplotlib.use("Agg")
print ("   matplotlib.pyplot")
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

print ("   seaborn")
import seaborn as sns
sns.set_style('whitegrid')

import pandas as pd
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
        self.df      = dataFrame
        self.target = targetCategory

    def plotTarget(self):

        print (" plotTarget: Plotting", self.target)
        ## Line plot of overall distribution
        plotName="plots/target_"+self.target+".pdf"
        #linePlot(self.df, self.target, plotName)
        #print (" plotTarget: Printed to: ", plotName)

        fig, (ax1, ax2, ax3 ) = plt.subplots(3, 1)
        bins = np.linspace(0, 120, 120)
        LogMin, LogMax = np.log10(self.df[self.target].min()),np.log10(self.df[self.target].max())
        logBins = np.logspace(LogMin, LogMax,10)
        print (" plotTarget: Plot 1")
        sns.distplot(self.df[self.target],ax=ax1,bins=bins, kde=False)
        ax1.set(xlim=(0,120) )
        
        print (" plotTarget: Plot 2")
        sns.distplot(self.df[self.target],ax=ax2,bins=bins, kde=False)
        ax2.set(xlim=(0,120) )
        ax2.set_yscale('log')

        print (" plotTarget: Plot 3")
        sns.distplot(self.df[self.target],ax=ax3,bins=logBins, kde=False)
        ax3.set_yscale('log')
        ax3.set_xscale('log')
        
        fig.savefig(plotName)
        print (" output to", plotName)

                        
    def doObjectPlot(self, category, order=None):

        if category not in list(self.df): return

        print ("\n**********************")
        print (" doObjectPlot: Running!")
        print (" doObjectPlot: cat", category)
        print (" doObjectPlot: target", self.target)

        # only in self.df, fill the two missing values with the most occurred value, which is "S".
        #self.df[category] = self.df[category].fillna("S")

        # plot
        sns.factorplot(category,self.target, data=self.df,size=4,aspect=3)

        fig, (ax1, ax2) = plt.subplots(2, sharex=True)

        print ("order",order)
        sns.countplot(x=category, data=self.df, ax=ax1, order=order)
        ax1.set_yscale('log')
        
        ##sns.countplot(x=self.target, hue=category, data=self.df, order=[1,0], ax=axis2)

        # group by category and get the mean and std_dev of target
        group_cat= self.df[[category, self.target]].groupby([category],as_index=False).mean()
        ax2.set_ylim(bottom=0.5)
        group_cat_mean   =  group_cat.mean()
        #group_cat_stddev =  group_cat.std()
        #sns.barplot(x=category, y=self.target, data=group_cat,ax=ax2)
        sns.boxplot(x=category, y=self.target, data=self.df,ax=ax2, order=order)
        ax2.set(ylim=(0,40) )
        
        plotName="plots/output_"+category+".pdf"
        fig.savefig(plotName)
        print (" output to", plotName)
        return
        
        facet = sns.FacetGrid(self.df, hue=self.target, aspect=4)
        facet.map(sns.kdeplot,category,shade=True)
        facet.set(xlim=(0,120), yscale="log")
        facet.add_legend()
        plotName="plots/output_facet"+category+".pdf"
        fig.savefig(plotName)

    def doHeatmapPlot(self, xCat, yCat):
        
        if xCat not in list(self.df): return
        if yCat not in list(self.df): return

        print ("\n**********************")
        print (" doHeatmapPlot: Running!")
        print (" doHeatmapPlot: xCat", xCat)
        print (" doHeatmapPlot: yCat", yCat)
        print (" doHeatmapPlot: target", self.target)
        
        
        #pivoted = self.df.pivot(index=yCat, columns=xCat, values=self.target)
        #sns.heatmap(pivoted,ax=ax1)

        sns.set_style("white")
      
        xBins   = np.linspace(-74.05,-73.9, 100)
        yBins   = np.linspace(40.65,  40.85, 100)
        #groups  = self.df.groupby([pd.cut(self.df[xCat], xBins),pd.cut(self.df[yCat], yBins)])[self.target].mean()

        self.df[xCat+"_bin"]=pd.cut(self.df[xCat], xBins)
        self.df[yCat+"_bin"]=pd.cut(self.df[yCat], yBins)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10), sharey=True)

        pivoted = self.df.pivot_table(index=yCat+"_bin", columns=xCat+"_bin", values=self.target, aggfunc=np.sum)
        sns_hm = sns.heatmap(pivoted, robust=True, xticklabels=10, yticklabels=10, ax=ax1)
        sns_hm.invert_yaxis()
        
        pivoted = self.df.pivot_table(index=yCat+"_bin", columns=xCat+"_bin", values=self.target, aggfunc=np.mean)
        sns.heatmap(pivoted, robust=True, xticklabels=10, yticklabels=10, ax=ax2)

        ax1.invert_yaxis()
        plotName="plots/output_heatmap_"+xCat+"_"+yCat+".pdf"
        fig.savefig(plotName)
        print (" doHeatmapPlot: Printed heat map to",plotName)

        sns.jointplot(x=xCat, y=yCat, data=self.df, kind="hex",xlim=(-74.05,-73.9),ylim=(40.65, 40.85));
        plotName="plots/output_jointplot_"+xCat+"_"+yCat+".pdf"
        plt.savefig(plotName)
        print (" doHeatmapPlot: Printed joint plot to",plotName)

        
