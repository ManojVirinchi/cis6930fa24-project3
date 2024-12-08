import gradio as gr
import pandas as pd
import numpy as np
from src.req import fetch_pdf_from_url, extract_incident_data
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import datetime

sns.set_theme()

import datetime

def process_input(url_input, file_input):
    url_timestamp = None
    file_timestamp = None
    all_incident_data = []
    
    if url_input:
        url_timestamp = datetime.datetime.now()
        urls = [url.strip() for url in url_input.split(',')]
    
    if file_input is not None and file_input.name != "":
        file_timestamp = file_input.timestamp if hasattr(file_input, 'timestamp') else datetime.datetime.now()
    
    if url_timestamp and file_timestamp:
        if file_timestamp > url_timestamp:
            if isinstance(file_input, str):
                with open(file_input, 'rb') as f:
                    pdf_file = BytesIO(f.read())
            else:
                pdf_file = BytesIO(file_input.read())
            incident_data = extract_incident_data(pdf_file)
            all_incident_data.extend(incident_data)
        else:
            for url in urls:
                pdf_file = fetch_pdf_from_url(url)
                incident_data = extract_incident_data(pdf_file)
                all_incident_data.extend(incident_data)
    elif file_timestamp:
        if isinstance(file_input, str):
            with open(file_input, 'rb') as f:
                pdf_file = BytesIO(f.read())
        else:
            pdf_file = BytesIO(file_input.read())
        incident_data = extract_incident_data(pdf_file)
        all_incident_data.extend(incident_data)
    elif url_timestamp:
        for url in urls:
            pdf_file = fetch_pdf_from_url(url)
            incident_data = extract_incident_data(pdf_file)
            all_incident_data.extend(incident_data)
    else:
        raise ValueError("No input provided")
    
    df = pd.DataFrame(all_incident_data)
    
    cluster_fig = create_cluster_plot(df)
    bar_fig = create_bar_plot(df)
    heatmap_fig = create_heatmap(df)
    pie_fig = create_pie_chart(df)
    
    return cluster_fig, bar_fig, heatmap_fig, pie_fig

def create_cluster_plot(df):
    incident_counts = df.groupby(['nature', 'incident_ori']).size().reset_index(name='count')
    
    X = pd.get_dummies(incident_counts[['nature', 'incident_ori']])
    X['count'] = incident_counts['count']
    
    n_clusters = min(5, len(X))
    wcss = []
    for i in range(1, n_clusters+1):
        kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    
    elbow = next(i for i, v in enumerate(wcss) if v - wcss[i+1] < wcss[i-1] - v)
    
    kmeans = KMeans(n_clusters=elbow, random_state=42)
    incident_counts['Cluster'] = kmeans.fit_predict(X)
    
    fig, ax = plt.subplots(figsize=(30, 15), facecolor='black')
    ax.set_facecolor('black')
    
    scatter = sns.scatterplot(
        data=incident_counts,
        x='nature',
        y='incident_ori',
        hue='Cluster',
        size='count',
        sizes=(40, 400),
        palette='viridis',
        alpha=0.7,
        ax=ax
    )
    
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right', fontsize=12, color='white')
    ax.set_yticklabels(ax.get_yticklabels(), color='white')
    ax.set_title('Incident Clusters by Nature and ORI', pad=20, fontsize=20, color='white')
    ax.set_xlabel('Nature of Incident', labelpad=15, fontsize=16, color='white')
    ax.set_ylabel('Incident ORI', labelpad=15, fontsize=16, color='white')
    
   
    ax.yaxis.grid(True, color='gray', linestyle='--', alpha=0.5)
    
    
    ax.xaxis.grid(False)
    
    for spine in ax.spines.values():
        spine.set_visible(False)
    

    legend = ax.get_legend()
    if legend:
        legend.set_frame_on(False)
        for text in legend.get_texts():
            text.set_color('white')
    
    for idx, row in incident_counts.iterrows():
        ax.text(
            x=row['nature'],
            y=row['incident_ori'],
            s=str(row['count']),
            ha='center',
            va='center',
            fontsize=10,
            color='white',
            fontweight='bold'
        )
    
    plt.tight_layout()
    return fig

