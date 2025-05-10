import pandas as pd
import plotly.express as px
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
from umap import UMAP
import matplotlib.pyplot as plt
import seaborn as sns

sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

data = pd.read_csv("metaculus_open_questions.csv")
docs = data['title'].tolist()
print(f"Loaded {len(docs)} documents.")
embeddings = sentence_model.encode(docs, show_progress_bar=False)

topic_model = BERTopic().fit(docs, embeddings)
topic_model.visualize_documents(docs, embeddings=embeddings)

reduced_embeddings = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
fig = topic_model.visualize_documents(docs, reduced_embeddings=reduced_embeddings)

# --- Styling for Helvetica, white bg, no axes / ticks / grid ---
fig.update_layout(
    font=dict(family="Helvetica", size=16),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title=None,
    yaxis_title=None
)
fig.update_xaxes(visible=False, showgrid=False, zeroline=False, showticklabels=False)
fig.update_yaxes(visible=False, showgrid=False, zeroline=False, showticklabels=False)

fig.show()

emb = pd.DataFrame(reduced_embeddings)

emb.columns = ['umap_1', 'umap_2']
data_emb = pd.concat([data.reset_index(drop=True), emb], axis=1)

data_emb.columns

data_emb['main_cat'] = data_emb['category_descriptions'].apply(lambda x: x.split(';')[0] if pd.notnull(x) else x)

import plotly.express as px

fig = px.scatter(
    data_emb,
    x='umap_1',
    y='umap_2',
    color='main_cat',
    opacity=0.7,
    color_discrete_sequence=px.colors.qualitative.T10
)

# Custom hover: show title and category only, no axis numbers or variable labels
custom = data_emb[['title', 'main_cat']].to_numpy()
fig.update_traces(
    customdata=custom,
    hovertemplate="%{customdata[0]}"
)

fig.update_layout(
    font=dict(family="Helvetica", size=16),
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis_title=None,
    yaxis_title=None
)
fig.update_xaxes(visible=False, showgrid=False, zeroline=False, showticklabels=False)
fig.update_yaxes(visible=False, showgrid=False, zeroline=False, showticklabels=False)

fig.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
fig.update_layout(
    title="2D UMAP Embeddings Colored by Category",
    legend_title_text='Category'
)
fig.write_html("metaculus_topics.html", full_html=True, include_plotlyjs="cdn")
fig.show() 