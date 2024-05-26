import streamlit as st
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# Import your modules
import main as m
import dic
from fpdf import FPDF
import networkx as nx
load_dotenv(".env")
EMAIL=os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")
# Streamlit Page Config (must be the first Streamlit command)
# st.set_page_config(page_title="Job Matcher Pro", page_icon=":briefcase:", layout="wide")

# Set Title and Description
st.title("LLM-POWERED RESUME PARSING AND INFORMATION RETRIEVAL")

# Apply some CSS to style the app


# Email input
email = st.text_input("Enter your email address")

# File Uploader
uploaded_file = st.file_uploader("Upload Single PDF", type=["pdf"])

# Function to load GloVe vectors
@st.cache_data
def load_glove_vectors(glove_file):
    with open(glove_file, 'r', encoding='utf-8') as f:
        glove_model = {}
        for line in f:
            parts = line.split()
            word = parts[0]
            vector = np.array(parts[1:], dtype=np.float32)
            glove_model[word] = vector
    return glove_model

# Function to convert a sentence to GloVe embeddings
def sentence_to_glove(sentence, model, dim=100, aggregate='mean'):
    words = sentence.split()
    embeddings = [model[word] if word in model else np.zeros(dim) for word in words]

    if embeddings:
        if aggregate == 'mean':
            return np.mean(embeddings, axis=0)
        elif aggregate == 'sum':
            return np.sum(embeddings, axis=0)
        else:
            raise ValueError("Unsupported aggregation method. Use 'mean' or 'sum'.")
    else:
        return np.zeros(dim)

# Visualization Function
def visualize_data():

    # Step 1: Generate the pie chart and save as an image
    
    # colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
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
    MAIN_SKILLS = sorted_dict
    data= dict(list(sorted_dict.items())[:5])
    print(data)
    print(type(data))
    labels = []
    sizes = []
    for i in data:
        labels.append(i)
        sizes.append(len(data[i]))


    plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    pie_chart_path = 'pie_chart.png'
    plt.savefig(pie_chart_path)
    plt.close()
    print("Pie chart saved")

    # Step 2: Create a dummy knowledge graph and save as an image
    G = nx.Graph()
    edges=[]
    for i in data:
        for j in data[i]:
            edges.append((i,j))
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)
    # plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=9)
    knowledge_graph_path = 'knowledge_graph.png'
    plt.savefig(knowledge_graph_path)
    plt.close()

    # Step 3: Create a PDF and add the pie chart and knowledge graph images
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Report with Charts and Graphs', 0, 1, 'C')

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()

    # Add some introductory text
    pdf.set_font('Arial', 'B', 14)
    # pdf.cell(0, 10, 'Introduction', 0, 1)
    pdf.set_font('Arial', '', 12)
    # main_skills_text = '\n'.join([f"{skill}: {level}" for skill, level in MAIN_SKILLS.items()])
    pdf.multi_cell(0, 10, 'This report presents a pie chart and a knowledge graph that represent various data distributions and relationships. These visualizations are useful for quick analysis and decision-making.')


    # Add some space before the pie chart image
    pdf.ln(10)

    # Add the pie chart image to the PDF
    pdf.image(pie_chart_path, x=10, y=40, w=pdf.w - 20)

   
    # Add some space before the knowledge graph image
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Knowledge Graph', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, 'The following knowledge graph represents the relationships between different nodes. This graph helps in understanding the connections and interdependencies among various entities.')

    # Add the knowledge graph image to the PDF
    pdf.ln(10)
    pdf.image(knowledge_graph_path, x=10, y=40, w=pdf.w - 20)

    # Save the PDF to a file
    pdf_output_path = 'report_with_charts_and_graph.pdf'
    pdf.output(pdf_output_path)

    print(f'PDF saved to {pdf_output_path}')
    return pdf_output_path

# Function to send email
def send_email(receiver_email, results):
    print("Sending email...")
    msg = MIMEMultipart()
    msg['Subject'] = 'Resume Report'
    msg['From'] = EMAIL
    msg['To'] = receiver_email
    global INPUT_PATH

    try:
        with open(results, "rb") as f:
            img_data = f.read()
        image = MIMEImage(img_data, name=os.path.basename(results),_subtype="png")
        msg.attach(image)

        

        with open("Input_Resume.pdf", "rb") as f:
            img_data = f.read()
        image = MIMEImage(img_data, name="Input_Resume.pdf",_subtype="png")
        msg.attach(image)

        with open('./data/processed/skills.txt', "rb") as f:
            img_data = f.read()
        image = MIMEImage(img_data, name="skills.txt",_subtype="png")
        msg.attach(image)

        with open('./data/processed/result.json', "rb") as f:
            img_data = f.read()
        image = MIMEImage(img_data, name="result.json",_subtype="png")
        msg.attach(image)


    except Exception as e:
        print("Error attaching image:", e)


    text = MIMEText("Report with Charts and Graphs attached.")
    msg.attach(text)
    # image = MIMEImage(img_data, name=os.path.basename(results))
    # msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login( EMAIL, PASSWORD)
    s.sendmail( EMAIL, receiver_email, msg.as_string())
    s.quit()
    print("Mail Sent")

# Background processing function
def process_data(uploaded_file, email):
    print("Processing data...")
    m.interface_test(uploaded_file)
    sorted_results = visualize_data()
    send_email(email, sorted_results)

# Main app logic
if uploaded_file is not None and email:
    # os.save("Input_Resume.pdf", uploaded_file)
    save_path = os.path.join("./", "Input_Resume.pdf")

    # Save the uploaded file to the specified location
    with open(save_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    threading.Thread(target=process_data, args=(uploaded_file, email)).start()
    st.success("File uploaded successfully! You will receive an email with the results shortly.")
    uploaded_file = None



from zipfile import ZipFile
# Allow single ZIP file upload
uploaded_filesss = st.file_uploader("Upload a ZIP file of your folder", type="zip")
if uploaded_filesss and email:
        folder_name = "extracted_files/"
        os.makedirs(folder_name, exist_ok=True)  # Ensure the folder exists

        with ZipFile(uploaded_filesss) as z:
            st.write("Files in the ZIP:")
            for file_info in z.infolist():
                st.write(file_info.filename)
                # process_data(folder_name+file_info.filename, "singhharjas2002@gmail.com")
                threading.Thread(target=process_data, args=(folder_name+file_info.filename, email)).start()
        st.success("File uploaded successfully! You will receive an email with the results shortly.")