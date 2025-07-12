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

# --- Average Salary by Unit (Static Bar Chart) ---
st.subheader("🟢 Average Salary by Unit")
salary_by_unit = data.groupby('UNIT')['SALARY'].mean().sort_values(ascending=False).reset_index()
fig_unit = px.bar(
    salary_by_unit,
    x='UNIT',
    y='SALARY',
    color='UNIT',
    title='Average Salary by Unit',
    width=700,
    height=400
)
fig_unit.update_layout(showlegend=False, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(fig_unit) 

# --- Salary Distribution by Unit (Boxplot) ---
st.subheader("🟣 Salary Distribution by Unit (Boxplot)")
if 'UNIT' in data.columns:
    fig_box_unit, ax_box_unit = plt.subplots(figsize=(7, 3.5))
    data.boxplot(column='SALARY', by='UNIT', ax=ax_box_unit, grid=False, patch_artist=True,
                 boxprops=dict(facecolor='#43C59E', color='#6C47FF'))
    ax_box_unit.set_title('Salary by Unit')
    ax_box_unit.set_xlabel('Unit')
    ax_box_unit.set_ylabel('Salary')
    plt.suptitle('')
    st.pyplot(fig_box_unit)
else:
    st.info('Unit data not available for boxplot.')

# --- Median Salary by Designation (Bar Chart) ---
st.subheader("🟤 Median Salary by Designation")
if 'DESIGNATION' in data.columns:
    med_salary_des = data.groupby('DESIGNATION')['SALARY'].median().sort_values(ascending=False).reset_index()
    fig_med_des = px.bar(med_salary_des, x='DESIGNATION', y='SALARY', color='SALARY',
                        color_continuous_scale='Blues', width=700, height=350,
                        title='Median Salary by Designation')
    fig_med_des.update_layout(margin=dict(l=10, r=10, t=40, b=10), xaxis_title='Designation', yaxis_title='Median Salary')
    st.plotly_chart(fig_med_des)
else:
    st.info('Designation data not available for median salary chart.')

# --- Employee Count by Experience Bucket (Bar Chart) ---
st.subheader("🟢 Employee Count by Experience Bucket")
if 'PAST EXP' in data.columns:
    bins = [0, 2, 5, 10, 20, 50]
    labels = ['0-2', '3-5', '6-10', '11-20', '20+']
    data['EXP_BUCKET'] = pd.cut(data['PAST EXP'], bins=bins, labels=labels, right=False)
    exp_count = data['EXP_BUCKET'].value_counts().sort_index().reset_index()
    exp_count.columns = ['Experience Bucket', 'Count']
    fig_exp_count = px.bar(exp_count, x='Experience Bucket', y='Count', color='Count', width=700, height=350, color_continuous_scale='Viridis')
    fig_exp_count.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_exp_count)
else:
    st.info('Experience data not available for experience bucket chart.')

# --- Salary vs. Experience (Line, by Unit) ---
st.subheader("🔵 Salary vs. Experience (Line, by Unit)")
if 'PAST EXP' in data.columns and 'UNIT' in data.columns:
    exp_unit = data.groupby(['PAST EXP', 'UNIT'])['SALARY'].mean().reset_index()
    fig_exp_unit = px.line(exp_unit, x='PAST EXP', y='SALARY', color='UNIT', width=700, height=350,
                          labels={'PAST EXP': 'Years of Experience', 'SALARY': 'Avg Salary'},
                          title='Average Salary vs. Experience by Unit')
    fig_exp_unit.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_exp_unit)
else:
    st.info('Experience or unit data not available for salary vs. experience chart.')

# --- Gender Pay Gap by Unit (Bar) ---
st.subheader("🟠 Gender Pay Gap by Unit")
if 'UNIT' in data.columns and 'SEX' in data.columns:
    paygap = data.groupby(['UNIT', 'SEX'])['SALARY'].mean().unstack()
    paygap['Gap'] = paygap.max(axis=1) - paygap.min(axis=1)
    paygap = paygap.sort_values('Gap', ascending=False)
    fig_paygap = px.bar(paygap.reset_index(), x='UNIT', y=paygap.columns[:-1], barmode='group',
                       width=700, height=350, title='Average Salary by Gender and Unit')
    fig_paygap.update_layout(margin=dict(l=10, r=10, t=40, b=10), yaxis_title='Avg Salary')
    st.plotly_chart(fig_paygap)
else:
    st.info('Unit or gender data not available for pay gap chart.')

# --- Top 10 Highest Paid Employees (Table) ---
st.subheader("🔴 Top 10 Highest Paid Employees")
top10 = data.sort_values('SALARY', ascending=False).head(10)
st.dataframe(top10.reset_index(drop=True))

# --- Correlation Heatmap ---
st.subheader("🟡 Correlation Heatmap")
numeric_cols = data.select_dtypes(include='number')
if numeric_cols.shape[1] > 1:
    corr = numeric_cols.corr()
    fig_corr, ax_corr = plt.subplots(figsize=(6, 4))
    im = ax_corr.imshow(corr, cmap='coolwarm', interpolation='nearest')
    ax_corr.set_xticks(range(len(corr.columns)))
    ax_corr.set_yticks(range(len(corr.columns)))
    ax_corr.set_xticklabels(corr.columns, rotation=45, ha='right')
    ax_corr.set_yticklabels(corr.columns)
    plt.colorbar(im, ax=ax_corr, fraction=0.046, pad=0.04)
    ax_corr.set_title('Correlation Heatmap')
    st.pyplot(fig_corr)
else:
    st.info('Not enough numeric data for correlation heatmap.') 

# NOTE: All Plotly charts are now extra small for compact laptop display: width=400, height=250 