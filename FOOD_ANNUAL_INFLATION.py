import pandas as pd
from matplotlib import pyplot as plt
import math as mt
import statsmodels.api as sm

### DATA FRAME 1; FOOD ANNUAL INFLATION (fcpi_a)
fcpi_a_i = pd.read_excel("inflation_data.xlsx", sheet_name="fcpi_a", index_col=2) #Food Core Price Index - Motnhly Inflation
sub_sample = ["India","Nepal", "Pakistan", "Sri Lanka","Bangladesh"] # Countries Sub-Sample (for which i have data)
fcpi_a_i = fcpi_a_i.loc[sub_sample] 
fcpi_a_i.drop(columns=["Country Code", "IMF Country Code", "Indicator Type","Series Name","Nothing","Note"], inplace=True) # Removing Columns

### FIG 1; INFLATION PLOT 
fig1, ax = plt.subplots(nrows=2, ncols=3, figsize=(10, 12))
ax = ax.flatten()

for i, country in enumerate(sub_sample):
    ax[i].plot(fcpi_a_i.columns, fcpi_a_i.loc[country, :])
    ax[i].set_title(f"{country}") 
fig1.suptitle('Average Annual Inflation in South Asia', fontsize=20, color="r")
plt.tight_layout()
plt.show()

### FIG 2; ACF 30 LAGS 
fig2, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 10), sharex=True, sharey=True)  # Adjust figsize as needed
axs = axs.flatten()
lags_n = 30
for i, country in enumerate(fcpi_a_i.index):
    sm.graphics.tsa.plot_acf(fcpi_a_i.loc[country], lags=lags_n, ax=axs[i])
    axs[i].set_title(country)
    axs[i].set_xlabel('Lags')
    axs[i].set_ylabel('Auto-correlation')

fig2.suptitle(f"Auto-Correlation function with {lags_n} LAGS", fontsize=20, color="r")
plt.tight_layout()
plt.show()

### DATA FRAME 3: FIRST ORDER ACF (acf)
window_size = 10 # 10 YEARS
acf = pd.DataFrame(index=fcpi_a_i.index, columns=fcpi_a_i.columns)
obs = len(fcpi_a_i.columns) - window_size + 1 

for country in sub_sample:
    for i in range(obs):
        window_data = fcpi_a_i.loc[country,:].iloc[i:i+window_size]
        acf_value = sm.tsa.acf(window_data,nlags=1)
        acf.loc[country,fcpi_a_i.columns[i+window_size-1]] = acf_value[1]  

### FIG 3 : FIRST ORDER ACF 
fig1, axx = plt.subplots(ncols=3, nrows=2, sharex=True, sharey=True)
axx=axx.flatten()

for i, country in enumerate(sub_sample):
    axx[i].plot(acf.columns, acf.loc[country])
    axx[i].set_title(country)
    axx[i].axhline(y=0, linestyle="-", color="black")

fig1.suptitle(f'First Order ACF with {window_size}Y Window Size', fontsize=20, color="r")
plt.tight_layout()
plt.show()