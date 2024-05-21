import matplotlib.pyplot as plt
from fpdf import FPDF
import networkx as nx

# Step 1: Generate the pie chart and save as an image
labels = ['A', 'B', 'C', 'D']
sizes = [15, 30, 45, 10]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # explode 1st slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
pie_chart_path = 'pie_chart.png'
plt.savefig(pie_chart_path)
plt.close()

# Step 2: Create a dummy knowledge graph and save as an image
G = nx.Graph()
G.add_edges_from([
    ("Node1", "Node2"),
    ("Node1", "Node3"),
    ("Node2", "Node4"),
    ("Node2", "Node5"),
    ("Node3", "Node6"),
    ("Node3", "Node7"),
])

pos = nx.spring_layout(G)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=12, font_weight="bold")
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
pdf.cell(0, 10, 'Introduction', 0, 1)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, 'This report presents a pie chart and a knowledge graph that represent various data distributions and relationships. These visualizations are useful for quick analysis and decision-making.')

# Add some space before the pie chart image
pdf.ln(10)

# Add the pie chart image to the PDF
pdf.image(pie_chart_path, x=10, y=40, w=pdf.w - 20)

# Add some explanatory text below the pie chart
pdf.ln(85)  # Adjust this value based on the image height
pdf.set_font('Arial', 'B', 14)
pdf.cell(0, 10, 'Analysis of Pie Chart', 0, 1)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, 'The pie chart above shows that category C has the highest proportion, followed by category B, A, and D. This distribution indicates that category C is the most significant contributor among the four.')

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
