import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("heart_disease.csv")

# Map the numeric values to descriptive labels
df['sex'] = df['sex'].map({1: 'Male', 0: 'Female'})
df['cp'] = df['cp'].map({0: 'Typical Angina', 1: 'Atypical Angina', 2: 'Non-Anginal Pain', 3: 'Asymptomatic'})
df['fbs'] = df['fbs'].map({1: 'Fasting Blood Sugar > 120 mg/dl', 0: 'Fasting Blood Sugar <= 120 mg/dl'})
df['restecg'] = df['restecg'].map({0: 'Normal', 1: 'ST-T Wave Abnormality', 2: 'Left Ventricular Hypertrophy'})
df['exang'] = df['exang'].map({1: 'Yes', 0: 'No'})
df['thal'] = df['thal'].map({0: 'Normal', 1: 'Fixed Defect', 2: 'Reversible Defect'})

# Function to calculate cardiovascular score (example implementation)
def calculate_cardio_score(row):
    score = (row['age'] / 100) + (row['chol'] / 300) + (row['trestbps'] / 200) + (row['thalach'] / 200)
    return score

df['cardio_score'] = df.apply(calculate_cardio_score, axis=1)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(style={'backgroundColor': '#eaf0f1', 'padding': '20px', 'margin': '0px'}, children=[
    html.H1("Heart Disease Analysis Dashboard", style={'textAlign': 'center', 'color': '#34495e', 'marginBottom': '20px'}),

    # Filters Row
    html.Div([
        html.Div([
            html.Label('Select Age Range', style={'fontSize': '18px', 'color': '#2c3e50'}),
            dcc.RangeSlider(
                id='age-slider',
                min=df['age'].min(),
                max=df['age'].max(),
                value=[df['age'].min(), df['age'].max()],
                marks={int(i): str(int(i)) for i in range(int(df['age'].min()), int(df['age'].max())+1, 10)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px'}),

        html.Div([
            html.Label('Select Gender', style={'fontSize': '18px', 'color': '#2c3e50'}),
            dcc.Dropdown(
                id='gender-dropdown',
                options=[{'label': 'Male', 'value': 'Male'}, {'label': 'Female', 'value': 'Female'}],
                value=['Male', 'Female'],
                multi=True,
                style={'backgroundColor': '#ffffff', 'color': '#2c3e50'}
            )
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px'}),

        html.Div([
            html.Label('Select Chest Pain Type', style={'fontSize': '18px', 'color': '#2c3e50'}),
            dcc.Dropdown(
                id='cp-dropdown',
                options=[{'label': cp, 'value': cp} for cp in df['cp'].unique()],
                value=df['cp'].unique().tolist(),
                multi=True,
                style={'backgroundColor': '#ffffff', 'color': '#2c3e50'}
            )
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    # Key Metrics Row
    html.Div([
        html.Div(id='metric-1', style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'}),
        html.Div(id='metric-2', style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'}),
        html.Div(id='metric-3', style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'textAlign': 'center'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px', 'marginBottom': '20px'}),

    # Compact Layout - Plots without Spaces
    html.Div([
        html.Div([
            dcc.Graph(id='box-plot', config={'displayModeBar': False}, style={'height': '400px'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='violin-plot', config={'displayModeBar': False}, style={'height': '400px'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'padding-left': '-70px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='scatter-plot', config={'displayModeBar': False}, style={'height': '400px'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),

    html.Div([
        html.Div([
            dcc.Graph(id='regression-plot', config={'displayModeBar': False}, style={'height': '400px'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='pie-chart', config={'displayModeBar': False}, style={'height': '400px'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        html.Div([
            dcc.Graph(id='treemap', config={'displayModeBar': False}, style={'height': '400px'})
        ], style={'width': '32%', 'display': 'inline-block', 'padding': '10px', 'margin': '10px', 'backgroundColor': '#ffffff', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'})
])

# Callbacks for Interactive Components
@app.callback(
    [Output('box-plot', 'figure'),
     Output('violin-plot', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('regression-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('treemap', 'figure'),
     Output('metric-1', 'children'),
     Output('metric-2', 'children'),
     Output('metric-3', 'children')],
    [Input('age-slider', 'value'),
     Input('gender-dropdown', 'value'),
     Input('cp-dropdown', 'value')]
)
def update_plots(age_range, genders, chest_pain_types):
    # Filter DataFrame based on input
    filtered_df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1]) & 
                     (df['sex'].isin(genders)) & (df['cp'].isin(chest_pain_types))]

    # Key Metrics
    avg_cholesterol = filtered_df['chol'].mean()
    median_cholesterol = filtered_df['chol'].median()
    avg_trestbps = filtered_df['trestbps'].mean()
    median_trestbps = filtered_df['trestbps'].median()
    avg_thalach = filtered_df['thalach'].mean()
    median_thalach = filtered_df['thalach'].median()

    high_bp_percentage = (filtered_df['trestbps'] > 120).mean() * 100
    avg_cardio_score = filtered_df['cardio_score'].mean()

    metric_1 = f"Avg Cholesterol: {avg_cholesterol:.2f} mg/dl (Median: {median_cholesterol:.2f})"
    metric_2 = f"Avg Resting BP: {avg_trestbps:.2f} mm Hg (Median: {median_trestbps:.2f})"
    metric_3 = f"Avg Max HR: {avg_thalach:.2f} bpm (Median: {median_thalach:.2f})\nHigh BP: {high_bp_percentage:.2f}%"

    # Box Plot - Cholesterol Levels by Age
    box_plot = px.box(filtered_df, x='age', y='chol', color='sex',
                      title='Cholesterol Levels by Age and Gender',
                      labels={'chol': 'Cholesterol Level', 'age': 'Age'},
                      color_discrete_sequence=['#3498db', '#e74c3c'])

    # Violin Plot - Cholesterol Levels by Chest Pain Type
    violin_plot = px.violin(filtered_df, y='chol', x='cp', color='sex',
                            title='Cholesterol Levels by Chest Pain and Gender',
                            labels={'chol': 'Cholesterol Level', 'cp': 'Chest Pain Type'},
                            box=True, points='all',
                            color_discrete_sequence=['#3498db', '#e74c3c'])

    # Scatter Plot - Age vs Cholesterol
    scatter_plot = px.scatter(filtered_df, x='age', y='chol', color='sex',
                              title='Age vs Cholesterol by Gender',
                              labels={'chol': 'Cholesterol Level', 'age': 'Age'},
                              color_discrete_sequence=['#3498db', '#e74c3c'])

    # Regression Plot
    regression_plot = px.scatter(filtered_df, x='age', y='chol', trendline='ols',
                                 title='Regression of Age vs Cholesterol',
                                 labels={'chol': 'Cholesterol Level', 'age': 'Age'},
                                 color_discrete_sequence=['#3498db'])

    # Pie Chart - Distribution of Chest Pain Types
    pie_chart = px.pie(filtered_df, names='cp', title='Distribution of Chest Pain Types',
                       color_discrete_sequence=px.colors.sequential.Plasma)

    # Treemap - Chest Pain Type by Cholesterol
    treemap = px.treemap(filtered_df, path=['cp', 'sex'], values='chol', 
                         title='Treemap of Cholesterol by Chest Pain Type and Gender',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
    treemap.update_layout(
        title=dict(
            text='Treemap of Cholesterol by Chest Pain Type and Gender',
            font_size=15,
            xanchor='center',
            x=0.5
        ),
        title_x=0.5,
        title_y=0.95,
        margin=dict(t=90, b=10, l=10, r=10)
    )

    return box_plot, violin_plot, scatter_plot, regression_plot, pie_chart, treemap, metric_1, metric_2, metric_3

# Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8080, debug=True)
