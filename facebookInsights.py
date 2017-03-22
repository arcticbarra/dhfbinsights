import facebookinsights as fi
import pandas as pd
import facebook
import seaborn

def generateCSVs(token, since, until):
    '''
    Reactions: Like, love, wow, haha, sad, anger
    Impressions: Organic, organic unique viral
    Negative Feedback
    Positive Feedback
    Page Consumptions By Consumption Type
    Page fans online (average)
    Demographics
        Page fans and page fans by age/gender (average)
        Page fans by country
        Page likes by source
        Page unlikes by source
    '''
    # Auth
    page = fi.authenticate(token=token)
    graph = facebook.GraphAPI(access_token=token, version='2.7')

    # Requests
    reactions = graph.get_object(id="tecdemonterrey/insights",metric='page_actions_post_reactions_like_total,page_actions_post_reactions_love_total,page_actions_post_reactions_wow_total,page_actions_post_reactions_haha_total,page_actions_post_reactions_sorry_total,page_actions_post_reactions_anger_total',until=until,since=since)
    insights = page.insights.daily(['page_impressions_organic','page_impressions_organic_unique','page_impressions_viral','page_consumptions_by_consumption_type','page_negative_feedback_by_type','page_positive_feedback_by_type','page_fans_online']).range(months=1,since=since).get()
    countryCodes = pd.read_html('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2')
    fansbyCountry = graph.get_object(id="tecdemonterrey/insights",metric='page_fans_country',until=until,since=since)
    unlikes = graph.get_object(id="tecdemonterrey/insights",metric='page_fans_by_unlike_source_unique',until=until,since=since)
    likes = graph.get_object(id="tecdemonterrey/insights",metric='page_fans_by_like_source_unique',until=until,since=since)
    fans = graph.get_object(id="tecdemonterrey/insights",metric='page_fans',until=until,since=since)
    fansByAge = graph.get_object(id="tecdemonterrey/insights",metric='page_fans_gender_age',until=until,since=since)

    # DataFrame creation
    impressionsdf = pd.DataFrame(columns=["Page Impressions Organic", "Page Impressions Organic Unique", "Page Impressions Viral"])
    negativeFeedbackdf = pd.DataFrame(columns=['hide_clicks','hide_all_clicks','report_spam_clicks','unlike_page_clicks','xbutton_clicks'])
    positiveFeedbackdf = pd.DataFrame(columns=['like','link','comment','answer','claim','rsvp'])
    pageFansOnlinedf = pd.DataFrame(columns=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22','23'])
    onlineFansaveragedf = pd.DataFrame(columns=["Average"])
    pageConsumptionsdf = pd.DataFrame(columns=['other clicks','video play','photo view','link clicks'])
    reactionsdf = pd.DataFrame()
    pageUnlikesBySourcedf = pd.DataFrame()
    pageLikesBySourcedf = pd.DataFrame()
    fansDemographicsdf = pd.DataFrame()
    fansbyAgedf = pd.DataFrame()

    # Data processing
    dates = []
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

    # Page fans online
    i=0
    for column in pageFansOnlinedf:
        onlineFansaveragedf.loc[i] = pageFansOnlinedf[column].sum()//24
        i+=1

    # Reactions
    for reaction in reactions['data']:
        i = 0
        for day in reaction['values']:
            reactionsdf.loc[i,reaction['name']] = day['value']
            i+=1
    reactionsdf.columns = ['Like','Love','Wow','Haha','Sorry','Anger']

    #Fans by country
    fansByCountrydf = pd.DataFrame(columns=countryCodes[2][0].ix[1:].tolist())
    for metric in fansbyCountry['data']:
        i = 0
        for day in metric['values']:
            for v,k in enumerate(day['value']):
                fansByCountrydf.loc[i,k] = day['value'][k]
            i+=1
    fansByCountrydf.columns = countryCodes[2][1].ix[1:].tolist()
    fansByCountrydf = fansByCountrydf.dropna(axis=1)

    # Unlikes
    for metric in unlikes['data']:
        i = 0
        for day in metric['values']:
            for v,k in enumerate(day['value']):
                pageUnlikesBySourcedf.loc[i,k] = day['value'][k]
            i+=1
    pageUnlikesBySourcedf = pageUnlikesBySourcedf.ix[:,0:2]

    # Likes
    for metric in likes['data']:
        i = 0
        for day in metric['values']:
            for v,k in enumerate(day['value']):
                pageLikesBySourcedf.loc[i,k] = day['value'][k]
            i+=1
    pageLikesBySourcedf =  pageLikesBySourcedf.fillna(0)

    # Fans
    for metric in fans['data']:
        i = 0
        for day in metric['values']:
            fansDemographicsdf.loc[i,metric['name']] = day['value']
            i+=1
    for metric in fansByAge['data']:
        i = 0
        for day in metric['values']:
            for v,k in enumerate(day['value']):
                fansbyAgedf.loc[i,k] = day['value'][k]
            i+=1
    fansDemographicsdf = fansDemographicsdf.join(fansbyAgedf)
    averageFansDemographicsdf = pd.DataFrame(columns=list(fansDemographicsdf))
    for column in fansDemographicsdf:
        averageFansDemographicsdf.loc[0,column] = fansDemographicsdf[column].sum()//len(dates)

    # Index as date
    dfarray = [pageFansOnlinedf,positiveFeedbackdf,negativeFeedbackdf,impressionsdf,pageConsumptionsdf,reactionsdf,fansByCountrydf,pageLikesBySourcedf,pageUnlikesBySourcedf,fansDemographicsdf]
    for df in dfarray:
        df.index = dates
    averageFansDemographicsdf.index = ['Average']

    onlineFansaveragedf.to_csv('Datasets/pageFansOnline.csv')
    positiveFeedbackdf.to_csv('Datasets/positiveFeedback.csv')
    negativeFeedbackdf.to_csv('Datasets/negativeFeedback.csv')
    impressionsdf.to_csv('Datasets/impressions.csv')
    pageConsumptionsdf.to_csv('Datasets/pageConsumptions.csv')
    reactionsdf.to_csv('Datasets/reactions.csv')
    fansByCountrydf.to_csv('Datasets/fansByCountry.csv')
    pageLikesBySourcedf.to_csv('Datasets/pageLikesBySource.csv')
    pageUnlikesBySourcedf.to_csv('Datasets/pageUnlikesBySource.csv')
    averageFansDemographicsdf.to_csv('Datasets/averageFansDemographics.csv')
    print("Datasets generated.")