def create_bar_plot(df):
    fig, ax = plt.subplots(figsize=(20, 10), facecolor='black')
    ax.set_facecolor('black')
    
    ori_counts = df['incident_ori'].value_counts().head(10)
    bars = ori_counts.plot(kind='bar', ax=ax, color=plt.cm.Set3(np.linspace(0, 1, 10)))
    
    ax.set_title('Bar graph', fontsize=16, color='white')
    ax.set_xlabel('Incident ORI', fontsize=12, color='white')
    ax.set_ylabel('Count', fontsize=12, color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    
    for i, v in enumerate(ori_counts):
        ax.text(i, v, str(v), ha='center', va='bottom', color='white')
    
    plt.tight_layout()
    return fig

def create_heatmap(df):
    fig, ax = plt.subplots(figsize=(20, 12), facecolor='black')
    ax.set_facecolor('black')
    
    top_natures = df['nature'].value_counts().nlargest(10).index
    top_locations = df['location'].value_counts().nlargest(10).index
    
    heatmap_data = pd.pivot_table(
        df[df['nature'].isin(top_natures) & df['location'].isin(top_locations)],
        values='incident_number',
        index='location',
        columns='nature',
        aggfunc='count',
        fill_value=0
    )
    
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', linewidths=0.5, ax=ax, cbar_kws={'label': 'Count'})
    
    ax.set_title('Heatmap of Top 10 Incident Types by Top 10 Locations', fontsize=16, color='white')
    ax.set_xlabel('Incident Type', fontsize=12, color='white')
    ax.set_ylabel('Location', fontsize=12, color='white')
    ax.tick_params(axis='x', rotation=45, colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.tight_layout()
    return fig

def create_pie_chart(df):
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='black')
    ax.set_facecolor('black')
    
    nature_counts = df['nature'].value_counts().nlargest(10)
    other_count = df['nature'].value_counts().sum() - nature_counts.sum()
    
    if other_count > 0:
        nature_counts['Other'] = other_count
    
    colors = plt.cm.Spectral(np.linspace(0, 1, len(nature_counts)))
    wedges, texts, autotexts = ax.pie(nature_counts.values, labels=nature_counts.index, autopct='%1.1f%%', 
                                      startangle=90, colors=colors, wedgeprops=dict(width=0.6))
    
    for text in texts + autotexts:
        text.set_color('white')
    
    ax.set_title('Top 10 Incident Types Distribution', fontsize=16, color='white')
    
    plt.tight_layout()
    return fig

with gr.Blocks(css="""
    .gradio-container {
        background-color: #000000;
    }
    .gr-button {
        background-color: #4CAF50;
        border: none;
        color: white;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
        padding: 10px 24px;
    }
    .gr-button:hover {
        background-color: #45a049;
    }
""") as demo:
    gr.Markdown("# NormanPD Incident Data Visualizer")
    
    with gr.Row():
        url_input = gr.Textbox(label="Enter PDF URL")
        file_input = gr.File(label="Or upload file ", file_types=[".pdf"])
        process_button = gr.Button("Process PDF")
    
    cluster_plot = gr.Plot(label="Incident Clusters")
    bar_plot = gr.Plot(label="Incident ORI count")
    heatmap_plot = gr.Plot(label="Incident Types by Location Heatmap")
    pie_plot = gr.Plot(label="Incident Type Distribution")
    
    process_button.click(
        fn=process_input,
        inputs=[url_input, file_input],
        outputs=[cluster_plot, bar_plot, heatmap_plot, pie_plot]
    )

if __name__ == "__main__":
    demo.launch(server_port=5003)