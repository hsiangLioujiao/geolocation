# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 09:28:41 2024

@author: g_s_s
"""

# https://discuss.streamlit.io/t/web-geolocation-api-to-get-users-location/9493/7
# https://pypi.org/project/streamlit-js-eval/
# https://github.com/aghasemi/streamlit_js_eval/tree/master


import streamlit as st
# from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
from streamlit_js_eval import streamlit_js_eval, get_geolocation
# import json
import pandas as pd
import matplotlib.pyplot as plt
import time
import threading
import queue

plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False


# # https://discuss.streamlit.io/t/realtime-data-update-to-streamlit-from-python-variable/35890/2
# q = queue.Queue()

# def test_run():
#     for x in range(1, 100):
#         time.sleep(1)
#         val = x
#         multiply = val * 10        
#         q.put((val, multiply))


# is_exit_target_if_main_exits = True
# threading.Thread(
#     target=test_run,
#     daemon=is_exit_target_if_main_exits).start()

# # dashboard title
# st.title("Streamlit Learning")

# # creating a single-element container.
# placeholder = st.empty()

# # Exit loop if we will not receive data within timeoutsec.
# timeoutsec = 30

# # Simulate data from test_run() in placeholder.
# while True:
#     try:
#         val, multiply = q.get(block=True, timeout=timeoutsec)
#     except queue.Empty:
#         break  # exit loop
#     else:
#         with placeholder.container():
#             col1, col2 = st.columns(2)
#             col1.metric(label="Current Value", value=val)
#             col2.metric(label="Multiply by 10 ", value=multiply)
#             q.task_done()





def test_form_callback(n):
    print(n) # Q2-1:調整數字後，按鈕不會立刻反應，回延遲一次才改變數字？


def form_callback(n):
    df=pd.DataFrame()
    # st.write(f"test! {n}")
    print(f"test! {n}")
    placeholder = st.empty()
    colA, colB, colC, colD = st.columns(4)
    for i in range(n):
        # st.write(i,n)
        print(i,n)
        loc = get_geolocation(f'my_key{i}')
        time.sleep(3)
        print(loc)
        if loc is not None:
            with placeholder.container():
                # st.write(loc)
                time.sleep(3)
                print(loc)
                print()
                print(loc['coords']['latitude'])
                print(loc['coords']['longitude'])
                print(loc['coords']['speed'])
                print()
                print()
                st.metric(label="timestamp", value=loc["timestamp"])
                st.metric(label="緯度", value=loc['coords']['latitude'])
                st.metric(label="經度", value=loc['coords']['longitude'])
                st.metric(label="速度", value=loc['coords']['speed'])
                # # Q1:使用st.columns時，不同迭代次數的結果會重複出現
                # colA.metric(label="timestamp", value=loc["timestamp"])
                # colB.metric(label="緯度", value=loc['coords']['latitude'])
                # colC.metric(label="經度", value=loc['coords']['longitude'])
                # colD.metric(label="速度", value=loc['coords']['speed'])                
                # # Q1
                dict_loc={"timestamp":loc["timestamp"],
                          "緯度":loc['coords']['latitude'],
                          "經度":loc['coords']['longitude'],
                          "高度":loc['coords']['altitude'],
                          "heading":loc['coords']["heading"],
                          "速度":loc['coords']['speed']}
                df_i=pd.DataFrame(dict_loc, index=[i])
                print(df_i)
                print()
                df=pd.concat([df, df_i])
        print(i, n, loc)
        print() # Q2-2:當callback時，迴圈只執行一次，沒有繼續迭代？
    return df



st.write(f"網頁: { streamlit_js_eval(js_expressions='window.location.origin', want_output = True, key = 'LOC')}")

with st.form("my_form"):
    col1, col2 = st.columns(2)
    n = col2.slider("紀錄時間[sec]:", 1, 600, 1)
    # Q2
    # submit_button = col1.form_submit_button(label='開始量測', on_click=test_form_callback , args=(n,))
    # st.write("test!")
    # print("test!")
    # Q2
    submit_button = col1.form_submit_button(label='開始量測')
    if submit_button:
        # test_form_callback(n) # 可以即時反應，沒有Q2-1問題
        df = form_callback(n)
        st.map(df, latitude='緯度', longitude='經度')
        print(df)
        print()
        st.dataframe(df)
st.write("量測結束.")





# loc = get_geolocation()

# col1, col2, col3 = st.columns(3)
# if st.button(label='開始量測'):
#     df=pd.DataFrame()
#     for i in range(3):
#         if loc is not None:    
#             print(loc)
#             print(type(loc)) # 使用dict來取得loc的內容
#             print()
#             print(loc['coords']['latitude'])
#             print(loc['coords']['longitude'])
#             print(loc['coords']['speed'])
#             print()
#             print()

#             col1.metric(label="緯度", value=loc['coords']['latitude'])
#             col2.metric(label="經度", value=loc['coords']['longitude'])
#             col3.metric(label="速度", value=loc['coords']['speed'])
#             dict_loc={"timestamp":loc["timestamp"],
#                       "緯度":loc['coords']['latitude'],
#                       "經度":loc['coords']['longitude'],
#                       "高度":loc['coords']['altitude'],
#                       "heading":loc['coords']["heading"],
#                       "速度":loc['coords']['speed']}
#             df_i=pd.DataFrame(dict_loc, index=[i])
#             print(df_i)
#             print()
#             df=pd.concat([df, df_i])
#             time.sleep(6)
#     st.map(df, latitude='緯度', longitude='經度')
#     print(df)
#     print()
#     st.dataframe(df)




    


    








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