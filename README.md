# Fuzzy Irrigation

This project is a **Fuzzy Logic-based** agricultural tool designed to help farmers determine the optimal irrigation duration for their crops. It processes imprecise environmental data (Temperature, Humidity, Soil Moisture) to calculate a precise watering time.

## Project Structure

This repository contains two versions of the system:

1. **`app.py` (Interactive Interface):**
* A web-based dashboard built with **Streamlit**.
* Features a "Manual Mode" to test specific scenarios (sliders).
* Features a "Simulation Mode" to generate random daily weather conditions.
* Visualizes rule strengths and final decisions in real-time.


2. **`fuzzy.py` (Command-Line Simulation):**
* A pure Python script for backend testing.
* Runs a 10-interval simulation automatically.
* Prints a detailed data trace to the terminal, showing exactly how fuzzy values (Low/Medium/High) are aggregated.



## Logic Overview

The system uses a **Mamdani-style Fuzzy Inference System**:

**Inputs:**
* **Temperature (°C):** Mapped to *Optimal* or *Hot*.
* **Humidity (%):** Mapped to *Low* or *High*.
* **Soil Moisture (%):** Mapped to *Dry*, *Moist*, or *Wet*.


**Rules:**
* **High Water:** If Soil is Dry **AND** (Temp is Hot **OR** Humidity is Low).
* **Medium Water:** If Soil is Moist **AND** (Temp is Optimal **OR** Humidity is Optimal).
* **Low Water:** If Soil is Wet **OR** Humidity is High **OR** Temp is Cold.


**Output:**
* **Duration (mins):** Calculated using the **Weighted Average** defuzzification method.



## Installation

You need **Python 3.x** installed. The only external requirement is the Streamlit library for the interface.

```bash
pip install streamlit

```

## How to Run

### 1. Run the Interactive Dashboard

To use the visual interface:

```bash
streamlit run app.py

```

*This will automatically open the tool in your web browser (usually at http://localhost:8501).*

### 2. Run the Command-Line Simulation

To see the raw data trace in your terminal:

```bash
python fuzzy.py

```

*(Note: Ensure your backend script is named `fuzzy.py`)*
