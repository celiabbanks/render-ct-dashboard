# Simple plot
# Study Type Histogram-2

import pandas as pd
import plotly.express as px

# Make sure that the clinical trial extraction code is run
# and 'df' is the DataFrame containing clinical trial data
import ct_data_extraction

# Call the extract_data function from data_extraction module
df = ct_data_extraction.extract_data()

# Assuming df_cleaned is available from the predictive analytics code
# df_study = df_cleaned  # Rename df_cleaned to df_study for clarity

# Assuming df is the original dataset before cleaning
df_study = df.copy()  # Make a copy of df for clarity

# Check unique values in the 'Phases' column
valid_phases = df_study['Phases'].dropna().unique()  # Get unique non-NA values in Phases column
df_study = df_study[df_study['Phases'].isin(valid_phases)]  # Filter out rows with unwanted values

# Visualization: Status of Study Type by Phase (excluding 'NA' and other unwanted values)
fig_hist2 = px.histogram(
    df_study,
    x='Phases',
    color='Overall Status',
    facet_col='Study Type',  # Use facet_col to display Study Type as columns
    category_orders={'Phases': sorted(valid_phases, reverse=False)},  # Use filtered valid phases for sorting
    title="Status of Study Type by Phase",
    barmode='group',
    color_discrete_map={'COMPLETED': '#1f77b4', 'UNKNOWN': '#ff7f0e', 'TERMINATED': '#2ca02c', 'WITHDRAWN': '#d62728'}
)

fig_hist2.update_layout(
    yaxis_title="Count",
    legend_title="Overall Status",
)

# Remove the repetitive 'Phases' label from x-axis
fig_hist2.update_xaxes(title_text='', showticklabels=True)

fig_hist2.show()