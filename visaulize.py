import facebookInsights
import pandas as pd

# facebookInsights.generateCSVs(token="EAACEdEose0cBABwfztoT4ZCOWjkFZAVsqvWga67cLNY4pEzLVK20iqRttEKva4WcQbEObUBIaskhXhVNGcuJ8BadT5KnfRvsIfuseUEZBHuZAvSDTfSKqj4WCbittBfjLpjETXzrbZCpMLLOKmomzP0QgR5P59QmNBhb8xbTVz0kDzJR4dZA9AyepdFk0TUToZD",since ='February 1 2017',until = 'February 29 2017')

onlineFansaveragedf = pd.read_csv('Datasets/pageFansOnline.csv',index_col=0)
positiveFeedbackdf = pd.read_csv('Datasets/positiveFeedback.csv',index_col=0)
negativeFeedbackdf = pd.read_csv('Datasets/negativeFeedback.csv',index_col=0)
impressionsdf = pd.read_csv('Datasets/impressions.csv',index_col=0)
pageConsumptionsdf = pd.read_csv('Datasets/pageConsumptions.csv',index_col=0)
reactionsdf = pd.read_csv('Datasets/reactions.csv',index_col=0)
fansByCountrydf = pd.read_csv('Datasets/fansByCountry.csv',index_col=0)
pageLikesBySourcedf = pd.read_csv('Datasets/pageLikesBySource.csv',index_col=0)
pageUnlikesBySourcedf = pd.read_csv('Datasets/pageUnlikesBySource.csv',index_col=0)
averageFansDemographicsdf = pd.read_csv('Datasets/averageFansDemographics.csv',index_col=0)

print(impressionsdf)
