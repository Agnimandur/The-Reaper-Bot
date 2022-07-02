from mongoengine import *
import datetime

class Params(Document):
    cooldown = IntField(min_value=1,max_value=1000000,default=43200) #default values for "begin game" button
    target = IntField(min_value=5,max_value=10000000,default=1000000)
    guild = IntField(unique=True,required=True)
    role = IntField(required=True) #reaper-admin role
    night = BooleanField(default=True)
    timezone = IntField(min_value=-12,max_value=14,default=0) #utc offset

    def edit(self,**kwargs):
        def to_second(x):
            if x.isdigit(): return int(x)
            mul = {'s':1,'m':60,'h':3600,'d':86400}
            return mul[x[-1]]*int(x[:-1])
        if 'c' in kwargs:
            self.cooldown = to_second(kwargs['c'])
        if 'p' in kwargs:
            self.target = to_second(kwargs['p'])
        if 'n' in kwargs:
            self.night = 't' in kwargs['n'].lower()
        if 'tz' in kwargs:
            self.timezone = kwargs['tz']

    def __str__(self):
        return f"""__Default Begin Game Parameters:__
Cooldown: {datetime.timedelta(seconds=self.cooldown)}
Target: {self.target} points
__Server Info:__
Night Reaps Allowed? {self.night}
Server Timezone (UTC offset): {self.timezone}"""