import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go

st.markdown("""
# 📊 Explore Salary Data
Dive into the salary dataset with interactive charts. Use the sidebar to switch pages.
""")

# --- Lottie Animation Function ---
def load_lottieurl(url):
    import requests
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Lottie Animation URL (e.g., data analysis animation) ---
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_ktwnwv5m.json"
lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json, height=100, key="explore_anim")

# --- Load Data ---
data = pd.read_csv('salary prediction.csv')  # Corrected path to match actual file

# --- Layout: Use columns for side-by-side charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🟠 Employee Count by Designation (Pie Chart)")
    des_count = data['DESIGNATION'].value_counts()
    fig1 = px.pie(names=des_count.index, values=des_count.values, title='', hole=0.3)
    # --- Example for all Plotly pie charts ---
    fig1.update_layout(width=800, height=450)  # Employee Count by Designation (Pie Chart) larger size
    st.plotly_chart(fig1)

with col2:
    st.subheader("🔵 Employee Count by Unit (Pie Chart)")
    unit_count = data['UNIT'].value_counts()
    fig2 = px.pie(names=unit_count.index, values=unit_count.values, title='', hole=0.3)
    # --- Example for all Plotly charts ---
    fig2.update_layout(width=800, height=450)  # Employee Count by Unit (Pie Chart) larger size
    st.plotly_chart(fig2)

# --- Enhanced Animated Bar Chart: Salary by Designation ---
# Animate over both UNIT and SEX if both are present, else fallback

if 'UNIT' in data.columns and 'SEX' in data.columns:
    # Prepare data for animation over UNIT and SEX
    frames = []
    units = data['UNIT'].unique()
    sexes = data['SEX'].unique()
    for unit in units:
        for sex in sexes:
            df = data[(data['UNIT'] == unit) & (data['SEX'] == sex)]
            if not df.empty:
                group = df.groupby('DESIGNATION')['SALARY'].mean().reset_index()
                group = group.sort_values('SALARY', ascending=False)
                frames.append(go.Frame(
                    data=[go.Bar(
                        x=group['DESIGNATION'],
                        y=group['SALARY'],
                        marker_color=group['SALARY'],
                        text=group['SALARY'].round(0),
                        textposition='auto',
                        marker=dict(color=group['SALARY'], colorscale='Viridis'),
                    )],
                    name=f"{unit}-{sex}",
                    layout=go.Layout(title_text=f"Unit: {unit} | Gender: {sex}")
                ))
    # Initial frame
    first = frames[0].data[0]
    fig3 = go.Figure(
        data=[first],
        layout=go.Layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [
                    {'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 900, 'redraw': True}, 'fromcurrent': True}]},
                    {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]}
                ]
            }],
            sliders=[{
                'steps': [
                    {'args': [[f.name], {'frame': {'duration': 900, 'redraw': True}, 'mode': 'immediate'}], 'label': f.name, 'method': 'animate'}
                    for f in frames
                ],
                'transition': {'duration': 400},
                'x': 0.1,
                'len': 0.9
            }],
            xaxis_title='Designation',
            yaxis_title='Average Salary',
            width=800,
            height=450,
            margin=dict(l=10, r=10, t=60, b=10),
        ),
        frames=frames
    )
else:
    # Fallback to previous logic (animate over UNIT or SEX or DESIGNATION)
    if 'UNIT' in data.columns:
        anim_col = 'UNIT'
    elif 'SEX' in data.columns:
        anim_col = 'SEX'
    else:
        anim_col = 'DESIGNATION'
    group = data.groupby([anim_col, 'DESIGNATION'])['SALARY'].mean().reset_index()
    group = group.sort_values([anim_col, 'SALARY'], ascending=[True, False])
    fig3 = px.bar(
        group,
        x='DESIGNATION',
        y='SALARY',
        color='SALARY',
        animation_frame=anim_col,
        range_y=[0, data['SALARY'].max()*1.1],
        width=800,
        height=450,
        color_continuous_scale='Viridis',
        text='SALARY',
        title=f'Animated Salary by Designation (by {anim_col.title()})'
    )
    fig3.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig3.update_layout(
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 900, 'redraw': True}, 'fromcurrent': True}]},
                {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]}
            ]
        }],
        margin=dict(l=10, r=10, t=60, b=10),
        xaxis_title='Designation',
        yaxis_title='Average Salary',
        coloraxis_colorbar=dict(title='Salary'),
    )

