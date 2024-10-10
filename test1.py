import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    # Load your dataset here, adjust the path or source accordingly
    df = pd.read_csv('fish_data.csv')
    return df

# Set up navigation bar
st.sidebar.title("Navigation")
nav_option = st.sidebar.radio("Go to", ['Introduction', 'Data Exploration', 'Conclusion'])

# Introduction Section
if nav_option == 'Introduction':
    st.title("Interactive Fish Species Data Exploration")
    st.markdown("""
    ### Introduction
    This interactive app allows users to explore a comprehensive dataset of various fish species, sourced from Kaggle.com, 
    by analyzing their physical characteristics such as length, weight, and weight-to-length ratio. Through descriptive statistics
    and dynamic visualizations, users can uncover patterns in the data, such as correlations between fish weight and length, while filtering 
    by species. The purpose of exploring this dataset is to better understand the relationships between physical attributes of fish, which 
    can reveal trends in fish growth, health, and species diversity. This analysis can aid in ecological studies and inform fishery management decisions.
    """)

# Data Exploration Section (Key Descriptive Statistics)
elif nav_option == 'Data Exploration':
    st.title("Data Exploration and Key Statistics")
    
    # Load data
    df = load_data()

    st.write("### Dataset Preview")
    st.write(df.head())
    
    # Descriptive statistics
    st.write("### Descriptive Statistics")
    st.write(df.describe())
    
    # Allow users to filter species
    st.sidebar.subheader("Filter Data")
    species = st.sidebar.multiselect("Select Fish Species", options=df['species'].unique(), default=df['species'].unique())
    df_filtered = df[df['species'].isin(species)]
    
    st.write("### Filtered Dataset Preview")
    st.write(df_filtered.head())

# Visualizations Section

    st.title("Visualizations")

    # User-selected variable for further analysis
    df = load_data()
    st.sidebar.subheader("Explore Variables")
    variable = st.sidebar.selectbox("Select a variable to explore:", options=['length', 'weight', 'w_l_ratio'])

    # User-selected range for variable
    min_value = float(df_filtered[variable].min())
    max_value = float(df_filtered[variable].max())
    range_slider = st.sidebar.slider(f"Select range for {variable}:",
                                     min_value=min_value, max_value=max_value,
                                     value=(min_value, max_value))
    
    # Filter data based on slider range
    df_variable_filtered = df_filtered[(df_filtered[variable] >= range_slider[0]) & (df_filtered[variable] <= range_slider[1])]
    
    # Histogram of selected variable
    st.subheader(f"Distribution of {variable.capitalize()}")
    fig, ax = plt.subplots()
    sns.histplot(df_variable_filtered[variable], kde=True, bins=10, ax=ax)
    ax.set_title(f"Histogram of {variable.capitalize()}")
    st.pyplot(fig)

    # Boxplot for Fish Weight
    st.subheader("Fish Weight Distribution")
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=df_filtered, y='weight', ax=ax2)
    ax2.set_title("Boxplot of Fish Weight")
    st.pyplot(fig2)

    # Scatter plot for Weight vs Length
    if st.sidebar.checkbox("Show Scatter Plot for Weight vs Length"):
        st.subheader("Scatter Plot of Weight vs Length")
        fig3, ax3 = plt.subplots()
    
    
        sns.scatterplot(data=df_filtered, x='length', y='weight', hue='species', ax=ax3)
    
        ax3.set_title("Scatter Plot: Weight vs Length (Filtered by Species)")
        st.pyplot(fig3)

    # Correlation 
    if st.sidebar.checkbox("Show Correlation Heatmap"):
        st.subheader("Correlation Heatmap")
        corr_matrix = df_filtered.select_dtypes(include=[np.number]).corr()
        fig4, ax4 = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax4)
        ax4.set_title("Correlation Heatmap")
        st.pyplot(fig4)


elif nav_option == 'Conclusion':
    st.title("Conclusion")
    st.markdown("""
    ## Summary and Conclusion
    From our exploration of the fish species dataset, several key insights emerge. 
    There is a clear relationship between fish length and weight, indicating that 
    as fish grow in size, their weight increases in a predictable manner. The 
    distribution of the weight-to-length ratio across different species reveals 
    potential biological differences that may be linked to species-specific growth 
    patterns or ecological niches. The visualizations also highlight outliers and 
    variations within certain species, suggesting that factors such as age, 
    environment, or genetic diversity might influence fish characteristics. Overall, 
    these findings provide valuable information for fisheries management and ecological 
    studies, allowing researchers and policymakers to better understand fish populations 
    and support species conservation efforts.
    
    
    """)
