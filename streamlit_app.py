import streamlit as st
import streamlit.components.v1 as components
from streamlined_custom_component import create_component
from pathlib import Path

# Configure the page
st.set_page_config(
    page_title = "Storm Damage Forecaster",
    page_icon = "🗺️",
    layout = "wide",
    initial_sidebar_state = "collapsed"
)

# Custom CSS for layout
st.markdown(
    """
    <style>
    
    /*Hide default streamlit elements*/
    .stApp > header {visibility: hidden;}
    .stApp > div > div > div > div > div > section > div {padding-top: 0rem;}
    #MainMenu {visibility:hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stToolbar {display: none;}
    div[data-testid="stToolbar"] {display: none;}
    .main .block-container {padding-top: 0;}
    .main .block-container {margin-top: 0;}
    .stApp {padding-top 0;}
    .stApp > div:first-child{margin-top 0;}
    body {margin-top: 0;}
    
    /*Main container styling*/
    .main-container {
        height: 100vh;
        display: flex;
        flex-direction: column;
        padding: 0;
        margin: 0;
        }
    
    /*Header styling*/
    .header-bar {
        background-color: #1f2937;
        color: white;
        padding: 1rem 2rem;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 1000;
        margin-top: -1rem;
        position: relative;
        top: 0
    }
    
    /*Map Container*/
    .map-container{
        position: relative;
        flex: 1;
        height: calc(100vh - 80px);
        background-color: #f0f2f6;
    }
    
    /*Map iframe styling*/
    .map-iframe-col {
        width: 100%;
        height: calc(100vh - 80px);
        border: none;
        background-color: white;
    }
    
    /*Floating sidebar*/
    .floating-sidebar {
        position: fixed;
        top: 100px;
        right: 20px;
        width: 20%;
        max-width: 300px;
        min-wdith: 200px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        padding: 1.5rem;
        z-index: 1000;
        max-height: calc(100vh - 120px);
        overflow-y: auto;
    }
    
    /*Button container*/
    .button-container {
        position: fixed;
        top: 140px;
        right: 20px;
        width: 20%;
        max-width: 300px;
        min-width: 200px;
        background-color: transparent;
        padding: 0 1.5rem;
        z-index: 1001;
    }
    
    /*Button styling*/
    .stButton > button {
        width: 100%;
        margin-bottom: 0.5rem;
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }
    
    .stButton> button:hover {
        background-color: #1d4ed8;
    }
    
    /*Remove default streamlit spacing*/
    .block-container {
        padding: 0;
        max-width: none;
    }
    
    /*Custom metric styling*/
    div[data-testid="metric-container"]:nth-child(1) [data-testid="metric-value"] {
        color: #10b981 !important;
        }
        
    div[data-testid="metric-container"]:nth-child(2) [data-testid="metric-value"] {
        color: #ef4444 !important;
        }
        
    div[data-testid="metric-container"]:nth-child(3) [data-testid="metric-value"] {
        color: #10b981 !important;
        }
        
    </style>
    
    """, unsafe_allow_html=True
)

# Header
st.markdown("""
    <div class = "header-bar">
    🗺️ Reliability Map
    </div>
    """, unsafe_allow_html = True)

map_col, sidebar_col = st.columns([0.8, 0.2])

path = "http://localhost:8000/"
path = ''
with map_col:
    # Initialize state
    if 'map_type' not in st.session_state:
        st.session_state.map_type = 'ExpectedStormOutages'
    if 'layer_choice' not in st.session_state:
        st.session_state.layer_choice = 'Street'
    if 'neighborhood' not in st.session_state:
        st.session_state.neighborhood = ''
        
    
    if st.session_state.map_type == 'WeatherData':
        current_map_url = str(Path(__file__).parent) + '/static/WeatherData.html'
        print(current_map_url)
    else:
        metric = st.session_state.map_type   
        current_map_url = ''
        if st.session_state.neighborhood != '' and st.session_state.neighborhood is not None:
            current_map_url =  current_map_url + st.session_state.neighborhood + "_"
            metric = 'ExpectedStormOutages' # we don't really have anything dynamic so just plot the outages version

        current_map_url = str(Path(__file__).parent) + 'static/' + current_map_url + st.session_state.layer_choice + "_" + metric + ".html"    
    
    ### Create the map
    print(current_map_url)
    with open(current_map_url, 'r') as f:
        html_file = f.read()
    components.html(html_file, height = "calc(100vh-80px);", width= "100%")
    #st.markdown(f'<iframe class="map-iframe-col" src="{current_map_url}" title="Interactive Map"></iframe>', unsafe_allow_html=True)

    
with sidebar_col:
    st.markdown("### 🗺️ Map Controls")
    
    st.selectbox(
        "Storm Selector:",
        ["11/19/2024 (demo data)"],
        index = 0,
    )
        
    if st.button("Expected Outages"):
        st.session_state.map_type = "ExpectedStormOutages"
        st.rerun()
        
    if st.button("Expected CI"):
        st.session_state.map_type = "ExpectedStormCI"
        st.rerun()
        
    if st.button("Expected CMI"):
        st.session_state.map_type = "ExpectedStormCMI"
        st.rerun()
        
    if st.button("Visualize Windspeed"):
        st.session_state.map_type = "WeatherData"
        st.rerun()
        
    map_layer = st.selectbox(
        "Select Layer:",
        ["Street", "Satellite",],
        index = ["Street", "Satellite"].index(st.session_state.layer_choice),
        key = "layer_selectbox"
    )
    
    if map_layer != st.session_state.layer_choice:
        st.session_state.layer_choice = map_layer
        st.rerun()
        
    st.markdown("---")
    
    st.markdown("### 📊 Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label = "SAIDI",
            value = "26",
            delta = -1,
            delta_color = "inverse",
        )
        
    with col2:
        st.metric(
            label = "SAIFI",
            value = "0.2",
            delta = 0.02,
            delta_color = "inverse",
        )
        
    with col3:
        st.metric(
            label = "CAIDI",
            value = "100",
            delta = 3,
            delta_color = "inverse",
        )
        
        
modifications = {

    'input_id': 'listener_test',
    'html' : '<input id="listener_test" value="test" /><button id="submit-button">Submit</button>',
    'javascript' : """
    window.parent.addEventListener('message', function(event){
        if(event.data.type === "area_selection"){
            console.log('Got parent event');
            console.log(event.data);
            event.data.type = "passed_area";
            sendDataToPython({
            value: event.data,
            dataType: "json",
            });
        }
    });
    """,
    'css' :  "display: none;"
}




message_listener = create_component(component_name="listener", modifications=modifications)
map_neighborhood_value = message_listener()
if isinstance(map_neighborhood_value, dict) and map_neighborhood_value.get('value', '') != '':
    
    if map_neighborhood_value['value'] != st.session_state.neighborhood:
        print(f"Component returned: {map_neighborhood_value['value']} while the session value is {st.session_state.neighborhood}")
        
        st.session_state.neighborhood = map_neighborhood_value['value']
        st.rerun()

