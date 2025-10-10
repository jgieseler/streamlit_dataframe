import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

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

df['date'] = pd.to_datetime(df["date"], format="%Y-%m-%d")

col1, col2, col3, col4, col5 = st.columns(5)
sc = {}
sc['BepiC'] = col1.checkbox("BepiColombo", value=True)
sc['L1'] = col2.checkbox("L1 (SOHO/Wind)", value=True)
sc['PSP'] = col3.checkbox("Parker Solar Probe", value=True)
sc['STA'] = col4.checkbox("STEREO A", value=True)
sc['SolO'] = col5.checkbox("Solar Orbiter", value=True)

for key, value in sc.items():
    if not value:
        df.drop(df.filter(like=f'{key}_',axis=1).columns.to_list(), axis=1, inplace=True)

gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_column("date", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz')
gb.configure_column("date", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-dd')
# gb.configure_column("date", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-ddTHH:mm:ZZZ')

gb = GridOptionsBuilder.from_dataframe(df)
gridOptions = gb.build()

AgGrid(df, show_toolbar=True, height=700, gridOptions=gridOptions)

# st.dataframe(df, height=700)
# st.markdown("See [this documentation](https://docs.streamlit.io/develop/concepts/design/dataframes#stdataframe-ui-features) for what can be done with the table above.")