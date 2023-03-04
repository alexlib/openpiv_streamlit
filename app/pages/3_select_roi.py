import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

frame_a = st.session_state.frame_a

st.set_page_config(
    page_title="Streamlit Image Coordinates: Image Update",
    page_icon="🎯",
    layout="wide",
)

"# :dart: Streamlit Image Coordinates: Image Update"

if "points" not in st.session_state:
    st.session_state["points"] = []


"## Click on image"


def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 5
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )


with st.echo("below"):
    # with Image.open("kitty.jpeg") as img:
    with Image.fromarray(frame_a) as img:
        draw = ImageDraw.Draw(img)
        # coords = get_ellipse_coords([])
        # draw.rectangle(coords, fill=None, outline='yellow', width=1)

        # # Draw an ellipse at each coordinate in points
        for point in st.session_state["points"]:
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="white")
            
            value = streamlit_image_coordinates(img, key="pil")

            if value is not None:
                point = value["x"], value["y"]

                if point not in st.session_state["points"]:
                    st.session_state["points"].append(point)
                    if len(st.session_state["points"]) == 2:
                        draw.rectangle(st.session_state["points"][:2], fill=None, outline='yellow', width=1)
                    
                    st.experimental_rerun()
                    
        
            
                
    # st.write(st.session_state["points"])