# --- Histogram: Salary Distribution ---
st.subheader("🟢 Salary Distribution (Histogram)")
fig4, ax4 = plt.subplots(figsize=(5, 2.8))
ax4.hist(data['SALARY'], bins=20, color='#6C47FF', edgecolor='white', alpha=0.8)
ax4.set_xlabel('Salary')
ax4.set_ylabel('Count')
ax4.set_title('Salary Distribution')
st.pyplot(fig4)

# --- Boxplot: Salary by Gender ---
st.subheader("🟤 Salary by Gender (Boxplot)")
fig5, ax5 = plt.subplots(figsize=(5, 2.8))
data.boxplot(column='SALARY', by='SEX', ax=ax5, grid=False, patch_artist=True, boxprops=dict(facecolor='#FFB300', color='#6C47FF'))
ax5.set_title('Salary by Gender')
ax5.set_xlabel('Gender')
ax5.set_ylabel('Salary')
plt.suptitle('')
st.pyplot(fig5)

# --- Missing Values Overview ---
st.subheader("🟡 Missing Values Overview")
missing = data.isnull().sum()
missing = missing[missing > 0]
if not missing.empty:
    st.dataframe(missing.to_frame('Missing Count').style.background_gradient(cmap='Oranges'))
else:
    st.success('No missing values found!')

# --- Animated Average Salary by Unit (Bar Chart) ---
# Animate over 'SEX' (gender) if available

if 'SEX' in data.columns:
    units = data['UNIT'].unique()
    sexes = data['SEX'].unique()
    frames = []
    for sex in sexes:
        df = data[data['SEX'] == sex]
        group = df.groupby('UNIT')['SALARY'].mean().reset_index()
        group = group.sort_values('SALARY', ascending=True)
        frames.append(go.Frame(
            data=[go.Bar(
                x=group['SALARY'],
                y=group['UNIT'],
                orientation='h',
                marker=dict(color=group['SALARY'], colorscale='Viridis'),
                text=group['SALARY'].round(0),
                textposition='auto',
            )],
            name=str(sex)
        ))
    # Initial data for the first frame
    first_group = data[data['SEX'] == sexes[0]].groupby('UNIT')['SALARY'].mean().reset_index().sort_values('SALARY', ascending=True)
    fig6 = go.Figure(
        data=[go.Bar(
            x=first_group['SALARY'],
            y=first_group['UNIT'],
            orientation='h',
            marker=dict(color=first_group['SALARY'], colorscale='Viridis'),
            text=first_group['SALARY'].round(0),
            textposition='auto',
        )],
        frames=frames
    )
    fig6.update_layout(
        width=800,
        height=450,
        title='Animated Average Salary by Unit (by Gender)',
        updatemenus=[{
            'type': 'buttons',
            'showactive': False,
            'buttons': [
                {'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': 1200, 'redraw': True}, 'fromcurrent': True}]},
                {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]},
            ]
        }],
        sliders=[{
            'steps': [
                {'method': 'animate', 'label': str(sex), 'args': [[str(sex)], {'frame': {'duration': 1200, 'redraw': True}, 'mode': 'immediate'}]} for sex in sexes
            ],
            'transition': {'duration': 400},
            'x': 0.1,
            'len': 0.8
        }],
        margin=dict(l=80, r=20, t=60, b=40),
        yaxis_title='Unit',
        xaxis_title='Average Salary',
        yaxis=dict(tickfont=dict(size=14)),
        xaxis=dict(tickfont=dict(size=14)),
    )
    st.plotly_chart(fig6)
else:
    # Fallback: static bar chart if 'SEX' not available
    st.subheader("🟢 Average Salary by Unit")
    salary_by_unit = data.groupby('UNIT')['SALARY'].mean().sort_values(ascending=False).reset_index()
    fig6 = px.bar(salary_by_unit, x='UNIT', y='SALARY', color='UNIT', title='', width=800, height=450)
    fig6.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig6)

# --- Experience vs. Salary (Scatter Plot) ---
st.subheader("🔴 Experience vs. Salary by Designation")
if 'PAST EXP' in data.columns:
    fig7 = px.scatter(data, x='PAST EXP', y='SALARY', color='DESIGNATION',
                     labels={'PAST EXP': 'Years of Experience', 'SALARY': 'Salary'},
                     width=400, height=250, opacity=0.7)
    fig7.update_layout(margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig7)
else:
    st.info('Experience data not available for scatter plot.')

# --- Salary Distribution by Designation (Boxplot) ---
st.subheader("🟣 Salary Distribution by Designation (Boxplot)")
fig8, ax8 = plt.subplots(figsize=(6, 3.2))
designations = data['DESIGNATION'].unique()
data.boxplot(column='SALARY', by='DESIGNATION', ax=ax8, grid=False, patch_artist=True,
             boxprops=dict(facecolor='#6C47FF', color='#FFB300'))
