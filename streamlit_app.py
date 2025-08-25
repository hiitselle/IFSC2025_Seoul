import streamlit as st

st.set_page_config(page_title="CSS Test", layout="wide")

st.markdown("""
<style>
.test-green {
    background-color: green !important;
    color: white !important;
    padding: 20px !important;
    margin: 10px 0 !important;
}
.test-red {
    background-color: red !important;
    color: white !important;
    padding: 20px !important;
    margin: 10px 0 !important;
}
.test-yellow {
    background-color: yellow !important;
    color: black !important;
    padding: 20px !important;
    margin: 10px 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("BASIC CSS TEST")

st.markdown('<div class="test-green">This should be GREEN</div>', unsafe_allow_html=True)
st.markdown('<div class="test-red">This should be RED</div>', unsafe_allow_html=True)
st.markdown('<div class="test-yellow">This should be YELLOW</div>', unsafe_allow_html=True)

st.write("Regular Streamlit text - this should work normally")
