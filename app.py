import streamlit as st
import pandas as pd
import plotly.express as px

# Page Layout and Design Enhancements
st.set_page_config(page_title="Educational Levels in Lebanon", layout="wide")

# Custom CSS for background and font styles
st.markdown(
    """
    <style>
    .main {
        background-image: url('https://images.unsplash.com/photo-1585431599340-e5bc3f0d189a');
        background-size: cover;
        background-color: rgba(255, 255, 255, 0.8);
        background-blend-mode: lighten;
    }
    h1, h2 {
        color: #2E86C1;
        font-family: 'Arial', sans-serif;
    }
    .stPlotlyChart {
        background-color: #f0f8ff;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)

# App Title
st.title("📘 Educational Levels by Town in Lebanon")

# Description of the app
st.write("""
This interactive app allows you to explore the educational levels across various towns in Lebanon. 
You can select multiple towns and educational levels to visualize the data in both bar charts and heatmaps. 
Understanding these trends can provide insights into regional disparities in education.
""")

# Load the dataset
data = pd.read_csv('educational levels.csv')
cleaned_data = data.dropna()

# --------- Bar Chart Section ---------
st.header("📊 Comparing Educational Levels Across Selected Towns")
st.write("""
This bar chart compares the educational levels of residents in the selected towns. 
Select multiple towns and educational levels to explore how educational attainment varies across regions.
""")

# Create a multiselect for towns for the bar chart
towns_bar = cleaned_data['Town'].unique()
selected_towns_bar = st.multiselect('Select one or more towns for the bar chart', towns_bar, key='town_select_bar')

# Create a multiselect for educational levels for the bar chart
education_levels_dict = {
    'Illiterate': 'PercentageofEducationlevelofresidents-illeterate',
    'School Dropout': 'PercentageofSchooldropout',
    'University': 'PercentageofEducationlevelofresidents-university',
    'Secondary': 'PercentageofEducationlevelofresidents-secondary',
    'Intermediate': 'PercentageofEducationlevelofresidents-intermediate',
    'Vocational': 'PercentageofEducationlevelofresidents-vocational',
    'Elementary': 'PercentageofEducationlevelofresidents-elementary',
    'Higher Education': 'PercentageofEducationlevelofresidents-highereducation'
}
selected_levels_bar = st.multiselect('Select one or more educational levels for the bar chart', list(education_levels_dict.keys()), key='level_select_bar')

# Prepare data for the bar chart
comparison_data_bar = []
for town in selected_towns_bar:
    filtered_data = cleaned_data[cleaned_data['Town'] == town]
    for level in selected_levels_bar:
        percentage_value = filtered_data[education_levels_dict[level]].values[0]
        comparison_data_bar.append({'Town': town, 'Education Level': level, 'Percentage': percentage_value})

comparison_df_bar = pd.DataFrame(comparison_data_bar)

# Display bar chart
if not comparison_df_bar.empty:
    fig_bar = px.bar(comparison_df_bar, x='Education Level', y='Percentage', color='Town', barmode='group',
                     title='Comparison of Educational Levels Across Selected Towns')
    st.plotly_chart(fig_bar)
else:
    st.write("Please select both towns and educational levels to see the comparison.")

st.divider()  # Divider for a cleaner layout

# --------- Heatmap Section ---------
st.header("🌡️ Heatmap of Educational Levels by Town")
st.write("""
This heatmap shows the intensity of educational levels across different towns. 
You can use it to visually compare educational levels and see patterns across regions.
""")

# Create a multiselect for towns for the heatmap
towns_heatmap = cleaned_data['Town'].unique()
selected_towns_heatmap = st.multiselect('Select one or more towns for the heatmap', towns_heatmap, key='town_select_heatmap')

# Create a multiselect for educational levels for the heatmap
selected_levels_heatmap = st.multiselect('Select one or more educational levels for the heatmap', list(education_levels_dict.keys()), key='level_select_heatmap')

# Prepare data for the heatmap
comparison_data_heatmap = []
for town in selected_towns_heatmap:
    filtered_data = cleaned_data[cleaned_data['Town'] == town]
    town_data = {'Town': town}
    for level in selected_levels_heatmap:
        town_data[level] = filtered_data[education_levels_dict[level]].values[0]
    comparison_data_heatmap.append(town_data)

comparison_df_heatmap = pd.DataFrame(comparison_data_heatmap)

# Pivot the DataFrame to create a matrix suitable for a heatmap
if not comparison_df_heatmap.empty:
    heatmap_data = comparison_df_heatmap.set_index('Town').T
    fig_heatmap = px.imshow(heatmap_data, labels=dict(x="Town", y="Educational Level", color="Percentage"),
                            title="Educational Levels Heatmap")

    # Display heatmap
    st.plotly_chart(fig_heatmap)
else:
    st.write("Please select both towns and educational levels to see the heatmap.")

st.divider()

# Footer Section with additional insights
st.write("""
**Insights**: 
Lebanon has a diverse educational landscape, with towns in some regions showing a high percentage of residents with higher education, while others have a larger proportion of illiterate or primary-level educated individuals. 
This data highlights the regional educational disparities and offers a glimpse into areas that may need further development and support.
""")
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