ax8.set_title('Salary by Designation')
ax8.set_xlabel('Designation')
ax8.set_ylabel('Salary')
plt.suptitle('')
st.pyplot(fig8)

# --- Average Salary by Experience Level (Bar) ---
st.subheader("🟢 Average Salary by Experience Level")
if 'PAST EXP' in data.columns:
    bins = [0, 2, 5, 10, 20, 50]
    labels = ['0-2', '3-5', '6-10', '11-20', '20+']
    data['EXP_BUCKET'] = pd.cut(data['PAST EXP'], bins=bins, labels=labels, right=False)
    exp_salary = data.groupby('EXP_BUCKET')['SALARY'].mean().reset_index()
    fig9 = px.bar(exp_salary, x='EXP_BUCKET', y='SALARY', color='SALARY', width=400, height=250, color_continuous_scale='Viridis')
    fig9.update_layout(margin=dict(l=10, r=10, t=30, b=10), xaxis_title='Experience (Years)', yaxis_title='Avg Salary')
    st.plotly_chart(fig9)
else:
    st.info('Experience data not available for experience-level chart.')

# --- Gender Ratio by Unit (Stacked Bar) ---
st.subheader("🟤 Gender Ratio by Unit (Stacked Bar)")
gender_unit = data.groupby(['UNIT', 'SEX']).size().unstack(fill_value=0)
fig10 = gender_unit.plot(kind='bar', stacked=True, figsize=(6, 3.2), color=['#6C47FF', '#FFB300', '#43C59E'])
plt.title('Gender Ratio by Unit')
plt.xlabel('Unit')
plt.ylabel('Count')
st.pyplot(fig10.get_figure())

# --- Add extra padding at the bottom for laptop screens ---
st.markdown('<div style="height: 2em;"></div>', unsafe_allow_html=True)

# --- All chart sizes and layout are now optimized for laptop screens --- 

# --- Animation Speed Control (Visible at Top) ---
st.markdown('---')
st.markdown('### Animation Controls')
speed_option = st.radio(
    'Select Animation Speed:',
    ['Slow', 'Moderate', 'Fast'],
    index=1,
    horizontal=True
)
if speed_option == 'Slow':
    ANIMATION_FRAME_DURATION = 2500  # ms
    ANIMATION_TRANSITION_DURATION = 1200  # ms
elif speed_option == 'Fast':
    ANIMATION_FRAME_DURATION = 800
    ANIMATION_TRANSITION_DURATION = 300
else:
    ANIMATION_FRAME_DURATION = 1800
    ANIMATION_TRANSITION_DURATION = 800

# --- Animated Salary by Designation ---
# (Use speed variables in update_layout)
fig3.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'buttons': [
            {'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': ANIMATION_FRAME_DURATION, 'redraw': True}, 'fromcurrent': True}]},
            {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]},
        ]
    }],
    sliders=[{
        'steps': [
            {'method': 'animate', 'label': str(frame.name), 'args': [[str(frame.name)], {'frame': {'duration': ANIMATION_FRAME_DURATION, 'redraw': True}, 'mode': 'immediate'}]} for frame in fig3.frames
        ],
        'transition': {'duration': ANIMATION_TRANSITION_DURATION},
        'x': 0.1,
        'len': 0.8
    }],
    xaxis_title='Designation',
    yaxis_title='Average Salary',
    width=800,
    height=450,
    margin=dict(l=10, r=10, t=60, b=10),
)

# --- Animated Average Salary by Unit ---
# (Use speed variables in update_layout)
fig6.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'buttons': [
            {'label': 'Play', 'method': 'animate', 'args': [None, {'frame': {'duration': ANIMATION_FRAME_DURATION, 'redraw': True}, 'fromcurrent': True}]},
            {'label': 'Pause', 'method': 'animate', 'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]},
        ]
    }],
    sliders=[{
        'steps': [
            {'method': 'animate', 'label': str(sex), 'args': [[str(sex)], {'frame': {'duration': ANIMATION_FRAME_DURATION, 'redraw': True}, 'mode': 'immediate'}]} for sex in sexes
        ],
        'transition': {'duration': ANIMATION_TRANSITION_DURATION},
        'x': 0.1,
        'len': 0.8
    }],
    margin=dict(l=80, r=20, t=60, b=40),
    yaxis_title='Unit',
    xaxis_title='Average Salary',
    yaxis=dict(tickfont=dict(size=14)),
    xaxis=dict(tickfont=dict(size=14)),
) 