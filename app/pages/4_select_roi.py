import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image

frame_a = st.session_state.frame_a


# with st.echo("below"):
# with Image.open("kitty.jpeg") as img:
with Image.fromarray(frame_a) as img:
    cropped_img = st_cropper(img, realtime_update=True, box_color="yellow",
                            aspect_ratio=None,
                            return_type="box")

# Manipulate cropped image at will
st.write("Preview")
# _ = cropped_img.thumbnail((150,150))
# st.image(cropped_img)
st.write(cropped_img)