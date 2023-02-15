import streamlit as st
from openpiv import tools, pyprocess
import numpy as np
import imageio.v3 as iio
import matplotlib.pyplot as plt

def simple_piv(im1, im2, window_size=32, search_size=48, overlap=16):
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
    return x, y, u, v, valid


st.title("OpenPIV analysis of the pair of images")

frame_a = iio.imread('frame_a.jpg')
frame_b =  iio.imread('frame_b.jpg')


window_size = st.sidebar.slider("Interrogation window size",
                                min_value=int(8),
                                max_value=int(np.max(np.array(frame_a.shape))/4),
                                value=32,
                                step=8)


overlap = st.sidebar.slider("Overlap",
                                min_value=int(0),
                                max_value=int(window_size-4),
                                value=int(window_size/2),
                                step=4)


# window_size = st.select_slider("Select the window size", 
#                                options=range(8, 256, 8), value=32)
search_size = int(window_size * 2)
# overlap = int(window_size / 2)

st.write("The window size is ", window_size)




# counter = frame_range[0]

x, y, u, v, valid = simple_piv(
    frame_a,
    frame_b,
    window_size=window_size,
    search_size=search_size,
    overlap=overlap
    )

arrow_length = st.sidebar.slider("Arrow length scaling",
                                 min_value=1,
                                 max_value=20,
                                 value=12)

fig, ax = plt.subplots()
# ax.text(20, 20, str(counter), color="y")
ax.imshow(frame_a, cmap="gray", alpha=0.8, origin="upper")
ax.quiver(x[valid], y[valid], u[valid], -v[valid], scale=10 * arrow_length, color="y")
ax.quiver(x[~valid], y[~valid], u[~valid], -v[~valid], scale=10 * arrow_length, color="r")
# ax.axis("off")

# Major ticks every 20, minor ticks every 5
# major_ticks = np.arange(0, frame_a.shape[1], window_size)
# minor_ticks = np.arange(0, frame_a.shape[0], window_size)
# sst.write(x)

ax.set_xticks(np.r_[x[0,:] - window_size/2 - overlap,frame_a.shape[1]-overlap])
# ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(np.concatenate([y[:,0] + window_size/2]))
# ax.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
# ax.grid('on',color='y')
ax.grid(which='major', axis='both', linestyle='--',color='y')


st.pyplot(fig)
# fig.savefig("res.png")
# res_frame = iio.imread('res.png')
# print(images[0].shape, res_frame.shape)
# images.append(res_frame)
# st.pyplot(fig)
# counter += 1
# frames = [Image.open(image) for image in uploaded_files]
# frame_one = images[0]
# frame_one.save("new.gif", format="GIF", append_images=images,
#             save_all=True, duration=200, loop=0)
    
# im.save("new.gif", format="GIF")
# iio.imwrite("new.gif", images)

# st.image("new.gif")

