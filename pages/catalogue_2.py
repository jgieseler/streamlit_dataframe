import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode #, StAggridTheme
from st_aggrid.shared import JsCode

st.title("full_catalog_with_stix_merged_with_cme")

t_df = pd.read_csv('catalogues/full_catalog_with_stix_merged_with_cme.csv', sep=',')
time_columns = [col for col in t_df.columns if 'time' in col]
df_stix = pd.read_csv('catalogues/full_catalog_with_stix_merged_with_cme.csv', sep=',', parse_dates=time_columns)

st.multiselect("Select columns to display (by default all are active).", options=df_stix.keys(), default=df_stix.keys(), key='selected_columns_2')
df_stix = df_stix[st.session_state.selected_columns_2]

gb = GridOptionsBuilder.from_dataframe(df_stix)
# gb.configure_column("# id", header_name='Event ID')
for key in df_stix.keys():
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

grid2 = AgGrid(df_stix, show_toolbar=True, height=500, gridOptions=gridOptions, 
                updateMode=GridUpdateMode.SELECTION_CHANGED,  # GridUpdateMode.VALUE_CHANGED,
                allow_unsafe_jscode=True,
                fit_columns_on_grid_load=st.session_state.fit_columns_on_grid_load,
                theme=st.session_state.selected_theme,
                key="table2",
                # update_on = ['selectionChanged'],
                )

# try:
#   crocs_link = grid2.data['IP Radio Bursts'][grid2.data.clicked == "clicked"]

#   st.write(crocs_link.values[0])
#   st.write(crocs_link.values[-1])
#   st.image(crocs_link.values[0])
# except AttributeError:
#   pass

if (type(grid2['selected_rows']).__name__ == "NoneType"):
  st.write('Select rows to see details and obtain radio spectrograms!')
else:
  st.write(grid2['selected_rows'])
  for crocs_link in grid2['selected_rows']['IP Radio Bursts'].values:
    st.image(crocs_link)
  # st.image(grid2['selected_rows']['IP Radio Bursts'].values[0])
  st.write('Plots obtained from https://parker.gsfc.nasa.gov/crocs.html')

