import pandas as pd
import streamlit as st
import country_converter as coco
from d3blocks import D3Blocks
import streamlit.components.v1 as components
st.set_page_config(layout="wide")

st.title('Directed Negative Stance ')
#Loading the data
@st.cache_data
def get_data():
    df = pd.read_csv(r"C:\Users\Sonja_Arbeit\PycharmProjects\pythonProject3\df_corr_lags.csv")
    df['year1'] = df['year'].astype('datetime64[ns]')
    df['year1'] = df['year1'].dt.year
    return df

df = get_data()
#df['year1'] = df['year'].astype('datetime64[ns]')
#df['year1']=df['year1'].dt.year
with st.container():
    year_range = st.sidebar.slider('Select Time Horizon:', min_value=df['year1'].min(), max_value=df['year1'].max(), value=(df['year1'].min(), df['year1'].max()))
    diff = year_range[1]-year_range[0]
    filtered_df = df[(df['year1'] >= year_range[0]) & (df['year1'] <= year_range[1])]
    #print(diff)
    df_map = filtered_df
    mapvars = ['gwcode1','gwcode2','Negative']
    df_map = df_map[mapvars]
    df_map['namesA'] = coco.CountryConverter().pandas_convert(series=df_map['gwcode1'], src='GWcode', to='name_short')
    df_map['namesB'] = coco.CountryConverter().pandas_convert(series=df_map['gwcode2'], src='GWcode', to='name_short')

    sankey = df_map.drop(['gwcode1','gwcode2'], axis=1)
    sum_df = sankey.groupby(['namesA','namesB']).agg({'Negative': 'sum'})
    sum_df = sum_df.reset_index()
    sum_df.rename(columns={'namesA': 'source', 'namesB': 'target', 'Negative':'weight'}, inplace=True)
    sum_df = sum_df.sort_values('weight', ascending=False).drop_duplicates(subset=['source', 'target'])
    sum_df.weight = sum_df.weight.astype(int)
    sum_df.weight = abs(sum_df.weight)

    makes = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70]
    makes_1 = list(range(0,60))
    default_idx = makes_1.index(diff+3)
    make_choice = st.sidebar.selectbox('Select your minimum number of references:', makes_1, index=default_idx)

    sum_df = sum_df[sum_df.weight >= make_choice]

    d3 = D3Blocks(chart='Chord', frame=True)
    d3.chord(sum_df, fontsize=14, figsize=(1000, 850), filepath='./chord_demo.html', showfig=False, save_button=False, )

    # Read the content of the HTML file
    with open('./chord_demo.html', encoding="utf8") as file:
        chord_chart_html = file.read()
    st.components.v1.html(chord_chart_html, height=900, scrolling=True)
# Streamlit app
#st.title('Negative Stances')


df_san = df
mapvars = ['gwcode1','gwcode2','Negative', 'Positive']
df_san = df_san[mapvars]
df_san['namesA'] = coco.CountryConverter().pandas_convert(series=df_san['gwcode1'], src='GWcode', to='name_short')
df_san['namesB'] = coco.CountryConverter().pandas_convert(series=df_san['gwcode2'], src='GWcode', to='name_short')

sankey = df_san.drop(['gwcode1','gwcode2'], axis=1)
sum_df = sankey.groupby(['namesA','namesB']).agg({'Negative': 'sum', 'Positive':'sum'})
sum_df = sum_df.reset_index()
country = sum_df['namesA'].unique()
country_choice = st.sidebar.selectbox('Select Country:', country)
sum_country = sum_df[sum_df['namesA']==country_choice]
sum_country = sum_country.reset_index()
sum_country= pd.melt(sum_country, id_vars='namesB', value_vars=['Positive', 'Negative'])
sum_country.rename(columns={'variable': 'source', 'namesB': 'target', 'value':'weight'}, inplace=True)
sum_country = sum_country.sort_values('weight', ascending=False).drop_duplicates(subset=['source', 'target'])
sum_country.weight = sum_country.weight.astype(int)
sum_country.weight = abs(sum_country.weight)

d3 = D3Blocks(chart='Sankey', frame=True)
d3.sankey(sum_country, filepath='./Sankey_demo.html', link={"linkColor": "source"}, showfig=False, save_button=False)

# Read the content of the HTML file
with open('./Sankey_demo.html', encoding="utf8") as file:
    chord_chart_html = file.read()

st.title('Positive and Negative Stance for Selected Country')
st.components.v1.html(chord_chart_html, height=900, scrolling=True)
