# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:28:41 2024

@author: g_s_s
"""


# https://pypi.org/project/streamlit-js-eval/
# https://github.com/aghasemi/streamlit_js_eval/tree/master


import streamlit as st
# from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from streamlit_js_eval import streamlit_js_eval, get_geolocation
# import json
import pandas as pd
import matplotlib.pyplot as plt
import time

plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False


# st.write(f"User agent is _{streamlit_js_eval(js_expressions='window.navigator.userAgent', want_output = True, key = 'UA')}_")
# st.write(f"Screen width is _{streamlit_js_eval(js_expressions='screen.width', want_output = True, key = 'SCR')}_")
# st.write(f"Browser language is _{streamlit_js_eval(js_expressions='window.navigator.language', want_output = True, key = 'LANG')}_")
st.write(f"網頁: { streamlit_js_eval(js_expressions='window.location.origin', want_output = True, key = 'LOC')}_")

# (待修正)
# st.write(f"my coordinates is _{ streamlit_js_eval(js_expressions='window.getCurrentPosition', want_output = True, key = 'myLOC')}_")


# Copying to clipboard only works with a HTTP connection
# copy_to_clipboard("Text to be copied!", "Copy something to clipboard (only on HTTPS)", "Successfully copied" , component_key = "CLPBRD")

# Share something using the sharing API
# create_share_link(dict({'title': 'streamlit-js-eval', 'url': 'https://github.com/aghasemi/streamlit_js_eval', 'text': "A description"}), "Share a URL (only on mobile devices)", 'Successfully shared', component_key = 'shdemo')


# if st.checkbox("Check my location"):
#     loc = get_geolocation()
#     st.write(f"Your coordinates are {loc}")


loc = get_geolocation()
# st.write(f"Your coordinates are {loc}")

df=pd.DataFrame()
col1, col2, col3 = st.columns(3)
for i in range(100):
    if loc is not None:
        df_loc=pd.DataFrame(loc)
        print(df_loc)
        # st.write(f"緯度: {df_loc.loc['latitude', 'coords']}")
        # st.write(f"經度: {df_loc.loc['longitude', 'coords']}")
        # st.write(f"速度: {df_loc.loc['speed', 'coords']}")
        
        col1.metric(label="緯度", value=f"{df_loc.loc['latitude', 'coords']}")
        col2.metric(label="經度", value=f"{df_loc.loc['longitude', 'coords']}")
        col3.metric(label="速度", value=f"{df_loc.loc['speed', 'coords']}")
        
        dict_loc={"time":df_loc.loc["accuracy", "timestamp"],
                  "緯度":df_loc.loc["latitude", "coords"],
                  "經度":df_loc.loc["longitude", "coords"],
                  "高度":df_loc.loc["altitude", "coords"],
                  "heading":df_loc.loc["heading", "coords"],
                  "速度":df_loc.loc["speed", "coords"]}
        df=pd.concat([df, pd.DataFrame(dict_loc, index=[0])])
    time.sleep(6)

print(df)
st.map(df, latitude='緯度', longitude='經度')


    
# if True:
#     x = streamlit_js_eval(js_expressions='window.innerWidth', key='WIDTH',  want_output = True,)                
#     st.write(f"Width is {x}")




# import streamlit as st
# from bokeh.models.widgets import Button
# from bokeh.models import CustomJS
# from streamlit_bokeh_events import streamlit_bokeh_events

# loc_button = Button(label="Get Location")
# loc_button.js_on_event("button_click", CustomJS(code="""
#     navigator.geolocation.getCurrentPosition(
#         (loc) => {
#             document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
#         }
#     )
#     """))
# result = streamlit_bokeh_events(
#     loc_button,
#     events="GET_LOCATION",
#     key="get_location",
#     refresh_on_update=False,
#     override_height=75,
#     debounce_time=0)