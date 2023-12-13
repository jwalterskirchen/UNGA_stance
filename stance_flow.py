import pandas as pd
import streamlit as st
import numpy as np
from d3blocks import D3Blocks
import streamlit.components.v1 as components
st.set_page_config(layout="wide")

st.title('Friend or Foe: Using Aspect-Based Sentiment Analysis to Measure Relations between Member States at the UN General Assembly')
#Loading the data
@st.cache_data
def get_data():
    df = pd.read_csv("df_stance.csv")
    df['year1'] = df['year'].astype('datetime64[ns]')
    df['year1'] = df['year1'].dt.year
    return df

df = get_data()

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')


csv = convert_df(df)
st.markdown(
    "**Authors: <a href='https://www.unibw.de/ciss-en/kompz-kfe/team/sonja-haffner-m-sc' style='text-decoration: none; color: black; font-weight: bold;'>Sonja Häffner</a> and <a href='https://jwalterskirchen.github.io/' style='text-decoration: none; color: black; font-weight: bold;'>Julian Walterskirchen</a>**",
    unsafe_allow_html=True)

st.markdown('''
**Abstract:**
As state preferences are not directly observable, conventional approaches to measuring countries’ foreign policy and security-related preferences often rely on secondary sources such as UN General Assembly voting patterns or joint military alliance memberships.
However, innovations in the field of Natural Language Processing (NLP) have opened opportunities to infer state preferences more directly from issued statements in written or verbal form.
In this paper, we combine two innovations, namely aspect-based sentiment analysis (also referred to as stance detection) and transformer models, to analyze interstate rhetoric in the UN General Assembly General Debates from 1970 to 2014.
Studying issued statements towards other countries, especially how positively or negatively they refer to each other, allows us to generate a comprehensive and dynamic measurement of interstate rhetoric.
We assess the validity of our approach by comparing it to other conventional measures of interstate relations and by aligning it with actual cooperative and conflictual behavior in a time-series cross-sectional framework.
We find that interstate rhetoric seems to better explain cooperative and conflictual behavior than most conventional approaches.
These results are promising and while we do not try to replace existing approaches it offers an additional lens through which to enhance our understanding of relations between countries.

**What is this about?**
This app serves as a companion to the above described paper and it allows users to explore which countries talk negatively about other countries in the UN General Assembly General Debate.
Interested users can also download the raw data via the provided download link.


> 	:rotating_light: **_NOTE:_**  Setting the minimum number of references to an invalid number may cause an error. Try a different number!
'''
)

st.download_button(
    "Press to Download the raw data as .csv file",
    csv,
    "UNGA_stances.csv",
    "text/csv",
    key='UNGA_stances'
)

st.markdown('#### Directed Negative Stance')
#df['year1'] = df['year'].astype('datetime64[ns]')
#df['year1']=df['year1'].dt.year
with st.container():
    year_range = st.sidebar.slider('Select Time Horizon:', min_value=df['year1'].min(), max_value=df['year1'].max(), value=(df['year1'].min(), df['year1'].max()))
    diff = year_range[1]-year_range[0]
    filtered_df = df[(df['year1'] >= year_range[0]) & (df['year1'] <= year_range[1])]
    #print(diff)
    df_map = filtered_df

    #sankey = df_map.drop(['speaker_country','target_country'], axis=1)
    sum_df = df_map.groupby(['namesA','namesB']).agg({'neg_count': 'sum'})
    sum_df = sum_df.reset_index()
    sum_df.rename(columns={'namesA': 'source', 'namesB': 'target', 'neg_count':'weight'}, inplace=True)
    sum_df = sum_df.sort_values('weight', ascending=False).drop_duplicates(subset=['source', 'target'])
    sum_df.weight = sum_df.weight.astype(int)
    sum_df.weight = abs(sum_df.weight)

    makes = [1,3,5,10,15,20,25,30]
    makes_1 = list(range(1,30,5))
    #default_idx = makes_1.index(diff-10)
    #makes_1 = sum_df.weight.astype(int)
    #default_idx = np.around(sum_df[sum_df['weight'] >= 3]["weight"].mean(), decimals=0) + 5
    #make_choice = st.sidebar.selectbox('Select your minimum number of references:',
    #                                   options=sum_df['weight'].unique(), index=sum_df['weight'].unique().tolist().index(default_idx))
    make_choice = st.sidebar.selectbox('Select your minimum number of references:',
                                       makes,
                                       index=2)

    sum_df = sum_df[sum_df.weight >= make_choice]

    d3 = D3Blocks(chart='Chord', frame=True)
    d3.chord(sum_df, fontsize=14, figsize=(1200, 900), filepath='./chord_demo.html', showfig=False, save_button=True, title='Directed Negative Stance')

    # Read the content of the HTML file
    with open('./chord_demo.html', encoding="utf8") as file:
        chord_chart_html = file.read()
    st.components.v1.html(chord_chart_html, height=900, scrolling=False)

st.markdown('#### Directed Positive Stance')
with st.container():
    #sankey = df_map.drop(['speaker_country','target_country'], axis=1)
    sum_df = df_map.groupby(['namesA','namesB']).agg({'pos_count': 'sum'})
    sum_df = sum_df.reset_index()
    sum_df.rename(columns={'namesA': 'source', 'namesB': 'target', 'pos_count':'weight'}, inplace=True)
    sum_df = sum_df.sort_values('weight', ascending=False).drop_duplicates(subset=['source', 'target'])
    sum_df.weight = sum_df.weight.astype(int)
    sum_df.weight = abs(sum_df.weight)

   # makes = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70]
    #makes_1 = list(range(0,60))
    #default_idx = makes_1.index(diff-10)
    #make_choice = st.sidebar.selectbox('Select your minimum number of references:', makes_1, index=15)

    sum_df = sum_df[sum_df.weight >= make_choice]

    d3 = D3Blocks(chart='Chord', frame=True)
    d3.chord(sum_df, fontsize=14, figsize=(1200, 900), filepath='./chord_demo_pos.html', showfig=False, save_button=True, title='Directed Positive Stance')

    # Read the content of the HTML file
    with open('./chord_demo_pos.html', encoding="utf8") as file:
        chord_chart_html = file.read()
    st.components.v1.html(chord_chart_html, height=900, scrolling=False)

# Streamlit app
#st.title('Negative Stances')
