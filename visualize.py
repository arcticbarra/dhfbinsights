import facebookInsights
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

facebookInsights.generateCSVs(token="EAACEdEose0cBAMtNaHxbfJZAThyn9BHZAR2DPMteT1fizJ5kFVdH62JyauQVqei1EaazfZCs9fQgvAzex26JXlaU075bB46ZBhZCX2vGfziYkcK8iFei563DFsrNOFl1Gt4ZAYcv8wJKNF1kfZCZBdSoYbKIEKPshBXzmNLiZC1TEjIUxZAm4tZBx3jJKtqSM4QUfYZD",since ='February 1 2017',until = 'February 29 2017')

# onlineFansaveragedf = pd.read_csv('Datasets/pageFansOnline.csv',index_col=0)
# positiveFeedbackdf = pd.read_csv('Datasets/positiveFeedback.csv',index_col=0)
# negativeFeedbackdf = pd.read_csv('Datasets/negativeFeedback.csv',index_col=0)
# impressionsdf = pd.read_csv('Datasets/impressions.csv',index_col=0)
# pageConsumptionsdf = pd.read_csv('Datasets/pageConsumptions.csv',index_col=0)
# reactionsdf = pd.read_csv('Datasets/reactions.csv',index_col=0)
# fansByCountrydf = pd.read_csv('Datasets/fansByCountry.csv',index_col=0)
# pageLikesBySourcedf = pd.read_csv('Datasets/pageLikesBySource.csv',index_col=0)
# pageUnlikesBySourcedf = pd.read_csv('Datasets/pageUnlikesBySource.csv',index_col=0)
# averageFansDemographicsdf = pd.read_csv('Datasets/averageFansDemographics.csv',index_col=0)
