
# coding: utf-8

# In[246]:

class BaseClient:
    BASE_URL = None

    method = None
    http_method = None

    def get_params(self):
        pass

    def get_json(self):
        pass

    def get_headers(self):
        pass

    def generate_url(self, method):
        return '{0}{1}'.format(self.BASE_URL, method)

    def _get_data(self, method, http_method):
        response = None
        
        # todo выполнить запрос
        
        return self.response_handler(response)

    def response_handler(self, response):
        return response

    def execute(self):
        return self._get_data(
            self.method,
            http_method=self.http_method
        )


# In[268]:

import requests
import json
import time
from collections import Counter

class vk_api(BaseClient):
    user_id,params,username = None,'',None
    age=[]
    c=[]
    
    def __init__(self,username):
        self.BASE_URL='http://api.vk.com/method/'
        self.http_method='GET'
        self.username=username
    def get_data(self,method,params):
        self.method = method
        r=requests.get(self.generate_url(self.method),params)
        data = r.json()
        return data
    
    def get_param(self, **kwargs):
        for key in kwargs:
            self.params = self.params+"&"+key+"="+str(kwargs[key])
        return self.params
    
    def get_id(self):
        return self.get_data("users.get",self.get_param(uids=self.username,v='3.0'))["response"][0]['uid']
   
    def get_friends(self):
        friends = self.get_data("friends.get",self.get_param(user_id=self.get_id(),fields="bdate",v='3.0'))
        for friend in friends.get('response'):
            if friend.get("bdate"):
                date = friend["bdate"].split(".")
                if len(date)>2:
                    self.age.append(int((int(time.time())-int(time.mktime(time.strptime(friend["bdate"], '%d.%m.%Y'))))/31536000))
        self.age = dict(Counter(self.age))
        return self.age
    def print_sharp(self,count):
        sharp = '';
        for i in range(count):
            sharp = sharp + "#"
        return sharp
    def print_age(self):
        for i in sorted(self.age):
            print("Age {} : {}".format(i,self.print_sharp(self.age[i])))
            


# In[270]:

vk = vk_api('id96115625')
print(vk.get_id())
print(vk.get_friends())
vk.print_age()


# In[ ]:




# In[ ]:



