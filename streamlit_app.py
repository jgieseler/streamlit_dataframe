import streamlit as st

st.set_page_config(
    page_title="SOLER Catalogues",
    page_icon="images/SOLER_Favicon-150x150.png",  # "☀️",  # 🔆
    layout="wide",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)
# st.logo("images/soler.png", size='large')

# for my_key in ["selected_columns_1", "selected_columns_2"]:
#     if my_key in st.session_state:
#         st.session_state[my_key] = st.session_state[my_key]

# st.sidebar.checkbox("Fit columns on grid load", value=True, key='fit_columns_on_grid_load')
# st.sidebar.checkbox("Expand columns to show content", value=True, key='fitCellContents')

available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material", "quartz",  "alpine"]
selected_theme = st.sidebar.selectbox("Theme", available_themes, key='selected_theme')

# st.sidebar.write(st.session_state)

pages = [st.Page("pages/home.py", title="Home"),
         st.Page("pages/catalogue_1.py", title="CME_catalog"),
         st.Page("pages/catalogue_2.py", title="Flare_catalog"),
        ]

pg = st.navigation(pages, position="top")
pg.run()


st.markdown(
    """
        <style>
                .stMainBlockContainer {
                    # padding-left: 0rem;
                    # padding-right: 0rem;
                    padding-top: 4rem;
                    padding-bottom: 0rem;
                }
                # .stAppHeader {
                #     background-color: rgba(255, 255, 255, 0.0);
                #     visibility: visible;
                # }
                # [data-testid = "stSidebarHeader"] {
                #     height: 2rem; /* 2rem keeps just enough space for the icon*/
                # }
        </style>
        """,
    unsafe_allow_html=True,
)