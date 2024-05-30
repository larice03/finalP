
'''"""Name: Lily Rice
This program CS230: Section 1
Data: Bridges in Georgia
Description: 
This program contains data pertaining to bridges in the state of Georgia. This program visualizes this data through a pie chart of most popular materials, a map displaying structure number and average daily traffic, and a bar graph displaying the most heavily trafficked (on average) bridges in Georgia.  
""'''
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk

@st.cache_data
def load_data():#loads data from file into dataframe
    df = pd.read_csv('GeorgiaBridges.csv', header=0)
    return df

@st.cache_data
def top_cities_chart(df):
    st.title("Top 20 Bridges by Highest Daily Traffic")

    # Selecting top 20 bridges with the highest values from column K (avg daily traffic)
    top_bridges = df.nlargest(20, '29 - Average Daily Traffic')[
        ['1 - State Name', '8 - Structure Number', '29 - Average Daily Traffic']].dropna()

    # Renaming columns for clarity
    top_bridges = top_bridges.rename(columns={'1 - State Name': 'State Name', '8 - Structure Number': 'Structure Number',
                                            '29 - Average Daily Traffic': 'Value'})

    # Filtering out zero or non-number values
    top_bridges = top_bridges[top_bridges['Value'] != 0]

    # Convert Structure Number to string format
    top_bridges['Structure Number'] = top_bridges['Structure Number'].astype(str)

    # Plotting the top bridges as a bar graph
    fig, ax = plt.subplots()
    ax.bar(top_bridges['Structure Number'], top_bridges['Value'], color='red', edgecolor='black')
    ax.set_xlabel('Structure Number')
    ax.set_ylabel('Value')
    ax.set_title('Top 20 Bridges by Highest Value')
    ax.grid(True)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90)

    # Display the bar graph
    st.pyplot(fig)

@st.cache_data
def map_page(df, num_coordinates):
    st.title("Map of Top Bridges") #name of streamlit page
    st.write("Column Names:"), df.columns #prints column names

    # Selecting top bridges with the highest traffic based on the selected number of coordinates
    top_bridges = df.nlargest(num_coordinates, '29 - Average Daily Traffic').dropna(
        subset=['latitude', 'longitude'])

    # Renaming latitude and longitude columns
    top_bridges = top_bridges.rename(
        columns={'16 - latitude (decimal)': 'latitude', '17 - longitude (decimal)': 'longitude'})
    st.write("Renamed Columns:",df.columns)

    # Filtering out zero or non-number values
    top_bridges = top_bridges[top_bridges['29 - Average Daily Traffic'] != 0]

    # Create a pydeck scatterplot layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=top_bridges,
        get_position=["longitude", "latitude"],
        get_color=[255, 0, 0, 160],
        get_radius=1000,  # Sets the size of the points
        pickable=True  # Allow  points to be interactive
    )

    # Set the initial view state when user opens map
    view_state = pdk.ViewState(
        latitude=top_bridges['latitude'].mean(),
        longitude=top_bridges['longitude'].mean(),
        zoom=4 #zoom level
    )

    # Create the pydeck map
    map_ = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Bridge ID: {8 - Structure Number}\nTraffic: {29 - Average Daily Traffic}"}
    )

    # Render the pydeck map
    st.pydeck_chart(map_)

@st.cache_data
def popular_materials_chart(df):
    st.title("Most Popular Materials")

    # Selecting the column '43A - Main Span Material' and get value counts
    material_counts = df['43A - Main Span Material'].value_counts()

    # Get the top 6 most common materials
    top_materials = material_counts.head(6)

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(top_materials, labels=top_materials.index, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    st.pyplot(plt)

def main():
    df = load_data()

    # Add tabs for navigation
    st.sidebar.title('Navigation')
    page = st.sidebar.radio("Go to", ('Home', 'Top Cities Chart', 'Map', 'Most Popular Materials'))

    # Display selected page
    if page == 'Home':
        st.title(" Georgia Bridge Traffic Analysis")
        st.write("Welcome to the Bridge Traffic Analysis Dashboard! Here you can view data on bridges within Georgia")
        st.write("Use the tabs on the left to navigate between different pages.")
    elif page == 'Top Cities Chart':
        top_cities_chart(df)
    elif page == 'Map':
        num_coordinates = st.slider("Number of Coordinates", min_value=1, max_value=1000, value=20)
        map_page(df, num_coordinates)
    elif page == 'Most Popular Materials':
        popular_materials_chart(df)

if __name__ == "__main__":
    main()
    