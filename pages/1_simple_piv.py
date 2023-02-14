import streamlit as st
from openpiv import tools, pyprocess
import numpy as np
import imageio.v3 as iio
import matplotlib.pyplot as plt
from PIL import Image

def simple_piv(im1, im2, window_size=32, search_size=48, overlap=16, plot=True):
    """
    Simplest PIV run on the pair of images using default settings

    piv(im1,im2) will create a tmp.vec file with the vector filed in pix/dt
    (dt=1) from two images, im1,im2 provided as full path filenames
    (TIF is preferable, whatever imageio can read)

    """
    if isinstance(im1, str):
        im1 = tools.imread(im1)
        im2 = tools.imread(im2)

    u, v, s2n = pyprocess.extended_search_area_piv(
        im1.astype(np.int32), im2.astype(np.int32), window_size=window_size,
        overlap=overlap, search_area_size=search_size,
    )
    x, y = pyprocess.get_coordinates(image_size=im1.shape,
                                     search_area_size=search_size,
                                     overlap=overlap)

    valid = s2n > np.percentile(s2n, 5)

    if plot:
        _, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(im1, cmap=plt.get_cmap("gray"), alpha=0.5, origin="upper")
        ax.quiver(x[valid], y[valid], u[valid], -v[valid], scale=70,
                  color='r', width=.005)
        plt.show()

    return x, y, u, v


st.title("OpenPIV analysis of GIF")
st.image("my_awesome.gif")

images = []
im = iio.imread("my_awesome.gif", index=None)
for frame in im:
    # st.write(frame.shape)
    if frame.ndim > 2:
        frame = tools.rgb2gray(frame)
    images.append(frame)

st.write(f'{len(images)} frames')

# frame_range = st.slider(
#     "Frames", value=(0, len(images)), min_value=0, max_value=len(images)
# )

window_size = st.select_slider("Select the window size", 
                               options=range(8, 256, 8), value=32)
search_size = int(window_size * 2)
overlap = int(window_size / 2)

st.write("The window size is ", window_size)

arrow_length = st.slider("Arrow length scaling", min_value=1, max_value=10, value=10)


# counter = frame_range[0]

x, y, u, v = simple_piv(
    images[0],
    images[1],
    window_size=window_size,
    search_size=search_size,
    overlap=overlap,
    plot=False)

fig, ax = plt.subplots()
# ax.text(20, 20, str(counter), color="y")
ax.imshow(images[0], cmap="gray", alpha=0.8, origin="upper")
ax.quiver(x, y, u, -v, scale=10 * arrow_length, color="r")
ax.axis("off")
fig.savefig("res.png")
res_frame = iio.imread('res.png')
# print(images[0].shape, res_frame.shape)
# images.append(res_frame)
# st.pyplot(fig)
# counter += 1
# frames = [Image.open(image) for image in uploaded_files]
# frame_one = images[0]
# frame_one.save("new.gif", format="GIF", append_images=images,
#             save_all=True, duration=200, loop=0)
    
# im.save("new.gif", format="GIF")
iio.imwrite("new.gif", images)

st.image("new.gif")

