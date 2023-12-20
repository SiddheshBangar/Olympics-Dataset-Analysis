import matplotlib.pyplot as px
import pandas as pd
import plotly.express as plt
import plotly.figure_factory as ff
import seaborn as sns
import streamlit as st

import helper
import preprocess

df = pd.read_csv('./athlete_events.csv')
region_df = pd.read_csv('./noc_regions.csv')

df = preprocess.preprocess(df, region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image('./download.png')

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    select_year = st.sidebar.selectbox("Select year", years)
    select_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, select_year, select_country)

    if select_year == 'Overall' and select_country == 'Overall':
        st.title('Overall Tally')
    elif select_year != 'Overall' and select_country == 'Overall':
        st.title('Medal Tally in ' + str(select_year))
    elif select_year == 'Overall' and select_country != 'Overall':
        st.title(select_country + ' Overall Performance')
    elif select_year != 'Overall' and select_country != 'Overall':
        st.title(select_country + ' performance in ' + str(select_year) + ' Olympics')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    st.header('Participating Nations over the year')
    nations_over_time = helper.data_over_time(df, 'region')
    fig = plt.line(nations_over_time, x='region', y='count')
    st.plotly_chart(fig)

    st.header('Events over the year')
    events_over_time = helper.data_over_time(df, 'Event')
    fig = plt.line(events_over_time, x='Event', y='count')
    st.plotly_chart(fig)

    st.header('Athletes over the year')
    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = plt.line(athletes_over_time, x='Name', y='count')
    st.plotly_chart(fig)

    st.title('No. of Events over time (Every Sport)')
    fig, ax = px.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    select_sport = st.selectbox('Select a Sport', sport_list)

    x = helper.most_successful(df, select_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)

    fig = plt.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")

    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = px.subplots(figsize=(20, 20))

    if not pt.empty:
        ax = sns.heatmap(pt, annot=True)
    else:
        st.write("No data to display.")
    st.pyplot(fig)

    st.title("Top 15 Athletes of " + selected_country)
    top15_df = helper.most_successful_country_wise(df, selected_country)
    st.table(top15_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=400)

    st.title('Distribution of Age')
    st.plotly_chart(fig)

    st.title('Height vs Weight')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    select_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df, select_sport)
    fig, ax = px.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)
    st.pyplot(fig)

    st.title('Men vs Women participation over the years')
    final = helper.men_vs_women(df)
    fig = plt.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)
