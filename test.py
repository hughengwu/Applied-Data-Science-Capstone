#%%
from matplotlib.colors import ListedColormap

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#%%
iris_df = pd.read_csv("iris.csv")
iris_df
#%%
x = iris_df["sepal.length"].values
y = iris_df["sepal.width"].values
#%%
fig = plt.figure()
ax = plt.axes()

# 创建一个ListedColormap实例
# 定义了[0, 1]区间的浮点数到颜色的映射规则
cmp = mpl.colors.ListedColormap(["r", "g", "b"])

# 创建一个BoundaryNorm实例
# BoundaryNorm是数据分组中数据归一化比较好的方法
# 定义了变量值到 [0, 1]区间的映射规则，即数据归一化
norm = mpl.colors.BoundaryNorm([0, 2, 6.4, 7], cmp.N)


# 绘制散点图，用x值着色，
# 使用norm对变量值进行归一化，
# 使用自定义的ListedColormap颜色映射实例
# norm将变量x的值归一化
# cmap将归一化的数据映射到颜色
plt.scatter(x, y, c=x, cmap=cmp, norm=norm, alpha=0.7)

plt.show()

# %%
