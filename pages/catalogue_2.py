import pooch
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridOptionsBuilder, GridUpdateMode #, StAggridTheme
from st_aggrid.shared import JsCode
from time import sleep

fname = 'Flare_catalog'  # 'full_catalog_with_stix_merged_with_cme'

st.title(fname)

t_df = pd.read_csv(f'catalogues/{fname}.csv', sep=',')
time_columns = [col for col in t_df.columns if 'time' in col]


df_cat_2_org = pd.read_csv(f'catalogues/{fname}.csv', sep=',', parse_dates=time_columns)

def store_value(my_key):
    # Copy the value to the permanent key
    st.session_state[my_key] = st.session_state[f"_{my_key}"]

if 'selected_columns_2' in st.session_state:
  default_keys = st.session_state.selected_columns_2
else:
  default_keys = df_cat_2_org.keys()

st.multiselect("Select columns to display (by default all are active).", options=df_cat_2_org.keys(), default=default_keys, key='_selected_columns_2', on_change=store_value, args=["selected_columns_2"])
# st.multiselect("Select columns to display (by default all are active).", options=df_cat_2_org.keys(), default=default_keys, key='_selected_columns_2')

if 'selected_columns_2' in st.session_state:
  df_cat_2 = df_cat_2_org[st.session_state.selected_columns_2]
else:
  df_cat_2 = df_cat_2_org

gb = GridOptionsBuilder.from_dataframe(df_cat_2)
# gb.configure_column("# id", header_name='Event ID')
for key in df_cat_2.keys():
  gb.configure_column(key, tooltipField=str(key), headerTooltip=str(key))
# gb.configure_column("flare_comments", header_name='Flare Comments', tooltipField='flare_comments', headerTooltip='Comments about flares', width=10)

gb.configure_column(
    "IP Radio Bursts",
    headerName="IP Radio Bursts",
    # width=100,
    cellRenderer=JsCode("""
        class UrlCellRenderer {
          init(params) {
            this.eGui = document.createElement('a');
            this.eGui.innerText = params.value;
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

# gb.configure_grid_options(onCellDoubleClicked=onCellDoubleClickedHandler)
# gb.configure_grid_options(onCellClicked=onCellDoubleClickedHandler)

# Make NaT values invisible without removing them
cell_stylejscode = JsCode("""
    function(params) {
        console.log(params.value);
        if (params.value === 'NaT') {
            return {
                'color':'rgb(0, 0, 0, 0.0)',
                /// 'backgroundColor':'white'
            }
        }
};
""")
gb.configure_columns(column_names=time_columns, cellStyle = cell_stylejscode)


gridOptions = gb.build() 
gridOptions['rowSelection'] = 'multiple'  # 'multiple'  # 'single'
gridOptions["tooltipShowDelay"] = 500
gridOptions['autoSizeStrategy'] = 'fitCellContents'  # 'fitGridWidth'  # 'fitCellContents'

# Colour rows where STIX start time is NaT
# jscode2 = JsCode("""
# function(params) {
#     if (params.data.event_start_time_stix === 'NaT') {
#         return {
#             'color': 'green',
#             'backgroundColor': 'orange'
#         }
#     }
# };
# """)
# gridOptions['getRowStyle'] = jscode2





# gridOptions["columnDefs"].append(
#     {
#         "field": "clicked",
#         "headerName": "Clicked",
#         "cellRenderer": BtnCellRenderer,
#         "cellRendererParams": {
#             "color": "red",
#             "background_color": "black",
#         },
#     }
# )


grid2 = AgGrid(df_cat_2, show_toolbar=True, height=500, gridOptions=gridOptions, 
                updateMode=GridUpdateMode.SELECTION_CHANGED,  # GridUpdateMode.VALUE_CHANGED,
                allow_unsafe_jscode=True,
                # fit_columns_on_grid_load=False,  # st.session_state.fit_columns_on_grid_load,
                # columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                theme=st.session_state.selected_theme,
                key="table2",
                # update_on = ['selectionChanged'],
                )


# this is a workaround to avoid showing details from previous selection while new selection is being processed until https://github.com/streamlit/streamlit/issues/5044 is resolved.
details_container = st.empty()
details_container.empty()
sleep(0.01)


# try:
#   crocs_link = grid2.data['IP Radio Bursts'][grid2.data.clicked == "clicked"]

#   st.write(crocs_link.values[0])
#   st.write(crocs_link.values[-1])
#   st.image(crocs_link.values[0])
# except AttributeError:
#   pass


with details_container:
    with st.container(border=True):
      if (type(grid2['selected_rows']).__name__ == "NoneType"):
        st.write('Select rows to see details and obtain radio spectrograms!')
      else:
        st.write(grid2['selected_rows'])
        for crocs_link in grid2['selected_rows']['IP Radio Bursts'].values:
          with st.spinner("Downloading figure...", show_time=True):
            fig = pooch.retrieve(url=crocs_link, known_hash=None, progressbar=False)
            st.image(fig)
            # st.image(crocs_link)
        # st.image(grid2['selected_rows']['IP Radio Bursts'].values[0])
        st.write('Plots obtained from https://parker.gsfc.nasa.gov/crocs.html')
