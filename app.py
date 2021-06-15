# -- coding: utf-8 --
"""
Created on Sun Jun 13 18:57:48 2021

@author: berkin, semih
"""
import streamlit as st
import pandas as pd
import networkx as nx
from PIL import Image
import timeit


connections = pd.read_csv('london.connections.csv', index_col=False)
stations = pd.read_csv('london.stations.csv', index_col=False)
lines = pd.read_csv('london.lines.csv', index_col=False)
coordinates = pd.read_csv('coordinates.csv', index_col=False)

stations_dict = pd.Series(stations.name.values,index=stations.id).to_dict()
lines_dict = pd.Series(lines.name.values,index=lines.line).to_dict()

connections['station1'] = connections['station1'].map(stations_dict)
connections['station2'] = connections['station2'].map(stations_dict)
connections['line'] = connections['line'].map(lines_dict)


G = nx.Graph()
for connection_id, connection in connections.iterrows():
    station1_name = connection['station1']
    station2_name = connection['station2']
    line_name = connection['line']
    time = connection['time']
    G.add_edge(station1_name, station2_name, weight = time, line = line_name)
    
st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center; margin-bottom:100px;;color: red;'>London Journey Planner</h1>", unsafe_allow_html=True)

c1, c2= st.beta_columns((1, 2))


def get_time(G, path):
    total = 0
    for u, v in zip(path[:-1], path[1:]):
        total += G.edges[u,v]['weight']
    return total



def get_transfer(G, path):


    current_line = G.edges[path[0],path[1]]['line']
    for u, v in zip(path[:-1], path[1:]):
        flag = False
        if(G.edges[u,v]['line'] != current_line): 
            node = u
            cl = current_line
            flag = True
        else:
            st.write(':arrow_forward: ' + u)
        current_line = G.edges[u,v]['line']
        
        if(flag):
            st.write(':white_circle:' + node + ' (Transfer from ' + cl + ' to ' + current_line + ')')
            
with c1:
    
    st.title('Plan a Journey')
    option = st.selectbox(
      'From:',
         options=list(G.nodes))
    
   
    
    
    option2 = st.selectbox(
      'To:',
         options=list(G.nodes)[::-1])
    
 
    start = timeit.default_timer()
    path = nx.dijkstra_path(G,option,option2, weight='weight')
    stop = timeit.default_timer()

    print('Time: ', stop - start)  
    
    navigate = st.button('Navigate')
    
    
    if navigate:
            
            st.markdown('**Steps**')
            get_transfer(G, path)
            st.write(':arrow_forward: ' + option2)
            st.write(':hourglass_flowing_sand: **Estimated travel time:** ' + str(get_time(G, path)) + ' minutes.')
            
with c2:
    image = Image.open('tube_map.jpg')
    st.image(image, caption='London Tube Map', width=None) 










            


            
            

#st.map(coordinates)
