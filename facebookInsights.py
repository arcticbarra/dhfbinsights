'''
Reactions: Like, love, wow, haha, sad, anger
Impressions: Organic, organic unique viral
Negative Feedback
Positive Feedback
Page Consumptions By Consumption Type
Likes by source
Unilkes by source
Page fans online (average)
'''

import facebookinsights as fi
import pandas as pd
import facebook

token = "EAACEdEose0cBACS3oxZBnnzW73ZBehdZBapEfBM66X6Fafp8UbdHGb8iZBmpRLAXkjWgoXhDaqkWEZCgkXZB2d7my7G0GD5ZAeZAmTHAtrVFYAYySUsoxOaFKygjZCxJlt4HBfEvcnKE6tYrkwZAFIeZBZAZBewNBkarae0azHQesxHPr9sMKFZA3wIeIZCHnov5XinMNAZD"

since = 'February 1 2017'
until = 'February 29 2017'

page = fi.authenticate(token=token)

graph = facebook.GraphAPI(access_token=token, version='2.7')

reactions = graph.get_object(id="tecdemonterrey/insights",metric='page_actions_post_reactions_like_total,page_actions_post_reactions_love_total,page_actions_post_reactions_wow_total,page_actions_post_reactions_haha_total,page_actions_post_reactions_sorry_total,page_actions_post_reactions_anger_total',until=until,since=since)

insights = page.insights.daily(['page_impressions_organic','page_impressions_organic_unique','page_impressions_viral','page_consumptions_by_consumption_type','page_negative_feedback_by_type','page_positive_feedback_by_type','page_fans_online','page_fans_by_unlike_source_unique','page_fans_by_like_source_unique']).range(months=1,since=since).get()

impressionsdf = pd.DataFrame(columns=["Page Impressions Organic", "Page Impressions Organic Unique", "Page Impressions Viral"])
negativeFeedbackdf = pd.DataFrame(columns=['hide_clicks','hide_all_clicks','report_spam_clicks','unlike_page_clicks','xbutton_clicks'])
positiveFeedbackdf = pd.DataFrame(columns=['like','link','comment','answer','claim','rsvp'])
pageFansOnlinedf = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22','23'])
pageConsumptionsdf = pd.DataFrame(columns=['other clicks','video play','photo view','link clicks'])
reactionsdf = pd.DataFrame(columns=['page_actions_post_reactions_like_total','page_actions_post_reactions_love_total','page_actions_post_reactions_wow_total','page_actions_post_reactions_haha_total','page_actions_post_reactions_sorry_total','page_actions_post_reactions_anger_total'])

dates = []

onlineFansaveragedf = pd.DataFrame(columns=["Average"])

for i,insight in enumerate(insights):
    dates.append(insight.end_time.strftime("%A %d, %B %Y"))

    impressionsdf.loc[i,"Page Impressions Organic"] = insight.page_impressions_organic
    impressionsdf.loc[i,"Page Impressions Organic Unique"] = insight.page_impressions_organic_unique
    impressionsdf.loc[i,"Page Impressions Viral"] = insight.page_impressions_viral

    for column in pageConsumptionsdf:
        pageConsumptionsdf.loc[i,column] = insight.page_consumptions_by_consumption_type[column]

    for column in negativeFeedbackdf:
        negativeFeedbackdf.loc[i,column] = insight.page_negative_feedback_by_type[column]

    for column in positiveFeedbackdf:
        positiveFeedbackdf.loc[i,column] = insight.page_positive_feedback_by_type[column]

    for column in pageFansOnlinedf:
        pageFansOnlinedf.loc[i,column] = insight.page_fans_online[column]

i=0
for column in pageFansOnlinedf:
    onlineFansaveragedf.loc[i] = pageFansOnlinedf[column].sum()//24
    i+=1

pageFansOnlinedf.index = dates
positiveFeedbackdf.index = dates
negativeFeedbackdf.index = dates
impressionsdf.index = dates
pageConsumptionsdf.index = dates

for reaction in reactions['data']:
    i = 0
    for day in reaction['values']:
        reactionsdf.loc[i,reaction['name']] = day['value']
        i+=1
reactionsdf.columns = ['Like','Love','Wow','Haha','Sorry','Anger']
reactionsdf.index = dates

print(onlineFansaveragedf)
