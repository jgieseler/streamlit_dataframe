import streamlit as st


st.title("SOLER Catalogs")

st.markdown('The [SOLER](https://soler-horizon.eu) project provides three interlinked catalogs focusing on different aspects of energetic solar eruptions: solar flares, coronal mass ejections (CME), and solar energetic particles (SEP).')

st.write('Select the catalog you want to explore:')

st.page_link("pages/cme_catalog.py", label="CME catalog", icon="1️⃣")
st.page_link("pages/flare_catalog.py", label="Flare catalog", icon="2️⃣")
st.page_link("pages/sep_catalog.py", label="SEP catalog", icon="3️⃣")

# st.write('Open the sidebar (">>" in the top left) for options.')


st.markdown("""
            #### Acknowledgement

            <img hspace="10px" align="right" height="80px" src="https://github.com/user-attachments/assets/28c60e00-85b4-4cf3-a422-6f0524c42234" alt="EU flag">
            <img align="right" height="80px" src="https://github.com/user-attachments/assets/5bec543a-5d80-4083-9357-f11bc4b339bd" alt="SOLER logo">

            These catalogs are developed within the SOLER (*Energetic Solar Eruptions: Data and Analysis Tools*) project. SOLER has received funding from the European Union’s Horizon Europe programme under grant agreement No 101134999.

            The catalogs reflects only the authors’ view and the European Commission is not responsible for any use that may be made of the information it contains.
            """, unsafe_allow_html=True)