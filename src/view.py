# app.py
import streamlit as st

import main as m
import dic as dic
import os
import matplotlib.pyplot as plt
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


st.title("Job Matcher Pro")
st.write("Upload a PDF file to view magic.")
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
# Sample data
labels = []
sizes = []

# Define a function to load GloVe vectors into a dictionary
def load_glove_vectors(glove_file):
    with open(glove_file, 'r', encoding='utf-8') as f:
        glove_model = {}
        for line in f:
            parts = line.split()
            word = parts[0]
            vector = np.array(parts[1:], dtype=np.float32)
            glove_model[word] = vector
    return glove_model


# Define a function to convert a sentence to GloVe embeddings
def sentence_to_glove(sentence, model, dim=100, aggregate='mean'):
    words = sentence.split()
    embeddings = []
    for word in words:
        if word in model:
            embeddings.append(model[word])
        else:
            embeddings.append(np.zeros(dim))  # If word not in vocabulary, use zero vector

    if embeddings:
        if aggregate == 'mean':
            return np.mean(embeddings, axis=0)
        elif aggregate == 'sum':
            return np.sum(embeddings, axis=0)
        else:
            raise ValueError("Unsupported aggregation method. Use 'mean' or 'sum'.")
    else:
        return np.zeros(dim)  # Return zero vector if no embeddings found
    



def vizu():
    skills=[]
    with open('./data/processed/skills.txt', 'r',encoding='utf-8') as f:
        skills=f.readlines()
    data=[]
    for i in skills:
        data.append(i.strip())

    st.write(data)


    print("loading embeddings")
    glove_model = load_glove_vectors('./glove.6B.100d.txt')
    # dic
    emb2=[]
    print("inside loop")
    for i in data:
      x=sentence_to_glove(i, glove_model)
      emb2.append(x)
    emb2=np.mean(emb2,axis=0)
    # emb2
    
    # st.write(emb2)
    
    # Calculate cosine similarity
    result={}
    for i in dic.dic:
      similarity_score = cosine_similarity(emb2.reshape(1, -1),dic.dic[i].reshape(1, -1))[0][0]
      result[i]=similarity_score
    sorted_dict = dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
    st.write(sorted_dict )
    data=sorted_dict
    # Data for pie chart
    labels = list(data.keys())
    sizes = list(data.values())
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Title
    ax.set_title('Industry Distribution')
    # Display the pie chart in Streamlit
    st.title('Industry Distribution Pie Chart')
    st.pyplot(fig)



if uploaded_file is not None:
    
    m.interface_test(uploaded_file)
    print("button clicked")
    skills=[]
    with open('./data/processed/skills.txt', 'r',encoding='utf-8') as f:
        skills=f.readlines()
    data=[]
    for i in skills:
        data.append(i.strip())

    print(data)
    data=m.segrigation(data)
    data=eval(data)
    sorted_dict = dict(sorted(data.items(), key=lambda item: len(item[1]),reverse=True))
    st.write(sorted_dict )
    data= dict(list(sorted_dict.items())[:5])
    print(data)
    print(type(data))
    labels = []
    sizes = []
    for i in data:
        labels.append(i)
        sizes.append(len(data[i]))
    


    
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Title
    ax.set_title('Industry Distribution')
    # Display the pie chart in Streamlit
    st.title('Industry Distribution Pie Chart')
    st.pyplot(fig)

    uploaded_file = None


if st.button('vizu'):
    vizu()

if st.button('Generate Pie Chart'):
    print("button clicked")
    skills=[]
    with open('./data/processed/skills.txt', 'r',encoding='utf-8') as f:
        skills=f.readlines()
    data=[]
    for i in skills:
        data.append(i.strip())

    print(data)
    data=m.segrigation(data)
    data=eval(data)
    sorted_dict = dict(sorted(data.items(), key=lambda item: len(item[1]),reverse=True))
    st.write(sorted_dict )
    data= dict(list(sorted_dict.items())[:5])
    print(data)
    print(type(data))
    labels = []
    sizes = []
    for i in data:
        labels.append(i)
        sizes.append(len(data[i]))
    


    
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Title
    ax.set_title('Industry Distribution')
    # Display the pie chart in Streamlit
    st.title('Industry Distribution Pie Chart')
    st.pyplot(fig)