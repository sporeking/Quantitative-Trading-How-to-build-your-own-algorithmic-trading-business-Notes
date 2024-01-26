import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak

# 计算纯多头策略的夏普比率
# sharpe_ratio = np.sqrt(252) * return_mean / return_std (一年大约252个交易日)
# return_mean= 超额收益率的均值 = mean(策略收益率 - 基准收益率)
# return_std = 超额收益率的标准差 = std(策略收益率 - 基准收益率)

SSE_df = ak.stock_zh_index_daily_em(symbol='sh000001', start_date='20080512', end_date='20240125')
df_002230 = ak.stock_zh_a_hist(symbol="002230", period="daily", start_date='20080512', end_date='20240125', adjust="hfq")
# print(SSE_df.columns)
# Index(['date', 'open', 'close', 'high', 'low', 'volume', 'amount'], dtype='object')
# print(df_002230.columns)
# Index(['日期', '开盘', '收盘', '最高', '最低', '成交量', '成交额', ' 振幅', '涨跌幅', '涨跌额', '换手率'], dtype='object')
# 注：使用后复权数据

# 计算从2008年5月12日到2024年1月25日持有002230（科大讯飞）的夏普比率，以上证指数为基准
# df_002230['day_return'] = (df_002230['收盘'] - df_002230['前收盘价']) / (df_002230['前收盘价'])
df_002230['day_return'] = (df_002230['收盘'] - df_002230['收盘'].shift(1)) / (df_002230['收盘'].shift(1))
df_002230['cum_return'] = (df_002230['收盘'] - df_002230['收盘'][0]) / (df_002230['收盘'][0])
SSE_df['day_return'] = (SSE_df['close'] - SSE_df['close'].shift(1)) / (SSE_df['close'].shift(1))
SSE_df['cum_return'] = (SSE_df['close'] - SSE_df['close'][0]) / (SSE_df['close'][0])
return_mean = df_002230['day_return'][1:].mean()
return_std = df_002230['day_return'][1:].std()
SSE_return_mean = SSE_df['day_return'][1:].mean()
sharpe_ratio = np.sqrt(252) * (return_mean - SSE_return_mean) / return_std
print("sharpe_ratio: ", sharpe_ratio)

# 计算该策略的最大回撤和最大回撤持续时间
df_002230['cum_roll_max'] = df_002230['cum_return'].cummax() # 计算每一天的累计收益率的滚动最大值（此前的最大收益率）
df_002230['drawdown'] = (df_002230['cum_roll_max'] - df_002230['cum_return']) / (df_002230['cum_roll_max'] + 1) # 计算每一天的回撤
for index, row in df_002230.iterrows():
    if df_002230.loc[index, 'drawdown'] == 0:
        df_002230.loc[index, 'drawdown_duration'] = 0
    else:
        df_002230.loc[index, 'drawdown_duration'] = df_002230.loc[index-1, 'drawdown_duration'] + 1
    
max_drawdown = df_002230['drawdown'].max() # 最大回撤
max_drawdown_duration = df_002230['drawdown_duration'].max() # 最大回撤期
max_drawdown_duration_to = df_002230['drawdown_duration'][1:].idxmax(axis=0) # 最大回撤期对应的结束日期
max_drawdown_duration_from = max_drawdown_duration_to - max_drawdown_duration # 最大回撤期对应的开始日期   
print("max_drawdown: ", max_drawdown)
print("max_drawdown_duration: ", max_drawdown_duration, " from ", df_002230['日期'][max_drawdown_duration_from], " to ", df_002230['日期'][max_drawdown_duration_to])
plt.plot(df_002230['日期'], df_002230['收盘'])
plt.show()

