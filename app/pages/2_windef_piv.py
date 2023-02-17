""" OpenPIV Streamlit app """
import streamlit as st
from openpiv import windef, validation, filters, scaling, tools
import numpy as np
import imageio.v3 as iio
import matplotlib.pyplot as plt

st.title("Multi-pass window deformation analysis")

frame_a = st.session_state.frame_a
frame_b = st.session_state.frame_b

settings = windef.PIVSettings()

# st.sidebar.write(settings)

settings.num_of_iterations = st.sidebar.slider("Number of iterations",
                                      min_value=1,
                                      max_value=4,
                                      value=1)

window_size = st.sidebar.slider("Smallest window size",
                                min_value=int(8),
                                max_value=int(np.max(np.array(frame_a.shape))/4),
                                value=32,
                                step=8)


# overlap = st.sidebar.slider("Overlap",
#                                 min_value=int(0),
#                                 max_value=int(window_size-4),
#                                 value=int(window_size/2),
#                                 step=4)



# search_size = int(window_size * 2)


settings.windowsizes = [int(window_size*2**n) for n in range(settings.num_of_iterations)][::-1]
settings.overlap = [int(w/2) for w in settings.windowsizes]
st.sidebar.write("The window sizes are:", settings.windowsizes)

# st.write(settings)
# st.write("The overlap are:", settings.overlap)

# x, y, u, v, s2n = windef.first_pass(
#             frame_a,
#             frame_b,
#             settings
#         )
# valid = s2n > np.percentile(s2n, 5)

def windef_piv(frame_a, frame_b, settings):

    from openpiv.windef import first_pass, multipass_img_deform
    from openpiv import smoothn

    x, y, u, v, s2n = first_pass(
                frame_a,
                frame_b,
                settings
            )
    grid_mask = np.zeros_like(u, dtype=bool)
    # mask the velocity
    u = np.ma.masked_array(u, mask=grid_mask)
    v = np.ma.masked_array(v, mask=grid_mask)

    flags = validation.typical_validation(u, v, s2n, settings)

    u, v = filters.replace_outliers(
        u,
        v,
        flags,
        method=settings.filter_method,
        max_iter=settings.max_filter_iteration,
        kernel_size=settings.filter_kernel_size,
    )

    # u, *_ = smoothn.smoothn(
    #                 u,
    #                 s=settings.smoothn_p
    #             )
    # v, *_ = smoothn.smoothn(
    #     v,
    #     s=settings.smoothn_p
    # )

    u = np.ma.masked_array(u, mask=grid_mask)
    v = np.ma.masked_array(v, mask=grid_mask)

    for i in range(1, settings.num_iterations):
        x, y, u, v, grid_mask, flags = multipass_img_deform(
            frame_a,
            frame_b,
            i,
            x,
            y,
            u,
            v,
            settings
        )

        # if settings.smoothn is True and i < settings.num_iterations-1:
        #     u, dummy_u1, dummy_u2, dummy_u3 = smoothn.smoothn(
        #         u, s=settings.smoothn_p
        #     )
        #     v, dummy_v1, dummy_v2, dummy_v3 = smoothn.smoothn(
        #         v, s=settings.smoothn_p
        #     )

        u = np.ma.masked_array(u, np.ma.nomask)
        v = np.ma.masked_array(v, np.ma.nomask)


    u = u.filled(0.)
    v = v.filled(0.)

    u = np.ma.masked_array(u, np.ma.nomask)
    v = np.ma.masked_array(v, np.ma.nomask)

    # pixel / frame -> pixel / second
    u /= settings.dt 
    v /= settings.dt
    
    # "scales the results pixel-> meter"
    x, y, u, v = scaling.uniform(x, y, u, v,
                                    scaling_factor=settings.scaling_factor)

    # before saving we conver to the "physically relevant"
    # right-hand coordinate system with 0,0 at the bottom left
    # x to the right, y upwards
    # and so u,v
    # x, y, u, v = tools.transform_coordinates(x, y, u, v)
    
    valid = np.ones_like(u, dtype=bool)
    
    return x, y, u, v, valid

            
x, y, u, v, valid = windef_piv(
    frame_a,
    frame_b,
    settings=settings
    )


window_size = settings.windowsizes[-1]
overlap = settings.overlap[-1]


arrow_length = st.sidebar.slider("Arrow length scaling",
                                 min_value=1,
                                 max_value=20,
                                 value=12)

fig, ax = plt.subplots()
# ax.text(20, 20, str(counter), color="y")
ax.imshow(frame_a, cmap="gray", alpha=0.8, origin="upper")
ax.quiver(x[valid], y[valid], u[valid], -v[valid], scale=10 * arrow_length, color="y")
# ax.quiver(x[~valid], y[~valid], u[~valid], -v[~valid], scale=10 * arrow_length, color="r")
# ax.axis("off")

# Major ticks every 20, minor ticks every 5
# major_ticks = np.arange(0, frame_a.shape[1], window_size)
# minor_ticks = np.arange(0, frame_a.shape[0], window_size)
# sst.write(x)


# ax.set_xticks(np.r_[x[0,:] - window_size/2 - overlap,frame_a.shape[1]-overlap])
# ax.set_xticks(minor_ticks, minor=True)
# ax.set_yticks(np.concatenate([y[:,0] + window_size/2]))
# ax.set_yticks(minor_ticks, minor=True)

# And a corresponding grid
# ax.grid('on',color='y')
# ax.grid(which='major', axis='both', linestyle='--',color='y')

st.pyplot(fig)

