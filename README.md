# 🍽️ Restaurant Map & Analytics Dashboard  
### A Full-Stack Interactive Data Visualization Project using Flask, Python, Plotly & Leaflet.js

---

## 📊 Project Overview  
This project is a **full-stack Restaurant Analytics Dashboard** built using **Flask**, **Leaflet.js**, **Plotly**, and **Python**.  
It provides an interactive map-based interface with dynamic restaurant markers, filter controls, and visually appealing analytics charts for India and Global regions.

Designed with real-world data cleaning, backend processing, and frontend visualization in mind — this project demonstrates a complete data engineering + visualization workflow.

---

## 🚀 Key Features

### 🌍 **1. Interactive World Map (Leaflet.js + MarkerCluster)**
- Dynamic loading of restaurant points  
- Smooth clustering that expands on zoom  
- Clean popups with:
  - Restaurant name  
  - City  
  - Cuisine  
  - Rating  
  - Votes  
  - Address  

### 🔎 **2. Real-Time Filters**
- Filter restaurants by:
  - **City**
  - **Cuisine**
- Dynamic refresh of map markers  
- Reset button included for user convenience  

### 📈 **3. Professional Analytics Dashboard (Plotly)**
Separate analytical views for:

#### 🇮🇳 **India Insights**
- Top Cities by:
  - Number of Restaurants  
  - Average Rating  
  - Cuisine Variety  

#### 🌍 **Global Insights**
- Same 3 charts for worldwide top cities  

All charts use:
- Vertical bar charts  
- Responsive layout  
- Clean labels & styling  

### 🧹 **4. Advanced Data Cleaning**
Includes automatic correction of corrupted UTF-8 text in dataset:


Cleaning powered by:
- `ftfy`  
- Manual correction mapping  
- Unicode normalization (NFC)

### 🧩 **5. Modular Architecture**
This project follows a scalable structure:

Task_4/
│── app.py
│── requirements.txt
│── Dataset.csv
│
├── templates/
│ └── index.html
│
├── static/
│ ├── styles.css
│ └── script.js
│
└── visualizations/
├── chart_generator.py
└── city_stats.py

Each component has a dedicated responsibility:
- **Backend** → Flask routes, chart data, map data  
- **Visualization Engine** → Plotly chart generator  
- **Geographic Engine** → Leaflet map + clusters  
- **Cleaning Engine** → city_stats with fix_text processing  

---

## 🛠️ Tech Stack

### **Backend**
- Flask  
- Python  
- Pandas  
- Numpy  

### **Frontend**
- HTML5  
- CSS3  
- JavaScript  

### **Visualizations**
- Plotly  
- Leaflet.js  
- Leaflet MarkerCluster  

### **Utilities**
- FTFY (Unicode text repair)  
- Matplotlib (optional)  

---

## 📥 Installation & Setup

### **1. Clone the Repository**

git clone https://github.com/YOUR_USERNAME/Restaurant-Map-Analytics.git
cd Restaurant-Map-Analytics
Create a Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Run the Flask App
python app.py

5. Open in Browser
http://127.0.0.1:5000/
