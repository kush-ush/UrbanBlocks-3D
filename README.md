# 🏙️ UrbanBlocks 3D – Smart Semantic Zoning Simulator

**UrbanBlocks 3D** is an AI-powered smart city zoning simulator that uses **Genetic Algorithms** and **Explainable AI** to generate optimal urban layouts under zoning constraints. The system aligns with **UN SDG 11** by enabling sustainable, inclusive, and balanced urban planning.

🌐 **Live Demo:** [Click to try the deployed web app](https://urbanblocks-3d.streamlit.app/)

![Zoning Layout Screenshot](output/zoning_map.png)

---

## 🚀 Key Features

- 🧬 Genetic Algorithm-based optimization of zoning layouts  
- 🧠 Explainable AI feedback for each zone decision  
- 📊 Real-time layout scoring with improvement suggestions  
- 🏘️ Supports zoning categories: Residential, Commercial, Green  
- 🖼️ Interactive 2D and 3D visualizations with Plotly & Matplotlib  
- 📝 Export full PDF reports  
- 🧩 Manual override of zones (human-in-the-loop)  

---

## 🧠 How It Works

1. User selects plot grid, zone constraints, and area settings  
2. Genetic Algorithm evolves optimal layouts under constraints  
3. Layout is scored on coherence, access, and zone ratio  
4. Visual + explainable feedback is generated  
5. Final layout can be reviewed, modified, or exported  

---

## 🧰 Tech Stack

| Layer        | Tools                          |
|--------------|--------------------------------|
| Frontend     | Streamlit                      |
| AI Core      | DEAP, NumPy, Pandas            |
| Visualization| Plotly, Matplotlib             |
| Utility      | PDFKit, Explainability Engine  |

---

## 🗂️ Folder Structure

UrbanBlocks-3D/
├── app.py ← Main dashboard
├── zoning_engine.py ← Genetic Algorithm logic
├── utils.py ← Visualization, scoring, explainability
├── requirements.txt
├── /assets/ ← UI icons (optional)
├── /data/ ← Input configs (optional)
├── /output/ ← Zone maps, reports
└── README.md



---

## 📸 Screenshots

<img src="output/zoning_map.png" alt="Sample Zoning Layout" width="650"/>


---


## 📦 Installation

To run locally:

```bash
git clone https://github.com/kush-ush/UrbanBlocks-3D.git
cd UrbanBlocks-3D
pip install -r requirements.txt
streamlit run app.py

``` 
## ✍️ Authors
Kushal S Gowda – (https://github.com/kush-ush) – Lead Developer, Research Author

Kumar Yash – Data Preprocessing/Analyst and UI Designer

## 📝 Citation
If you use this project, please cite:

Kushal S Gowda, Kumar Yash.
UrbanBlocks 3D: A Genetic Algorithm-Based Semantic Zoning System for Smart City Planning, 2025. (Under Review – IEEE)

📬 Contact:
 📧 kushalsgowda.ai23@rvce.edu.in
 🌐 (https://github.com/kush-ush)

 ---
🌍 UN SDG Alignment
✅ Supports UN SDG 11: Sustainable Cities and Communities
Enables planners to design urban zones that are inclusive, accessible, and environmentally balanced.


