import streamlit as st
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage import io, util
from openpiv.tools import imread, save
from openpiv.process import extended_search_area_piv, get_coordinates, get_field_shape
from openpiv.validation import sig2noise_val
from openpiv.filters import replace_outliers

# Function to process images
def process_images(img, params):
    # Normalize image to [0, 1] float
    img = img / img.max()
    if params['invert']:
        img = util.invert(img)
    if params['background_subtract']:
        img = img - params['background']
        img[img < 0] = 0
    if params['crop_ROI']:
        crop_x = params['crop_x']
        crop_y = params['crop_y']
        img = img[crop_y[0]:crop_y[1], crop_x[0]:crop_x[1]]
    return img

# Streamlit app
st.title("OpenPIV Streamlit App")

# Step 1: Select image folder
folder_path = st.text_input("Enter the path to the image folder:")

if folder_path:
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.png') or f.endswith('.jpg')]
    st.write(f"Found {len(image_files)} images.")

    # Step 2: Set processing parameters
    invert = st.checkbox("Invert images")
    background_subtract = st.checkbox("Subtract background")
    crop_ROI = st.checkbox("Crop ROI")
    crop_x = st.text_input("Crop X (comma-separated, e.g., 0,100)", "0,100")
    crop_y = st.text_input("Crop Y (comma-separated, e.g., 0,100)", "0,100")

    params = {
        'invert': invert,
        'background_subtract': background_subtract,
        'crop_ROI': crop_ROI,
        'crop_x': [int(x) for x in crop_x.split(',')],
        'crop_y': [int(y) for y in crop_y.split(',')],
        'background': None  # Placeholder for background image
    }

    # Step 3: Process images
    if st.button("Process Images"):
        for image_file in image_files:
            img_path = os.path.join(folder_path, image_file)
            img = io.imread(img_path)
            processed_img = process_images(img, params)
            # Save or display processed image
            st.image(processed_img, caption=f"Processed {image_file}")

        # Step 4: Run OpenPIV on processed images
        # Placeholder for OpenPIV processing
        st.write("Running OpenPIV on processed images...")

        # Example result visualization
        fig, ax = plt.subplots()
        ax.imshow(processed_img, cmap='gray')
        st.pyplot(fig)