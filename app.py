import streamlit as st
import random

# Triangular Membership Function
def get_membership(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0

# Fuzzification Inputs
# Temperature (°C)
temp_hot     = (26, 32, 40)
temp_optimal = (16, 22, 28)
# Humidity (%)
humidity_low  = (0, 0, 50)
humidity_high = (70, 100, 100)
# Soil Moisture (%)
soil_dry   = (0, 0, 40)
soil_moist = (30, 50, 70)
soil_wet   = (60, 100, 100)

# Fuzzy Rules
def compute_watering_duration(temp, humidity, moisture):
    
    # Fuzzify Inputs
    t_hot_score     = get_membership(temp, *temp_hot)
    t_optimal_score = get_membership(temp, *temp_optimal)
    
    h_low_score     = get_membership(humidity, *humidity_low)
    h_high_score    = get_membership(humidity, *humidity_high)
    
    s_dry_score     = get_membership(moisture, *soil_dry)
    s_moist_score   = get_membership(moisture, *soil_moist)
    s_wet_score     = get_membership(moisture, *soil_wet)

    # Apply Rules
    # High Irrigation(Dry Soil AND (Hot Temp OR Low Humidity))
    rule_high = min(s_dry_score, max(t_hot_score, h_low_score))
    
    # Medium Irrigation (Moist Soil AND Optimal Temp)
    rule_med = min(s_moist_score, t_optimal_score)
    
    # Low irrigation(Wet Soil OR High Humidity)
    rule_low = max(s_wet_score, h_high_score)

    return rule_low, rule_med, rule_high

# Defuzzification
def defuzzify(low, med, high):
    center_low, center_med, center_high = 10, 30, 60
    
    numerator = (low * center_low) + (med * center_med) + (high * center_high)
    total_strength = low + med + high
    
    if total_strength == 0: return 0.0
    return numerator / total_strength

# Streamlit Interface
st.set_page_config(page_title="Fuzzy Irrigation", page_icon="💧", layout="centered")

st.title("Fuzzy Irrigation")
st.markdown("This system uses Fuzzy Logic to determine the optimal watering duration based on environmental conditions.")

# Sidebar Controls
st.sidebar.header("Input Settings")
mode = st.sidebar.radio("Select Mode:", ["Manual Input", "Simulate Weather Sensor"])

if mode == "Manual Input":
    st.sidebar.markdown("### Set Conditions Manually")
    t_input = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
    h_input = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 50.0)
    m_input = st.sidebar.slider("Soil Moisture (%)", 0.0, 100.0, 40.0)

else:
    st.sidebar.markdown("### Random Weather Generator")
    if st.sidebar.button("Generate New Conditions"):
        st.session_state['t_sim'] = random.uniform(10, 40)
        st.session_state['h_sim'] = random.uniform(20, 90)
        st.session_state['m_sim'] = random.uniform(10, 80)
    
    # Default if button hasn't been clicked yet
    if 't_sim' not in st.session_state:
        st.session_state['t_sim'] = 25.0
        st.session_state['h_sim'] = 50.0
        st.session_state['m_sim'] = 50.0
        
    t_input = st.session_state['t_sim']
    h_input = st.session_state['h_sim']
    m_input = st.session_state['m_sim']

# Main Display
col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{t_input:.1f} °C")
col2.metric("Humidity", f"{h_input:.1f} %")
col3.metric("Soil Moisture", f"{m_input:.1f} %")

st.divider()

# Run Fuzzy Logic
low_s, med_s, high_s = compute_watering_duration(t_input, h_input, m_input)
final_time = defuzzify(low_s, med_s, high_s)

# --- Display Results ---
st.subheader("System Decision")

# Visualizing strength of each rule
c1, c2, c3 = st.columns(3)
c1.info(f"Low Water Strength: **{low_s:.2f}**")
c2.warning(f"Med Water Strength: **{med_s:.2f}**")
c3.error(f"High Water Strength: **{high_s:.2f}**")

# Final Crisp Output
st.success(f"### Recommended Watering Time: **{final_time:.1f} minutes**")

# Optional: Show 'Why' (Logic Trace)
with st.expander("See Logic Explanation"):
    st.write("The system calculated the membership of your inputs against the fuzzy sets:")
    st.write(f"- **Temperature** was mapped to Hot/Optimal.")
    st.write(f"- **Humidity** was mapped to Low/High.")
    st.write(f"- **Moisture** was mapped to Dry/Moist/Wet.")
    st.write("Then it aggregated the rules (Low/Med/High) and calculated the weighted average center.")