import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SERPENTINE Solar Cycle 25 SEP Events Catalog",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)

df = pd.read_csv('sep-sc25.csv', sep=';')

st.dataframe(df, height=700)

st.markdown("See [this documentation](https://docs.streamlit.io/develop/concepts/design/dataframes#stdataframe-ui-features) for what can be done with the table above.")