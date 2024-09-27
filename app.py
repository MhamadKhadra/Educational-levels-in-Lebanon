import streamlit as st
import pandas as pd
import plotly.express as px

# App Title
st.title("Educational Levels by Town in Lebanon")

# Description of the app
st.write("""
This app allows you to explore the educational levels across various towns in Lebanon. 
You can select multiple towns and educational levels to visualize the data in both bar charts and heatmaps.
""")

# Load the dataset
data = pd.read_csv('educational levels.csv')
cleaned_data = data.dropna()

# --------- Bar Chart Section ---------
st.header("Comparing Educational Levels Across Selected Towns")
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

# --------- Heatmap Section ---------
st.header("Heatmap of Educational Levels by Town")
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
