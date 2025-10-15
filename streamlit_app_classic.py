import copy
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, StAggridTheme
from st_aggrid.shared import JsCode

st.set_page_config(
    page_title="SOLER Catalogues",
    page_icon="☀️",  # 🔆
    layout="wide",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)
st.title("SOLER Catalogues")

available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material", "quartz",  "alpine"]
selected_theme = st.sidebar.selectbox("Theme", available_themes)

fit_columns_on_grid_load = False

cell_renderer =  JsCode("""
                        function(params) {return `<a href=${params.value} target="_blank">${params.value}</a>`}
                        """)

# reference to onCellClicked handling functions here: https://ag-grid.com/javascript-data-grid/grid-events/#reference-selection-cellDoubleClicked
# This example function logs the params to the console and alerts which row/column was clicked.
onCellDoubleClickedHandler = JsCode(r"""
    function (params){
      console.log(params);
      let clickedColumn = params.column.colId;
      let clickedRowIndex = params.rowIndex;
      let clickedValue = params.node.data[clickedColumn];

      let msg = `You double clicked on row ${clickedRowIndex}, column ${clickedColumn}, value is ${clickedValue}`;

      alert(msg);

      params.node.setDataValue('doubleClicked', Date.now());       

    }
""")

# an example based on https://www.ag-grid.com/javascript-data-grid/component-cell-renderer/#simple-cell-renderer-example
jsfnc = """
class BtnCellRenderer {
    init(params) {
        this.params = params;
        this.eGui = document.createElement('div');
        this.eGui.innerHTML = `
         <span>
            <button id='click-button' 
                class='btn-simple' 
                style='color: ${this.params.color}; background-color: ${this.params.background_color}'>Click!</button>
         </span>
        `;
        this.eButton = this.eGui.querySelector('#click-button');
        this.btnClickedHandler = this.btnClickedHandler.bind(this);
        this.eButton.addEventListener('click', this.btnClickedHandler);
    }

    getGui() {
        return this.eGui;
    }

    refresh() {
        return true;
    }

    destroy() {
        if (this.eButton) {
            this.eGui.removeEventListener('click', this.btnClickedHandler);
        }
    }

    btnClickedHandler(event) {
            if(this.params.getValue() == 'clicked') {
                this.refreshTable('');
            } else {
                this.refreshTable('clicked');
            }
                console.log(this.params);
                console.log(this.params.getValue());
        }

    refreshTable(value) {
        this.params.setValue(value);
    }
};
"""
BtnCellRenderer = JsCode(jsfnc)


tab1, tab2, tab3 = st.tabs(["full_catalog_cme_merged_with_flares_and_weak_flares",
                            "full_catalog_with_stix_merged_with_cme",
                            "Catalogue 3"])

with tab1:
  df_cme = pd.read_csv('full_catalog_cme_merged_with_flares_and_weak_flares.csv', sep=',',
                      parse_dates=['event_time', 'Start time (1 AU)', 'Start time (Sun)'])

  # col1, col2, col3, col4, col5 = st.columns(5)
  # sc = {}
  # sc['BepiC'] = col1.checkbox("BepiColombo", value=True)
  # sc['L1'] = col2.checkbox("L1 (SOHO/Wind)", value=True)
  # sc['PSP'] = col3.checkbox("Parker Solar Probe", value=True)
  # sc['STA'] = col4.checkbox("STEREO A", value=True)
  # sc['SolO'] = col5.checkbox("Solar Orbiter", value=True)

  # for key, value in sc.items():
  #     if not value:
  #         df_cme.drop(df_cme.filter(like=f'{key}_',axis=1).columns.to_list(), axis=1, inplace=True)

  gb = GridOptionsBuilder.from_dataframe(df_cme)
  for key in df_cme.keys():
    gb.configure_column(key, tooltipField=str(key), headerTooltip=str(key))
  # gb.configure_column("flare_comments", header_name='Flare Comments', tooltipField='flare_comments', headerTooltip='Comments about flares', width=10)


  # gb.configure_column("event_time", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-dd')
  # gb.configure_column("event_time", type=["customDateTimeFormat"], custom_format_string='yyyy-MM-ddTHH:mm:ZZZ')

  # gb.configure_pagination(enabled=True, paginationAutoPageSize=False,paginationPageSize=20)
  gb.configure_side_bar()  # TODO: not working?
  # gb.configure_default_column(filter=True, groupable=True, value=True, enableRowGroup=True, aggFunc="sum")

  gridOptions = gb.build()
  # gridOptions['pagination'] = True
  # gridOptions['paginationPageSize'] = 20    
  gridOptions['sideBar'] = True  # TODO: not working?
  # gridOptions['defaultColDef'] = {"filter": True, "groupable": True, "value": True, "enableRowGroup": True, "aggFunc": "sum"}
  gridOptions['rowSelection'] = 'multiple'  # 'single'
  gridOptions["tooltipShowDelay"] = 500

  # custom_theme = (
  #     StAggridTheme(base="quartz")
  #     .withParams(fontSize=20)
  #     .withParts("iconSetAlpine", "colorSchemeDark")
  # )


  grid1 = AgGrid(df_cme, show_toolbar=True, height=700, gridOptions=gridOptions, 
                  updateMode=GridUpdateMode.SELECTION_CHANGED,  # GridUpdateMode.VALUE_CHANGED,
                  allow_unsafe_jscode=True,
                  fit_columns_on_grid_load=fit_columns_on_grid_load,
                  theme=selected_theme,
                  key="table1",
                  )
  

with tab2:
  t_df = pd.read_csv('full_catalog_with_stix_merged_with_cme.csv', sep=',')
  time_columns = [col for col in t_df.columns if 'time' in col]
  df_stix = pd.read_csv('full_catalog_with_stix_merged_with_cme.csv', sep=',', parse_dates=time_columns)

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

  gridOptions = gb.build() 
  gridOptions['rowSelection'] = 'single'  # 'multiple'  # 'single'
  gridOptions["tooltipShowDelay"] = 500

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
                  fit_columns_on_grid_load=fit_columns_on_grid_load,
                  theme=selected_theme,
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
    pass
  else:
    st.write(grid2['selected_rows'])
    st.image(grid2['selected_rows']['IP Radio Bursts'].values[0])


with tab3:
  st.write("Tab 3 content")
