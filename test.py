import streamlit as st
import pandas as pd
import requests
# from streamlit_folium import st_folium
# import folium

def delete_link(l):
    print(f"Just got called {l}")
    links = st.session_state["links"]
    print(links)
    links.remove(l)
    st.session_state["links"] = links


if "links" not in st.session_state:
    st.session_state["links"] = ["https://apicarto.ign.fr/api/gpu/municipality?insee=75114","https://apicarto.ign.fr/api/cadastre/commune?code_insee=75114",
"https://apicarto.ign.fr/api/cadastre/commune?code_insee=75115"]

if "dataframes" not in st.session_state:
    st.session_state["dataframes"] = []

# with st.sidebar:
#     m = folium.Map(location=[48.84648807785674,2.4227106571197514], zoom_start=16)
#     st_data = st_folium(m, width=725,height=200)
#     try:
#         st.write(st_data["center"])
#     except:
#         print("Cant find location")
with st.expander("Links"):
    link1 = st.text_input("Link")
    button = st.button("Add Link")
    if button and len(link1) > 0:
        st.write("Loaded")
        st.session_state["links"]  = st.session_state["links"]  + [link1]

    col1,col2 = st.columns([3,1])
    for l in st.session_state["links"]:
        col1.write(l)
        col2.button("delete",on_click=delete_link,args=[l],key=f"{l}_delete")
    # st.write()
    load = st.button("Load data")


if load:
    with st.expander("Databases"):
        if len(st.session_state['dataframes']) != len(st.session_state['links']) or len(st.session_state['dataframes']) == 0:
            dataframes = []
            for url,i in zip(st.session_state["links"],range(len(st.session_state["links"]))):

                st.subheader(f"Link {i}")
                st.write(url)
                try:
                    urlData = requests.get(url)
                    elevations = urlData.json()
                    df = pd.json_normalize(elevations['features'])
                    st.write(df)
                    dataframes.append(df)
                except: 
                    st.warning(f"{url} might not be supported yet")
            st.session_state['dataframes'] = dataframes
else:
    with st.expander("Databases"):
        if len(st.session_state['dataframes']) > 0:
            for url,i,df in zip(st.session_state["links"],range(len(st.session_state["links"])),st.session_state['dataframes']):

                st.subheader(f"Link {i}")
                st.write(url)
                st.write(df)



if "merges" not in st.session_state:
    st.session_state['merges'] = []


if "final_db" in st.session_state:
    final_db = st.session_state["final_db"]
else:
    final_db = None

if "final_db" in st.session_state:
    st.subheader("Current Final Table")
    st.write(st.session_state["final_db"])


with st.expander("Joins"):
    if len(st.session_state['dataframes']) > 0:
        col1,col2 = st.columns(2)
        if "final_db" in st.session_state:
            dataset_1 = col1.selectbox("Final db",["final_db"])
            column_1 = col1.selectbox("Columns",st.session_state['final_db'].columns,key=1)
        else:    
            dataset_1 = col1.selectbox("db 1",[x for x in range(len(st.session_state['dataframes']))])
            column_1 = col1.selectbox("Columns",st.session_state['dataframes'][dataset_1].columns,key=1)

        dataset_2 = col2.selectbox("db 2",[x for x in range(len(st.session_state['dataframes']))])    
        column_2 = col2.selectbox("Columns",st.session_state['dataframes'][dataset_2].columns,key=2)


        add_merge = st.button("add_merge")
        if add_merge and "final_db" not in st.session_state:
            final_db=st.session_state['dataframes'][dataset_1].merge(st.session_state['dataframes'][dataset_2],left_on=column_1,right_on=column_2)
            print("Je suis ici")
            st.session_state["final_db"] = final_db
            st.write(st.session_state["final_db"])
            
            st.rerun()
        elif add_merge:
            final_db=final_db.merge(st.session_state['dataframes'][dataset_2],left_on=column_1,right_on=column_2)
            st.session_state["final_db"] = final_db
            st.write(st.session_state["final_db"])
            st.rerun()



