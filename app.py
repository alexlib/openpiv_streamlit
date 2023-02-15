import streamlit as st
from PIL import Image

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

st.write("## Upload a pair of images")

uploaded_files = st.file_uploader("Upload here a pair of images", accept_multiple_files=True)
# for uploaded_file in uploaded_files:
#     # bytes_data = uploaded_file.read()
#     st.write("filename:", uploaded_file.name)
#     # st.write(bytes_data)
#     st.image(uploaded_file)

if len(uploaded_files) > 0:
    st.write("### Click on << or >> ")
    tab1, tab2 = st.tabs(["**<<**","**>>**"])

    with tab1:
        st.header("A")
        frame_a = Image.open(uploaded_files[0])
        st.image(frame_a, width=600)

    with tab2:
        st.header("B")
        frame_b = Image.open(uploaded_files[1])
        st.image(frame_b, width=600)

    
    frame_a.save("frame_a.jpg",)
    frame_b.save("frame_b.jpg")    
    st.sidebar.success("Choose `simple piv` above ")
    

# if len(uploaded_files) > 1:
#     frames = [Image.open(image) for image in uploaded_files]
#     frame_one = frames[0]
#     frame_one.save("my_awesome.gif", format="GIF", append_images=frames,
#                save_all=True, duration=200, loop=0)
#     st.image("my_awesome.gif")