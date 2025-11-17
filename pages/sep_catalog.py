import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode #, StAggridTheme
from st_aggrid.shared import JsCode
from time import sleep

fname = 'SOLER_SEP_catalog_PyOnset - WP2_multi_sc_event_list_draft'  # 'full_catalog_with_stix_merged_with_cme'

st.title(fname)

t_df = pd.read_csv(f'catalogues/{fname}.csv', sep=',')
datetime_columns = [col for col in t_df.columns if 'yyyy-mm-dd' in col]
date_columns = [col for col in t_df.columns if 'yyyy-mm-dd' in col]
time_columns = [col for col in t_df.columns if 'HH:MM:SS' in col]

df_cat_3_org = pd.read_csv(f'catalogues/{fname}.csv', sep=',', parse_dates=datetime_columns)


def store_value(my_key):
    # Copy the value to the permanent key
    st.session_state[my_key] = st.session_state[f"_{my_key}"]

if 'selected_columns_3' in st.session_state:
  default_keys = st.session_state.selected_columns_3
else:
  default_keys = df_cat_3_org.keys()

st.multiselect("Select columns to display (by default all are active).", options=df_cat_3_org.keys(), default=default_keys, key='_selected_columns_3', on_change=store_value, args=["selected_columns_3"])

if 'selected_columns_3' in st.session_state:
  df_cat_3 = df_cat_3_org[st.session_state.selected_columns_3]
else:
  df_cat_3 = df_cat_3_org

gb = GridOptionsBuilder.from_dataframe(df_cat_3)
for key in df_cat_3.keys():
  gb.configure_column(key, tooltipField=str(key), headerTooltip=str(key))
# gb.configure_column("flare_comments", header_name='Flare Comments', tooltipField='flare_comments', headerTooltip='Comments about flares', width=10)


# Make NaT values invisible without removing them
cell_style_NaT = JsCode("""
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
# gb.configure_columns(column_names=datetime_columns, cellStyle=cell_style_NaT)

gb.configure_columns(column_names=date_columns, cellDataType='date', type=["dateColumnFilter", "customDateTimeFormat"], custom_format_string='yyyy-MM-dd', cellStyle=cell_style_NaT)

for key in ["SEP_IDX", "Event No"]:
  gb.configure_column(key, spanRows='true')




gridOptions = gb.build() 
gridOptions['rowSelection'] = 'multiple'  # 'multiple'  # 'single'
gridOptions["tooltipShowDelay"] = 500
gridOptions['autoSizeStrategy'] = 'fitCellContents'  # 'fitGridWidth'  # 'fitCellContents'
gridOptions['enableCellSpan'] = 'true'



grid3 = AgGrid(df_cat_3, show_toolbar=True, height=500, gridOptions=gridOptions, 
                updateMode=GridUpdateMode.SELECTION_CHANGED,  # GridUpdateMode.VALUE_CHANGED,
                allow_unsafe_jscode=True,
                # fit_columns_on_grid_load=False,  # st.session_state.fit_columns_on_grid_load,
                # columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                theme=st.session_state.selected_theme,
                key="table3",
                # update_on = ['selectionChanged'],
                )


# this is a workaround to avoid showing details from previous selection while new selection is being processed until https://github.com/streamlit/streamlit/issues/5044 is resolved.
details_container = st.empty()
details_container.empty()
sleep(0.01)


if (type(grid3['selected_rows']).__name__ == "NoneType"):
  st.write('Select rows to see details!')
else:
  st.write(grid3['selected_rows'])