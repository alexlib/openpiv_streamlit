import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

frame_a = st.session_state.frame_a



"# :dart: Streamlit Image Coordinates: Image Update"

if "points" not in st.session_state:
    st.session_state["points"] = []

"## Click on image"


def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 10
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
        value = streamlit_image_coordinates(img, key="pil")
        st.write(value)
        if value is not None:
            point = value["x"], value["y"]
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="yellow")
            st.session_state["points"].append(point)
            st.write(st.session_state["points"])
            st.write(len(st.session_state["points"]))
            
            if len(st.session_state["points"]) == 2:
                st.write(f'Two points: {st.session_state["points"]}')
                draw.rectangle(st.session_state["points"], fill='yellow', outline='yellow', width=5)
                st.session_state["points"] = []
                
            
            

        



            # if point not in st.session_state["points"]:
            #     st.session_state["points"].append(point)
            #     if len(st.session_state["points"]) == 2:
            #         st.write(st.session_state["points"])
                    
            #         # 
            #         st.session_state["points"].clear()
            #     # st.experimental_rerun()
            