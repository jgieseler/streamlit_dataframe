import streamlit as st


st.title("SOLER Catalogues")

st.write('Here you find some general info about the catalogues and how to use them.')

st.write('Select the catalogue you want to explore:')

st.page_link("pages/catalogue_1.py", label="CME_catalog", icon="1️⃣")
st.page_link("pages/catalogue_2.py", label="Flare_catalog", icon="2️⃣")

st.write('Open the sidebar (">>" in the top left) for options.')


st.markdown("""
            #### Acknowledgement

            <img hspace="10px" align="right" height="80px" src="https://github.com/user-attachments/assets/28c60e00-85b4-4cf3-a422-6f0524c42234" alt="EU flag">
            <img align="right" height="80px" src="https://github.com/user-attachments/assets/5bec543a-5d80-4083-9357-f11bc4b339bd" alt="SOLER logo">

            These catalogues are developed within the SOLER (*Energetic Solar Eruptions: Data and Analysis Tools*) project. SOLER has received funding from the European Union’s Horizon Europe programme under grant agreement No 101134999.

            The catalogues reflects only the authors’ view and the European Commission is not responsible for any use that may be made of the information it contains.
            """, unsafe_allow_html=True)