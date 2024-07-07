# Individual simple plots...

# Study Type Histogram-1

import pandas as pd
import plotly.express as px


# Make sure that the clinical trial extraction code is run
# and 'df' is the DataFrame containing clinical trial data
import ct_data_extraction

# Call the extract_data function from data_extraction module
df = ct_data_extraction.extract_data()

# Assuming df_cleaned is available from the predictive analytics code
# df_study = df_cleaned  # Rename df_cleaned to df_study for clarity

df_study = df.copy()

# Check unique values in the 'Phases' column
unique_phases = df_study['Phases'].unique()
print(unique_phases)

# Filter out rows where 'Phases' column contains 'NA' or any other unwanted values
valid_phases = df_study['Phases'].dropna().unique()  # Get unique non-NA values in Phases column
df_study = df_study[df_study['Phases'].isin(valid_phases)]  # Filter out rows with unwanted values

# Visualization: Status of Study Type by Phase (excluding 'NA' and other unwanted values)
fig_hist1 = px.histogram(
    df_study,
    x='Phases',
    color='Study Type',
    category_orders={'Phases': sorted(valid_phases, reverse=False)},  # Use filtered valid phases for sorting
    title="Count of Study Type by Phase",
    barmode='group'
)

fig_hist1.update_layout(
    xaxis_title="Phases",
    yaxis_title="Count",
    legend_title="Study Type"
)

fig_hist1.show()