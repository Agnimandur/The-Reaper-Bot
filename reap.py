import random
from time import time
from mongoengine import *

class Reap(Document):
    cooldown = IntField(min_value=1,max_value=1000000,required=True)
    target = IntField(min_value=5,max_value=10000000,required=True)
    guild = IntField(unique=True,required=True)
    last = IntField(required=True)
    board = IntField(required=True) #message where the leaderboard is stored
    channel = IntField(required=True) #channel where the buttons are stored
    data = DictField() #map of users to (time,points)

    reapTimes = MapField(ListField(DecimalField())) #map of reapers to the list of TIMES of their reaps
    #reapMuls = MapField(ListField(IntField())) #map of reapers to the MULTIPLIERS of their reaps

    #return the multiplier if the reap was successful, 0 otherwise.
    #if someone won, returns "WIN"
    def reap(self,user):
        if self.nextreap(user)==0:
            m = self.multiplier()
            newTime = time()
            self.appendLog(user,newTime - self.last,m)
            points = round(self.get_data(user,'p') + (newTime - self.last) * m)
            self.last = newTime
            self.data[user] = (self.last,points)
            if points >= self.target: return "WIN"
            return m
        else:
            return 0

    def appendLog(self,user,t,m):
        user = str(user)
        if user not in self.reapTimes:
            self.reapTimes[user] = []
        self.reapTimes[user].append(t)

    #(average reap time, number of reaps)
    def reap_data(self,user):
        user = str(user)
        if user in self.reapTimes:
            N = len(self.reapTimes[user])
            return (round(sum(self.reapTimes[user])/N),N)

    #average multiplier is 2
    def multiplier(self):
        m = 1
        while random.randint(1,2)==1: m += 1
        return m

    def get_data(self, user, t):
        d = (0,0)
        if user in self.data: d = self.data[user]
        if t=='t':
            return d[0]
        elif t=='p':
            return d[1]
        else:
            raise Exception("t/p only")

    def nextreap(self,user):
        delta = round(time() - self.get_data(user,'t'))
        return max(0,self.cooldown - delta)

    def value(self):
        return round(time() - self.last)

    def leaderboard(self):
        vals = []
        for k,v in self.data.items():
            vals.append([v[1],k])
        vals.sort(reverse=True)
        return vals

    def removePlayer(self,user):
        if user in self.data:
            del self.data[user]
            del self.reapTimes[user]

    def __str__(self):
        return f"""Cooldown: {self.cooldown}
Target: {self.target}
Value of Current Reap: {round(time()-self.last)}
Scores: {str(self.data)}"""