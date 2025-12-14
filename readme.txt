Hi, this is Mihir Apte CS7DS4 / CSU44065 student number : 25334927
This repository contains my submission for A3 of the Data Visualization module.  
The goal of this assignment is to design and implement a novel, complex visualization artefact that effectively communicates insights from a multivariate dataset.

---

How to Run (Step-by-Step)
1. Open a terminal in the project folder
Navigate to the directory that contains a3_ritik.py.

You should see: - a3.py - Global_Mobile_Prices_2025_Extended.csv - requirements.txt

2. Create and activate a virtual environment (recommended)
macOS / Linux bash python3 -m venv venv source venv/bin/activate

Windows (PowerShell) python -m venv venv venv\Scripts\Activate.ps1

3. Install required dependencies
pip install -r requirements.txt

4. Run the dashboard application
python a3.py

5. Open the dashboard in your browser
http://127.0.0.1:8050/


-----

Dataset

The dataset used in this project is **Global_Mobile_Prices_2025_Extended.csv**, which contains information about smartphones released in 2025 across multiple brands.

### Attributes include:
- Brand and model
- Price (USD)
- RAM and storage
- Camera resolution
- Battery capacity
- Display size
- Charging speed
- 5G support
- Operating system
- Processor
- User rating
- Release month and year


Visualization Design

- Interactive Scatter Plot
  Used to explore relationships between price and other attributes such as RAM, camera, battery, and rating.

- Scatterplot Matrix (SPLOM)
  A reduced multivariate view showing relationships between key attributes (price, RAM, camera, battery, rating) while avoiding visual clutter.

- Faceted Scatter Plot (Small Multiples)
  Shows price versus rating, split by brand, allowing easy comparison across manufacturers.

- Static Temporal Line Chart
  Displays average smartphone prices across release months, providing insight into temporal trends without animation complexity.




Libraries to download
- Python
- Pandas 
- Plotly Express 
- Plotly Dash 


Thankyou for executing Assignment 3!




