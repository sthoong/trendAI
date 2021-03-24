#Present Client Similarities

import surprise
from collections import defaultdict
from surprise import PredictionImpossible
import numpy as np
import pandas as pd

class ClientSimilarities:
    def __init__(self, rawdata, low, high):
        #raw data is a pandas data frame
        self.rawdata = rawdata
        #scale of rating, this is determined based on your data
        self.scale_low = low
        self.scale_high = high
        #index of best algorithm, set -1 by default, valid values should be >=0
        self.algoIndex = -1
        self.rmse = []
        self.predictions = []
        
    def get_top_n(self, n=10):
        # First map the predictions to each user
        top_n = defaultdict(list)
        for uid,iid,true_r,est,_ in self.predictions[self.algoIndex]:
            top_n[uid].append((iid,est))
        
        # Then sort the predictions for each user and retrieve the k highest ones
        for uid,user_ratings in top_n.items():
            user_ratings.sort(key=lambda x: x[1], reverse=True)
            top_n[uid] = user_ratings[:n]

        return top_n
        
    def recommendItems(self, n, client):
        top_n = self.get_top_n(n)
        items = []
        # iterate the clients
        for uid,user_ratings in top_n.items():
            if (uid == client):
                items = [iid for (iid, _) in user_ratings]
        
        return items
        
    def similarClients(self, n, client):
        users = []
        innerid = self.cKNN.trainset.to_inner_uid(client)
        client_neighbors = self.cKNN.get_neighbors(innerid, k=n)
        for cl in client_neighbors:
            users.append([self.cKNN.trainset.to_raw_uid(cl),sim[innerid,cl]])
        
        return users
    
    # training function, we use four different models to train our data sets
    def trainModels(self):
        #when importing from a DF, need to specify the scale of the ratings in order to get best performance
        reader = surprise.Reader(rating_scale=(self.scale_low,self.scale_high))
        data = surprise.Dataset.load_from_df(self.rawdata,reader)
        
        trainset = data.build_full_trainset()
        testset = trainset.build_anti_testset()
        
        self.rmse = []
        self.predictions = []
               
        print ("=== Training with Collaborative KNN ===")
        sim_options = {'name': 'cosine', 'user_based': False } # compute similarities between items
        self.cKNN = surprise.KNNBasic(k=40, sim_options=sim_options)
        self.cKNN.fit(trainset)
        self.predictions.append(self.cKNN.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[0],verbose=True))
        minR = self.rmse[0]
        self.algoIndex = 0
        
        print ("=== Matrix Factorization ===")
        self.SVD = surprise.prediction_algorithms.matrix_factorization.SVD(n_factors=30, n_epochs=10, biased=True)
        self.SVD.fit(trainset)
        self.predictions.append(self.SVD.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[1],verbose=True))
        if (minR>self.rmse[1]):
            self.algoIndex = 1
            minR = self.rmse[1]
        
        print ("=== Co-clustering ===")
        self.Co = surprise.prediction_algorithms.co_clustering.CoClustering(n_cltr_u=4, n_cltr_i=4, n_epochs=25)
        self.Co.fit(trainset)
        self.predictions.append(self.Co.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[2],verbose=True))
        if (minR>self.rmse[2]):
            self.algoIndex = 2
            minR = self.rmse[2]
               
        print ("=== Slope One Collaborative Filtering ===")
        self.slope = surprise.prediction_algorithms.slope_one.SlopeOne()
        self.slope.fit(trainset)
        self.predictions.append(self.slope.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[3],verbose=True))
        if (minR>self.rmse[3]):
            self.algoIndex = 3
            
    def saveModels(self, prefix):
        file_name = os.path.expanduser('~/{}_cknn.model'.format(prefix))
        dump.dump(file_name, algo=self.cKNN)
        
        file_name = os.path.expanduser('~/{}_svd.model'.format(prefix))
        dump.dump(file_name, algo=self.SVD)
        
        file_name = os.path.expanduser('~/{}_co.model'.format(prefix))
        dump.dump(file_name, algo=self.Co)
        
        file_name = os.path.expanduser('~/{}_slope.model'.format(prefix))
        dump.dump(file_name, algo=self.slope)
        
    def loadModels(self, prefix):
        reader = surprise.Reader(rating_scale=(self.scale_low, self.scale_high))
        data = surprise.Dataset.load_from_df(self.rawdata,reader)
        
        trainset = data.build_full_trainset()
        testset = trainset.build_anti_testset()
        
        file_name = os.path.expanduser('~/{}_cknn.model'.format(prefix))
        _, self.cNN = dump.load(file_name)
        self.predictions.append(self.cKNN.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[0],verbose=True))
        minR = self.rmse[0]
        self.algoIndex = 0

        file_name = os.path.expanduser('~/{}_svd.model'.format(prefix))
        _, self.SVD = dump.load(file_name)
        self.predictions.append(self.SVD.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[0],verbose=True))
        if (minR>self.rmse[1]):
            minR = self.rmse[1]
            self.algoIndex = 1

        file_name = os.path.expanduser('~/{}_co.model'.format(prefix))
        _, self.Co = dump.load(file_name)
        self.predictions.append(self.Co.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[0],verbose=True))
        if (minR>self.rmse[2]):
            minR = self.rmse[2]
            self.algoIndex = 2

        file_name = os.path.expanduser('~/{}_slope.model'.format(prefix))
        _, self.slope = dump.load(file_name)
        self.predictions.append(self.slope.test(testset))
        self.rmse.append(surprise.accuracy.rmse(self.predictions[0],verbose=True))
        if (minR>self.rmse[3]):
            minR = self.rmse[3]
            self.algoIndex = 3
