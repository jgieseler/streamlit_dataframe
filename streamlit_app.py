import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

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

sc = {}
sc['BepiC'] = st.checkbox("BepiColombo", value=True)
sc['L1'] = st.checkbox("L1 (SOHO/Wind)", value=True)
sc['PSP'] = st.checkbox("Parker Solar Probe", value=True)
sc['STA'] = st.checkbox("STEREO A", value=True)
sc['SolO'] = st.checkbox("Solar Orbiter", value=True)

for key, value in sc.items():
    if not value:
        df.drop(df.filter(like=f'{key}_',axis=1).columns.to_list(), axis=1, inplace=True)

AgGrid(df)

# st.dataframe(df, height=700)
# st.markdown("See [this documentation](https://docs.streamlit.io/develop/concepts/design/dataframes#stdataframe-ui-features) for what can be done with the table above.")