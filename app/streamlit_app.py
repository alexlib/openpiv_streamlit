import streamlit as st
import imageio.v3 as iio
from skimage.util import img_as_ubyte
import pathlib

st.set_page_config(
    page_title="OpenPIV Streamlit app",
    page_icon="👋",
)

st.write("# OpenPIV Streamlit app 👋")



# st.markdown(
#     """
#     Streamlit is an open-source app framework built specifically for
#     Machine Learning and Data Science projects.
#     **👈 Select a demo from the sidebar** to see some examples
#     of what Streamlit can do!
#     ### Want to learn more?
#     - Check out [streamlit.io](https://streamlit.io)
#     - Jump into our [documentation](https://docs.streamlit.io)
#     - Ask a question in our [community
#         forums](https://discuss.streamlit.io)
#     ### See more complex demos
#     - Use a neural net to [analyze the Udacity Self-driving Car Image
#         Dataset](https://github.com/streamlit/demo-self-driving)
#     - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
# """
# )
st.write("OpenPIV is an open source particle image velocimetry [website](https://www.openpiv.net)")

st.write("### Want to know more?")
st.markdown("""
        - check our [website](https://www.openpiv.net)
        - try our examples [Notebooks](https://github.com/openpiv/openpiv-python-examples)  
        - Ask a question in our [Google group forum](https://groups.google.com/g/openpiv-users) 
    """
)

st.write("## Upload a pair of images:")

uploaded_files = st.file_uploader("Upload here a pair of images", accept_multiple_files=True)

st.write("## Or click below: _Load demo files_ ")

if st.button('Load demo files'):
    uploaded_files = [
        'https://raw.githubusercontent.com/OpenPIV/openpiv-python-examples/main/test1/exp1_001_a.bmp',
        'https://raw.githubusercontent.com/OpenPIV/openpiv-python-examples/main/test1/exp1_001_b.bmp',
    ]

if len(uploaded_files) > 0:
    st.write("### Click on << or >> ")
    tab1, tab2 = st.tabs(["**<<**","**>>**"])

    with tab1:
        st.header("A")
        st.session_state.frame_a = img_as_ubyte(iio.imread(uploaded_files[0]))
        if st.session_state.frame_a.ndim > 2:
            st.session_state.frame_a = st.session_state.frame_a[:,:,0]
        st.image(st.session_state.frame_a, width=600)

    with tab2:
        st.header("B")
        st.session_state.frame_b = img_as_ubyte(iio.imread(uploaded_files[1]))
        if st.session_state.frame_b.ndim > 2:
            st.session_state.frame_b = st.session_state.frame_b[:,:,0]
            
        st.image(st.session_state.frame_b, width=600)


    # st.session_state.user_file_path = pathlib.Path("img/") / 'frame_a.png'
    # with open(st.session_state.user_file_path, "wb") as user_file:
    #     user_file.write(uploaded_files[0].getbuffer())
        
    # st.write(st.session_state.user_file_path)



    st.sidebar.success("Choose `simple piv` above ")