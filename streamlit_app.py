import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode

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

cell_renderer =  JsCode("""
                        function(params) {return `<a href=${params.value} target="_blank">${params.value}</a>`}
                        """)

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
gb.configure_column("# id", header_name='Event ID')
gb.configure_column("science_case", header_name='Science Case')
gb.configure_column(
    "solar_mach_link",
    headerName="Solar-MACH",
    width=100,
    cellRenderer=JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = 'Open link';
            this.eGui.setAttribute('href', params.value);
            this.eGui.setAttribute('style', "text-decoration:none");
            this.eGui.setAttribute('target', "_blank");
          }
          getGui() {
            return this.eGui;
          }
        }
    """)
)

# gb.configure_column("date", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-dd')
# gb.configure_column("date", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-ddTHH:mm:ZZZ')

# gb.configure_pagination(enabled=True, paginationAutoPageSize=False,paginationPageSize=20)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gb.configure_side_bar()
# gb.configure_side_bar(filters_panel=True, columns_panel=True, defaultToolPanel='filters')  # TODO: not working?
# gb.configure_default_column(filter=True, groupable=True, value=True, enableRowGroup=True, aggFunc="sum")

gridOptions = gb.build()

grid = AgGrid(df, show_toolbar=True, height=700, gridOptions=gridOptions, updateMode=GridUpdateMode.VALUE_CHANGED, allow_unsafe_jscode=True)

# st.dataframe(df, height=700)
# st.markdown("See [this documentation](https://docs.streamlit.io/develop/concepts/design/dataframes#stdataframe-ui-features) for what can be done with the table above.")




