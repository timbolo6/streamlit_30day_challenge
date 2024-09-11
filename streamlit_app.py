import streamlit as st
import requests
import random

st.title('🏀 Bored API app')

st.sidebar.header('Input')
selected_type = st.sidebar.selectbox('Select an activity type', ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"])

suggested_activity_url = f'https://bored-api.appbrewery.com/filter?type={selected_type}'
json_data = requests.get(suggested_activity_url)
suggested_activity = json_data.json()

c1, c2 = st.columns(2)
with c1:
  with st.expander('About this app'):
    st.write('Are you bored? The **Bored API app** provides suggestions on activities that you can do when you are bored. This app is powered by the Bored API.')
with c2:
  with st.expander('JSON data'):
    st.write(suggested_activity)

st.header('Suggested activity')

index = random.randint(0, len(suggested_activity) - 1)
activity = suggested_activity[index]

st.info(activity['activity'])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='Number of Participants', value=activity['participants'], delta='')
with col2:
    st.metric(label='Type of Activity', value=activity['type'].capitalize(), delta='')
with col3:
    st.metric(label='Price', value=activity['price'], delta='')