import streamlit as st
import requests
import random

st.set_page_config(layout="wide")
st.title('🏀 Bored API app')

# Initialize session state for button click
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if 'suggested_activities' not in st.session_state:
    st.session_state.suggested_activities = []
    
if 'index' not in st.session_state:
    st.session_state.index = 0

st.sidebar.header('Input')
selected_type = st.sidebar.selectbox(
    'Select an activity type', 
    ["education", "recreational", "social", "diy", "charity", "cooking", "relaxation", "music", "busywork"]
)

# Fetch new activity only when button has not been clicked
def fetch_activity():
    suggested_activities_url = f'https://bored-api.appbrewery.com/filter?type={selected_type}'
    response = requests.get(suggested_activities_url)
    if response.status_code == 200:
        suggested_activities = response.json()
        st.session_state.suggested_activities = suggested_activities
        st.session_state.index = random.randint(0, len(suggested_activities) - 1)
    else:
        st.error("Failed to fetch activities. Please try again later.")
        st.session_state.suggested_activities = []
        st.session_state.index = 0

# Fetch activity if not already fetched
if not st.session_state.button_clicked:
    fetch_activity()

st.write(
    st.session_state.index, 
    st.session_state.suggested_activities[st.session_state.index] if st.session_state.suggested_activities else 'No activities', 
    st.session_state.button_clicked
)

c1, c2 = st.columns(2)
with c1:
    with st.expander('About this app'):
        st.write('Are you bored? The **Bored API app** provides suggestions on activities that you can do when you are bored. This app is powered by the Bored API.')
with c2:
    with st.expander('JSON data'):
        st.write(st.session_state.suggested_activities)

st.header('Suggested activity')

if st.session_state.suggested_activities:
    activity = st.session_state.suggested_activities[st.session_state.index]

    if st.button("Let's do it!"):
        st.session_state.button_clicked = True
        st.success(activity['activity'])
        st.balloons()
    else:
        st.info(activity['activity'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label='Number of Participants', value=activity['participants'], delta='')
    with col2:
        st.metric(label='Type of Activity', value=activity['type'].capitalize(), delta='')
    with col3:
        st.metric(label='Price', value=activity['price'], delta='')
