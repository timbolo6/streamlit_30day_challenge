import streamlit as st
import pandas as pd

# Import for API calls
import requests

# Import for navbar
from streamlit_option_menu import option_menu

# Import for dynamic tagging
from streamlit_tags import st_tags, st_tags_sidebar

# Imports for aggrid
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid.shared import JsCode
from st_aggrid import GridUpdateMode, DataReturnMode

# Import for loading interactive keyboard shortcuts into the app
from gui import keyboard_to_url
from gui import load_keyboard_class


st.set_page_config(layout='wide', page_title="Zero-Shot Text Classifier", page_icon="🤗")
st.image("logo.png", width=120)

st.title("Zero-Shot Text Classifier")

API_KEY = st.secrets["api_token"]

API_URL = (
        "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
    )

headers = {"Authorization": f"Bearer {API_KEY}"}

label_widget = st_tags(
        label="",
        text="Add labels - 3 max",
        value=["Positive", "Neutral", "Negative"],
        suggestions=[
            "Navigational",
            "Transactional",
            "Informational",
            "Positive",
            "Negative",
            "Neutral",
        ],
        maxtags=3,
    )

new_line = "\n"
nums = [
    "Bruv, this new trainers got me walking like I'm headlining London Fashion Week - feeling like a snack and a half",
    "Fam, that sandwich was so dry, even the desert would be like 'nah, you're good, mate'",
    "I love my gf"
]

sample = f"{new_line.join(map(str, nums))}"
MAX_LINES = 5
text = st.text_area(
            "Enter keyphrase to classify",
            sample,
            height=200,
            key="2",
            help="At least two keyphrases for the classifier to work, one per line, "
            + str(MAX_LINES)
            + " keyphrases max as part of the demo",
        )
lines = text.split("\n")  # A list of lines
linesList = []
for x in lines:
    linesList.append(x)
linesList = list(dict.fromkeys(linesList))  # Remove dupes
linesList = list(filter(None, linesList))  # Remove empty


if len(linesList) > MAX_LINES:


    st.info(
        f"🚨 Only the first "
        + str(MAX_LINES)
        + " keyprases will be reviewed. Unlock that limit by switching to 'Unlocked Mode'"
    )

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    # Unhash to check status codes from the API response
    # st.write(response.status_code)
    return response.json()
listToAppend = []
for row in linesList:
    api_answer = query(
                {
                    "inputs": row,
                    "parameters": {"candidate_labels": label_widget},
                    "options": {"wait_for_model": True},
                }
            )
    listToAppend.append(api_answer)

df = pd.DataFrame.from_dict(listToAppend)

gb = GridOptionsBuilder.from_dataframe(df)
# enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
gb.configure_default_column(
    enablePivot=True, enableValue=True, enableRowGroup=True
)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
gridOptions = gb.build()

response = AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    height=400,
    fit_columns_on_grid_load=False,
    configure_side_bar=True,
)
    

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

csv = convert_df(df)

st.caption("")

st.download_button(
    label="Download results as CSV",
    data=csv,
    file_name="results.csv",
    mime="text/csv",
)