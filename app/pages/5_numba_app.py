import numpy as np
import numba
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import imageio
import io
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imageio
import io
@numba.jit(nopython=True)
def compute_piv(image_a, image_b, window_size):
    u = np.zeros(image_a.shape)
    v = np.zeros(image_a.shape)
    
    half_window = window_size // 2
    
    for i in range(half_window, image_a.shape[0] - half_window):
        for j in range(half_window, image_a.shape[1] - half_window):
            window_a = image_a[i-half_window:i+half_window, j-half_window:j+half_window]
            best_offset = (0, 0)
            best_corr = -1
            
            for di in range(-half_window, half_window+1):
                for dj in range(-half_window, half_window+1):
                    if (i + di - half_window < 0 or i + di + half_window >= image_a.shape[0] or
                        j + dj - half_window < 0 or j + dj + half_window >= image_a.shape[1]):
                        continue
                    
                    window_b = image_b[i + di - half_window: i + di + half_window,
                                       j + dj - half_window: j + dj + half_window]
                    
                    corr = np.sum(window_a * window_b)
                    
                    if corr > best_corr:
                        best_corr = corr
                        best_offset = (di, dj)
            
            u[i, j] = best_offset[0]
            v[i, j] = best_offset[1]
    
    return u, v

def cold_start():
    # Cold start Numba compilation
    image_a = np.random.random((32, 32))
    image_b = np.random.random((32, 32))
    compute_piv(image_a, image_b, 8)



def display_gif(image_a, image_b, u, v):
    fig, ax = plt.subplots()
    ax.imshow(image_a, cmap='gray')
    ax.quiver(np.arange(u.shape[1]), np.arange(u.shape[0]), v, u, color='r')
    plt.savefig('piv_result.png')
    piv_image = Image.open('piv_result.png')
    
    with io.BytesIO() as output:
        piv_image.save(output, format="GIF")
        gif_image = output.getvalue()
    
    st.image(gif_image, format="GIF")

def main():
    st.title("Fast PIV Algorithm with Numba")

    uploaded_file_a = st.file_uploader("Choose Image A...", type="png")
    uploaded_file_b = st.file_uploader("Choose Image B...", type="png")

    if uploaded_file_a and uploaded_file_b:
        image_a = np.array(Image.open(uploaded_file_a).convert('L'))
        image_b = np.array(Image.open(uploaded_file_b).convert('L'))

        if st.button("Run PIV"):
            u, v = compute_piv(image_a, image_b, 8)
            display_gif(image_a, image_b, u, v)

    st.sidebar.header("Upload Images")
    st.sidebar.info("Upload a pair of images to analyze motion.")

if __name__ == "__main__":
    cold_start()
    main()




