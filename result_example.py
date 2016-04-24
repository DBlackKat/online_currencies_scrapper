import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

if __name__== '__main__': # this need to be later converted i a function
    file = open("1998-2005.p",'rb')
    data = pd.read_pickle("1998-2005.p")
    df = pd.DataFrame(data,columns=['index','date','rates'])
    df = df.set_index(df.date)
    sns.tsplot([df.rates], color="indianred")