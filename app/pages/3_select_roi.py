from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from svgpathtools import parse_path

# def full_app(frame_a):
frame_a = st.session_state.frame_a

st.sidebar.header("Configuration")
st.markdown(
    """
Draw on the canvas, get the drawings back to Streamlit!
* Configure canvas in the sidebar
* In transform mode, double-click an object to remove it
* In polygon mode, left-click to add a point, right-click to close the polygon, double-click to remove the latest point
"""
)

with st.echo("below"):
    # Specify canvas parameters in application
    # drawing_mode = st.sidebar.selectbox(
    #     "Drawing tool:",
    #     ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
    # )
    drawing_mode = "rect"
    stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
    if drawing_mode == 'point':
        point_display_radius = st.sidebar.slider("Point display radius: ", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke color hex: ")
    bg_color = st.sidebar.color_picker("Background color hex: ", "#eee")
    # bg_image = st.sidebar.file_uploader("Background image:", type=["png", "jpg"])
    realtime_update = st.sidebar.checkbox("Update in realtime", True)


    
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.fromarray(frame_a), #Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=150,
        drawing_mode=drawing_mode,
        point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
        display_toolbar=st.sidebar.checkbox("Display toolbar", True),
        key="full_app",
    )

    # Do something interesting with the image data and paths
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data)
    if canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        for col in objects.select_dtypes(include=["object"]).columns:
            objects[col] = objects[col].astype("str")
        st.dataframe(objects)
