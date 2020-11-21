import pandas as pd
import numpy as np
from numpy import loadtxt

data = pd.read_csv(r'C:\Users\Hp\Desktop\ratings.csv',delimiter=',')
data = data[:99997]
#print(data['ISBN'][0])

data_new = np.zeros([8594,3])

c=0
for i in range(len(data)):
    if data['userID'][i]<5000:
        data_new[c,0] = data['ISBN'][i]
        data_new[c,1] = data['userID'][i]
        data_new[c,2] = data['bookRating'][i]
        c=c+1
#print(c)     
        
#np.savetxt('ratings(2).csv',data_new, delimiter=',')
        

    
data_new = pd.read_csv(r'C:\Users\Hp\Desktop\ratings(2).csv',delimiter=',')
#df = data_new['ISBN'].astype(str).str.cat(data_new['userID'].astype(str))

df = data_new[data_new.duplicated(subset=['ISBN','userID'])]
idx = df.index

data_new2 = np.zeros([8510,3])

c=0
for i in range(len(data_new)):
    if i in idx:
        wqe=0
    else:
        data_new2[c:c+1] = data_new[i:i+1]
        c=c+1
print(c) 
np.savetxt('ratings(3).csv',data_new2, delimiter=',')







