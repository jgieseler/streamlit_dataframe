import streamlit as st



st.set_page_config(
    page_title="SOLER Catalogues",
    page_icon="SOLER_Favicon-150x150.png",  # "☀️",  # 🔆
    layout="wide",
    initial_sidebar_state="collapsed",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)


# st.logo("soler.png", size='large')

st.session_state.fit_columns_on_grid_load = False

available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material", "quartz",  "alpine"]
selected_theme = st.sidebar.selectbox("Theme", available_themes, key='selected_theme')

pages = [st.Page("home.py", title="Home"),
         st.Page("catalogue_1.py", title="full_catalog_cme_merged_with_flares_and_weak_flares"),
         st.Page("catalogue_2.py", title="full_catalog_with_stix_merged_with_cme"),
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