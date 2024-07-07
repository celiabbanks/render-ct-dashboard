# Working code with all predictive visualizations

# predictive_visualizations.py

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import ct_data_extraction

# Extract data
df = ct_data_extraction.extract_data()

# Optimize data types
df['Completed'] = df['Overall Status'].apply(lambda x: 1 if x == 'COMPLETED' else 0).astype('int8')

# Drop columns not useful for modeling
df_cleaned = df.drop(columns=['NCT ID', 'Acronym', 'Start Date', 'Primary Completion Date', 'Study First Post Date', 'Last Update Post Date', 'Overall Status'])

# Encode categorical variables
df_encoded = pd.get_dummies(df_cleaned, columns=['Conditions', 'Interventions', 'Locations', 'Study Type', 'Phases'], drop_first=True)

# Handle missing values by filling them with a placeholder (e.g., -1)
df_encoded.fillna(-1, inplace=True)

# Define features and target
X = df_encoded.drop(columns=['Completed'])  # Drop the target column from features
y = df_encoded['Completed']  # Target column indicating whether the trial is completed

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model with fewer estimators
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Confusion Matrix with Annotations
cm = confusion_matrix(y_test, y_pred)
cm_fig = px.imshow(cm, text_auto=True, labels=dict(x="Predicted", y="Actual"),
                   title="Confusion Matrix",
                   color_continuous_scale='Blues')

cm_fig.update_layout(
    title={
        'text': "Confusion Matrix for Clinical Trials Completion Prediction",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    annotations=[go.layout.Annotation(
        text='The confusion matrix visualizes the performance of the classification model in predicting whether clinical trials are completed.',
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.25,
        bordercolor='black',
        borderwidth=1
    )],
    margin=dict(b=120)  # Adjust bottom margin to avoid overlap
)

# Classification Report with Detailed Metrics
report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()
report_fig = px.bar(report_df, x=report_df.index, y='f1-score', title="Classification Report (F1-Scores)")

report_fig.update_layout(
    title={
        'text': "Classification Report for Clinical Trials Completion Prediction",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    annotations=[go.layout.Annotation(
        text='The bar chart represents the F1-scores for each class, indicating the balance between precision and recall.',
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.25,
        bordercolor='black',
        borderwidth=1
    )],
    margin=dict(b=120)  # Adjust bottom margin to avoid overlap
)

# Feature Importance calculation
importances = model.feature_importances_
feature_names = X_train.columns

# Create a DataFrame for better plotting
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importances
})

# Sort by importance and select top N features
N = 10  # Number of top features to plot
top_importance_df = importance_df.sort_values(by='Importance', ascending=False).head(N)

# Plotly Bar plot for interactive visualization
feature_fig = go.Figure()
feature_fig.add_trace(go.Bar(
    x=top_importance_df['Feature'],
    y=top_importance_df['Importance'],
    text=top_importance_df['Importance'].round(3),  # Add importance values as text
    textposition='auto',
    marker_color='lightskyblue'
))

feature_fig.update_layout(
    title={
        'text': "Feature Importance for Clinical Trials Completion Prediction",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    annotations=[go.layout.Annotation(
        text='The bar chart shows the importance of top 10 features in predicting completion of clinical trials.',
        align='center',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.5,
        y=1.15,  # Move annotation under the title
        bordercolor='black',
        borderwidth=1
    )],
    xaxis_title="Feature",
    yaxis_title="Importance",
    margin=dict(b=120, l=200),  # Adjust bottom and left margins to avoid overlap
    xaxis=dict(
        tickangle=45,  # Rotate x-axis labels
        tickfont=dict(size=10)  # Adjust font size
    ),
    yaxis=dict(
        tickfont=dict(size=10)  # Adjust font size
    )
)

# Display the enhanced visualizations
cm_fig.show()
report_fig.show()
feature_fig.show()
