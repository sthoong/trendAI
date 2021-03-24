# Similarity Test Process

from ClientSimilarities import ClientSimilarities
import pandas as pd
import os
import csv

def decode(key):
    rt = 1
    if (key == 'BUY'):
        rt = 1
    elif (key == 'SELL'):
        rt = -1
    elif (key == 'SELLSHORT'):
        rt = -1.5
    return rt

def traingData():
    #Load data from readership
    raw = pd.read_csv('../data/readershipdata.csv')
    raw.drop_duplicates(inplace=True)
    raw = raw.query('Week=="Week 3, 2021" and Language=="ja" and IndustryGroup!="Unknown" and Client!="Unmapped"')
    raw = raw.dropna()
    readerData = raw.copy(True)

    raw = raw[['Client','Ticker','Views']]
    raw.columns = ['n_clients', 'n_ticker', 'views']

    cs1 = ClientSimilarities(raw, 1, 130)
    cs1.trainModels()
    cs1.saveModels('reader')

    #Load OES data
    raw = pd.read_csv('../data/oesdata_v2.csv')
    raw.drop_duplicates(inplace=True)
    raw = raw.query('Week=="Week 4, 2021" and Client!="Unmapped"')
    oesData = raw.copy(True)
    raw['Side_c'] = raw[Side].appy(lambda x: decode(x))
    raw['VectorTurnover'] = raw['Norm_Turnover']*raw['Side_c']*1000000

    raw = raw[['Client', 'Ticker', 'VectTurnover']]
    raw.colums = ['n_clients', 'n_ticker', 'VectTurnover']

    cs2 = ClientSimilarities(raw, -3000, 1000)
    cs2.trainModels()
    cs2.saveModels('OES')

    return [cs1,cs2,readerData,oesData]

clients = ['RM259588', 'RM257375', 'RM258888', 'RM256668', 'RM257275',
           'RM278413', 'RM408316', 'RM685155', 'RM492200', 'RM492642']

[cs1,cs2,readerData,oseData] = trainingData()

for client in clients:
    try:
        print ('Process client:{}'.format(client))
        items1 = cs1.recommendItems(50, client)
        items2 = cs2.recommendItems(250, client)
        # find same items , top 10
        with open('../data/{}_RecommendedItems.csv'.format(client), 'w', newline='')
            fieldnames = ['ClientName', 'Sector', 'Ticker', 'Title', 'Rating', 'TP']
            writer = csv.DictWrite(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            count = 0
            eTicker = ''
            # compare sectors
            for item1 in items1:
                for item2 in items2:
                    if (count>=10):
                        break
                    #Fetch data which had this stock readed
                    df1 = readData.query('Ticker=="{}"'.format(item1))
                    for idx1, row1 in df1.iterrows():
                        #Find matched ticker and matched industry group from OES
                        df2 = oesData.query('Ticker=="{} and IndustryGroup=="{}"'.format(item2,row1['IndustryGroup']))
                        #check if we find the match, write to file
                        for idx2, row2 in df2.iterrows():
                            if (eTicker != row1['Ticker']):
                                writer.writerow({'ClientName': client, 'Sector': row1['IndustryGroup'], 'Ticker': row1['Title'], 'Rating': row1['Rating'], 'TP', row1['TP']})
                                count+=1
                                eTicker = row1['Ticker']
                            break

        clients1 = cs1.similarClients(20,client)
        clients2 = cs2.similarClients(20,client)


            
