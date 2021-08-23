#%%
from multiprocessing import Pool
from datetime import datetime
import time
from random import random


def f(k):
    time.sleep(4)
    print(k * k)
    return k * k


if __name__ == "__main__":
    start = datetime.now()
    #%%
    p = Pool(5)
    for i in [[1, 2, 3, 4, 5]]:
        p.map_async(f, i)

    #%%
    p.close()
    #%%
    p.join()
    print(dir(p))
    # with Pool(5) as p:
    #     print(p.map(f, [1, 2, 3,4,5]))
    print(datetime.now() - start)

# %%
#%%
import pandas as pd

#%%
df = [["20120102", "20200119"]]
df = pd.DataFrame(df).T
#%%
df[0]=pd.to_datetime(df[0])
# %%
df.head()
# %%
df[0].dt.strftime('%Y%m%d')
# %%
