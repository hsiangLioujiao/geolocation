import streamlit as st
from streamlit_js_eval import streamlit_js_eval, get_geolocation
import pandas as pd
import matplotlib.pyplot as plt
import time

plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False




def form_callback(n):
    df=pd.DataFrame()
    print(f"每間隔{m}秒取樣一次，共取樣{n}次。")
    placeholder = st.empty()
    for i in range(n):
        print(i,n)
        loc = get_geolocation(f'my_key{i}')
        time.sleep(m)
        print(loc)
        if loc is None:
            with placeholder.container():
                st.write(f"第{i+1}次量測：")
                st.write(f"沒有抓到位置訊號(累計{i+1-len(df)}次)，請重新量測。")
        else:
            with placeholder.container():
                st.write(f"第{i+1}次量測：")
                colA, colB, colC = st.columns(3)
                # st.metric(label="緯度", value=loc['coords']['latitude'])
                # st.metric(label="經度", value=loc['coords']['longitude'])
                # st.metric(label="速度", value=loc['coords']['speed'])
                colA.metric(label="緯度", value=loc['coords']['latitude'])
                colB.metric(label="經度", value=loc['coords']['longitude'])
                colC.metric(label="速度", value=loc['coords']['speed'])                
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
        time.sleep(3)
        placeholder.empty()
    return df




# 主程式
m = 3 # 取樣時間間隔
st.write(f"網頁: { streamlit_js_eval(js_expressions='window.location.origin', want_output = True, key = 'LOC')}")

with st.form("my_form"):
    col1, col2 = st.columns(2)
    submit_button = col1.form_submit_button(label='開始量測')
    n = col2.slider(f"每間隔{m}秒記錄1次，請輸入總記錄次數[次]:", 1, 200, 1)
    
    if submit_button:
        df = form_callback(n)
        if len(df)>0:
            st.map(df, latitude='緯度', longitude='經度')
            print(df)
            print()
            st.dataframe(df)

if submit_button:
    st.write("量測結束。")