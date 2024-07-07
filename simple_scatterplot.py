# Individual simple plots...

# Interventions for Conditions scatterplot

import plotly.express as px

# Make sure that the clinical trial extraction code is run
# and 'df' is the DataFrame containing clinical trial data
import ct_data_extraction

# Call the extract_data function from data_extraction module
df = ct_data_extraction.extract_data()

# Assuming df_cleaned is available from the predictive analytics code
# df_interventions = df_cleaned  # Rename df_cleaned to df_interventions for clarity

df_interventions = df.copy()

# Truncate long values for Conditions and Interventions
df_interventions['Conditions_truncated'] = df_interventions['Conditions'].str[:30]  # Truncate to first 30 characters
df_interventions['Interventions_truncated'] = df_interventions['Interventions'].str[:30]  # Truncate to first 30 characters

# Calculate the count of each combination of Conditions, Interventions, and Phases
df_counts = df_interventions.groupby(['Conditions_truncated', 'Interventions_truncated', 'Phases']).size().reset_index(name='Count')

# Create a scatter plot with truncated values and count as marker size
fig_scatter = px.scatter(
    df_counts,
    x='Interventions_truncated',
    y='Conditions_truncated',
    color='Phases',
    size='Count',  # Size of marker based on count
    title="Count of Interventions for Conditions by Phase",
    labels={'Interventions_truncated': 'Interventions (Truncated)', 'Conditions_truncated': 'Conditions (Truncated)', 'Count': 'Count'},
    category_orders={'Phases': sorted(df_interventions['Phases'].unique(), reverse=True)},
    hover_name='Phases'  # Display phase as hover information
)

# Update layout for better visualization
fig_scatter.update_layout(
    xaxis_tickangle=45,  # Rotate x-axis labels by 45 degrees
    xaxis_title="Interventions (Truncated)",
    yaxis_title="Conditions (Truncated)",
    legend_title="Phases"
)

# Show the scatter plot
fig_scatter.show()