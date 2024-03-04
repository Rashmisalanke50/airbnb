import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
import pandas as pd
import os
from PIL import Image
import warnings
import plotly.figure_factory as ff

warnings.filterwarnings('ignore')
st.set_page_config(page_title = "Airbnb-Analysis by Rashmi N", page_icon=":world_map:", layout="wide")

st.title(":world_map: Airbnb Exploration")
st.markdown('<style>h1 { text-align: center; font-size: 50px; } .block-container { padding-left: 1rem; }</style>', unsafe_allow_html=True)

#contact page
#file_path = r"C:\Users\rashm\OneDrive\Desktop\streamlit\Datas\DCM_0864.JPG"
#Description = "This project uses MongoDB Atlas to analyze Airbnb data, focusing on cleaning, geospatial visualization, and dynamic plotting for insights into pricing, availability, and location trends"

#Headbar settings
select = option_menu(
    menu_title=None,
    options=[".", "|", "*",],
    icons=["house", "bar-chart", "envelope"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding":"01important", "background-color": "grey", "size": "cover", "width": "100"},
            "icon": {"font-size": "25px"},
            "nav-link": {"font-size": "0.5px", "text-align": "center", "margin": "-2px", "--hover-color": "#000066"},
            "nav-link-selected": {"background-color": "#000066"}})

if select == ".":
    st.write(
        "<div style='font-size: 25px; color: black;'>"
        "Airbnb is an innovative online platform that revolutionizes the way people travel by connecting travelers with hosts who offer a wide array of accommodations. From cozy apartments and traditional houses to one-of-a-kind stays like treehouses and castles, Airbnb provides a diverse range of lodging options to suit every traveler's taste and budget. This global platform empowers travelers to discover unique and personalized stays, allowing them to immerse themselves in local culture and experience destinations like a true insider. At the same time, Airbnb enables hosts to monetize their spaces and share their passion for hospitality with guests from around the world. <br><br>"
        "With millions of listings spanning over 220 countries and regions, Airbnb has become synonymous with accessible and authentic travel experiences. By offering affordable alternatives to traditional hotels and fostering meaningful connections between hosts and guests, Airbnb has truly transformed the way people explore the world."
        "</div>",unsafe_allow_html=True)
    st.write(
    "<div style='font-size: 20px; color: #000066; text-align: center; margin-top: 60px;'>"
    "Unlock insights with our Airbnb Analysis project! 📊🏠 Dive into pricing, availability, and location trends for data-driven travel decisions. 💼✨"
    "</div>", unsafe_allow_html=True)
if select == "|":
    file=st.file_uploader(":floppy_disk: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
    if file is not None:
        filename = file.name
        st.write(filename)
        df=pd.read_csv(file, encoding="ISO-8859-1")
    else:
        file_path= r"C:\Users\rashm\OneDrive\Desktop\streamlit\Datas\final_airbnbdata.csv"
        df=pd.read_csv(file_path, encoding="ISO-8859-1")
    st.sidebar.header("Choose your filter: ")
    #creating a neighbourhood_group
    neighbourhood_group = st.sidebar.multiselect("Pick your neighbourhood_group", df["neighbourhood_group"].unique())
    if not neighbourhood_group:
        df2=df.copy()
    else:
        df2=df[df["neighbourhood_group"].isin(neighbourhood_group)]
    #create for neighbourhood
    neighbourhood = st.sidebar.multiselect("Pick the neighbourhood", df2["neighbourhood"].unique())
    if not neighbourhood:
        df3 = df2.copy()
    else:
        df3 = df2[df2["neighbourhood"].isin(neighbourhood)]

    #Filter the data based on neighbourhood_group, neighbourhood
    if not neighbourhood_group and not neighbourhood:
        filtered_df = df
    elif not neighbourhood:
        filtered_df = df[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif not neighbourhood_group:
        filtered_df = df[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood:
        filtered_df = df3[df["neighbourhood"].isin(neighbourhood)]
    elif neighbourhood_group:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group)]
    elif neighbourhood_group and neighbourhood:
        filtered_df = df3[df["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]
    else:
        filtered_df = df3[df3["neighbourhood_group"].isin(neighbourhood_group) & df3["neighbourhood"].isin(neighbourhood)]

    room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("room_type_ViewData")
        fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]], template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200) 
    with col2:
        st.subheader("neighbour_group_ViewData")
        fig = px.pie(filtered_df, values="price", names="neighbourhood_group", hole=0.5)
        fig.update_traces(text=filtered_df["neighbourhood_group"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True) 

    colm1, colm2 = st.columns((2))
    with colm1:
        with st.expander("room_type wise price"):
            st.write(room_type_df.style.background_gradient(cmap="Blues"))
            csv=room_type_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                            help='Click here to download the data as a CSV file')
    with colm2:
        with st.expander("neighbourhood_group wise price"):
            neighbourhood_group=filtered_df.groupby(by="neighbourhood_group", as_index=False)["price"].sum()
            st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
            csv=neighbourhood_group.to_csv(index=False).encode('utf-8')
            st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                            help='Click here to download the data as a CSV file')
    #Create a scatter plot
    data1=px.scatter(filtered_df, x="neighbourhood_group", y="neighbourhood", color="room_type")
    data1['layout'].update(title="room_type in the neighbourhood and neighbourhood_group wise data using scatter plot",
                        titlefont=dict(size=20), xaxis=dict(title="neighbourhood_group", titlefont=dict(size=20)),
                        yaxis=dict(title="neighbourhood", titlefont=dict(size=20)))
    st.plotly_chart(data1, use_container_width=True)

    #Download original dataset
    csv=df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

    st.subheader(":point_right: neighbourhood_group wise room_type and Minimum stay nights")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["neighbourhood_group", "neighbourhood", "number_of_reviews", "room_type", "price", "minimum_nights", "host_name"]]
        fig=ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)

    #map function for room_type
    # If the dataframe has latitude and longitude
    st.subheader("Airbnb Analysis in Map view")
    df=df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
    st.map(df)

if select == "*":
    col1, col2 = st.columns(2)
    col1.write('<style>div[data-testid="stHorizontalBlock"] { width: 50%; margin: auto; }</style>', unsafe_allow_html=True)
    col2.write('<style>div[data-testid="stHorizontalBlock"] { width: 50%; margin: auto; }</style>', unsafe_allow_html=True)
    with col1:
        image = Image.open(r"C:\Users\rashm\OneDrive\Desktop\streamlit\Datas\DCM_0864.JPG")
        st.image(image, width=300)
    with col2:
        st.markdown(
            "<p style='color: ##000066; font-size: 20px;'>"
            "This project uses MongoDB Atlas to analyze Airbnb data, focusing on cleaning, geospatial visualization, and dynamic plotting for insights into pricing, availability, and location trends"
            "</p>", unsafe_allow_html=True)
        st.subheader("Contact Information:")
        st.markdown(
            "<p style='color: ##000066; font-size: 20px;'>"
            "Rashmi N"
            "</p>", unsafe_allow_html=True)
        st.markdown(
        "<ul style='color: ##000066; font-size: 50px;'>"
        "<li> E-mail: Rashmisalanke50@gmail.com</li>"
        "<li> LinkedIn: <a href='https://www.linkedin.com/in/rashmi50/' style='color: #200000;'>Rashmi N</a></li>"
        "<li> GitHub: <a href='https://github.com/Rashmisalanke50' style='color: #200000;'>Rashmi N</a></li>"
        "</ul>",
        unsafe_allow_html=True)