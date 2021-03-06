import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
"""
Predicting the exact behavior of asset classes is virtually impossible, however, we can examine the possible outcomes based on the historical behavior of asset classes to have a better sense of the range of outcomes and managing the risk. [Geometric Brownian Motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion) is the well-known model for the stochastic time-evolution of an asset price. I coded this interactive application of the GBM model with Python and its libraries. The code is available in my [Github](https://github.com/mehranlp/GBM) repository. This application helps to understand the importance of various factors on the GBM model, for instance, by changing the Volatility, the outcome will change drastically. The volatility and any other variable in this model can be dynamic and automatically imported to the model. 
There are countless books about Geometric Brownian Motion and it's a related process, but I dive into this concept more thoroughly with [Aspects of Brownian Motion by Mansuy, Roger, Yor, Marc](https://www.springer.com/gp/book/9783540223474) and I highly recommend it to anyone interested in stochastic modeling concept.
"""
@st.cache
def gbm(n_steps=10,
            n_scen=1000,
            mu=0.07,
            sigma=0.15,

             s_0=100.0,
             prices=True):
    dt = 1/12

    random_return = np.random.normal(loc=(1+mu)**dt, scale=(sigma*np.sqrt(dt)), size=(n_steps,n_scen))
    random_return[0] = 1
    random_price = s_0*pd.DataFrame(random_return).cumprod() if prices else rets_plus_1-1
    return random_price


n_steps= st.sidebar.slider(label='NUMBER OF STEPS IN MODEL',
                                min_value=10,max_value=200)

n_scen= st.sidebar.slider(label='HOW MANY SCENARIOS YOU WANT TO SIMULATE?',
                                                                min_value=10,max_value=200)

mu= st.sidebar.slider('DRIFT FACTOR',
                                                                0.01, 0.1, 0.05)

sigma=st.sidebar.slider('VOLATILITY OF PRICE CHANGE', 0.05,0.30,0.15)

m=gbm(n_steps,n_scen,mu,sigma)

fig=px.line(m,template='plotly_white', width=1200, height=650)


fig.update_layout(showlegend=False,
    title="GEOMETRIC BROWNIAN MOTION PRICE SIMULATION")
fig.update_traces(mode='lines+markers',hovertemplate=None)

fig.update_xaxes(visible=False)
st.plotly_chart(fig)

wealth=m.iloc[-1]
Max=round(wealth.max())
Min=round(wealth.min())
Median = round(wealth.mean())
Qu1 = round(np.percentile(wealth,25))
Qu3 = round(np.percentile(wealth,75))


st.write('AFTER SIMULATING',n_scen, 'DIFFERENT PATHS:')
st.write('THE MINIMUM FINAL VALUE OF SIMULATED SCENRIOS IS' ,Min)


st.write('THE FIRST QUANTILE OF SIMULATED PATHS IS VALUED AT ', Qu1)

st.write('THE AVERAGE FINAL VALUE OF SIMULATED PATHS IS ', Median)


st.write('THE LAST QUANTILE FINAL VALUE OF SIMULATED PATHS IS ', Qu3)


st.write('AND THE MAXIMUM FINAL VALUE OF SIMULATED SCENRIOS IS', Max)
