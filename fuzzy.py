# Fuzzy Logic System
import random

# Triangular Membership Function
def get_membership (x, a, b, c):
    """
    Calculates triangular membership.
    x: The input value
    a: Start of the triangle
    b: Peak of the triangle 
    c: End of the triangle
    """
    # Outside the triangle
    if x <= a or x >= c:
        return 0.0
    # Rising slope
    elif a < x <= b:
        return (x - a) / (b - a)
    # Falling slope
    elif b < x < c:
        return (c - x) / (c - b)
    else:
        return 0.0
    
# Input Sensor Class
class Sensor:
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.moisture = 0

    def get_data(self):
        # Simulate random environmental changes
        self.temperature = random.uniform(0, 50)
        self.humidity = random.uniform(0, 100)
        self.moisture = random.uniform(0, 100)

# Initialize sensor
sensor = Sensor()

# Fuzzification Inputs
# Temp (°C)
temp_cold = (0, 0, 18) # Start, Peak, End
temp_optimal = (16, 22, 28)
temp_hot  = (26, 32, 40)

# Humidity (%)
humidity_low    = (0, 0, 50)
humidity_optimal = (40, 60, 80)
humidity_high    = (70, 100, 100)

# Soil moisture (%)
soil_dry   = (0, 0, 40)
soil_moist = (30, 50, 70)
soil_wet   = (60, 100, 100)

# Output: Irrigation Duration (Minutes)
water_low    = (0, 10, 20)
water_medium = (15, 30, 45)
water_high   = (40, 60, 60)

# Fuzzy Rules
def compute_watering_duration(temp, humidity, moisture):
    """
    Takes crisp inputs, applies fuzzy rules, 
    and returns aggregated strengths for High, Medium, and Low watering.
    """
    
    # FUZZIFICATION
    # Calculate membership for Inputs
    # * operator unpacks the tuples
    
    # Temperature Scores
    t_hot_score     = get_membership(temp, *temp_hot)
    t_optimal_score = get_membership(temp, *temp_optimal)
    # t_cold_score   = get_membership(temp, *temp_cold)  # Not used in rules
    
    # Humidity Scores
    h_low_score     = get_membership(humidity, *humidity_low)
    h_high_score    = get_membership(humidity, *humidity_high)
    # h_optimal_score= get_membership(humidity, *humidity_optimal)  # Not used in rules
    
    # Soil Scores
    s_dry_score     = get_membership(moisture, *soil_dry)
    s_moist_score   = get_membership(moisture, *soil_moist)
    s_wet_score     = get_membership(moisture, *soil_wet)

    # Rules
    
    # HIGH WATERING
    # IF Soil is Dry AND (Temp is Hot OR Humidity is Low)
    rule_high_strength = min(s_dry_score, max(t_hot_score, h_low_score))
    
    # MEDIUM WATERING
    # IF Soil is Moist AND Temp is Optimal
    rule_medium_strength = min(s_moist_score, t_optimal_score)
    
    # LOW WATERING
    # IF Soil is Wet OR Humidity is High
    rule_low_strength = max(s_wet_score, h_high_score)

    # Return firing strength
    return rule_low_strength, rule_medium_strength, rule_high_strength

# Defuzzification
def defuzzify(low_strength, med_strength, high_strength):
    """
    Converts the three fuzzy rule strengths into a single crisp value (minutes).
    Uses the Weighted Average method based on the peaks of the output triangles.
    """
    # Define the 'Center' (Peak) of each output triangle
    center_low = 10
    center_medium = 30
    center_high = 60

    # Weighted numerator
    numerator = (
        (low_strength * center_low) +
        (med_strength * center_medium) +
        (high_strength * center_high)
    )
    
    # Total strength (denominator)
    total_strength = low_strength + med_strength + high_strength

    # Return result
    if total_strength == 0:
        return 0.0
    
    return numerator / total_strength

# Main Simulation Loop
if __name__ == "__main__":
    print("Starting Fuzzy Logic Irrigation Simulation")
    print(f"{'Interval':<10} | {'Temp':<6} | {'Humid':<6} | {'Moist':<6} || {'Low':<4} {'Med':<4} {'High':<4} || {'Result':<10}")
    print("-" * 75)

    # Run for 10 intervals to simulate time passing
    for i in range(1, 11):
        # Get new random sensor readings
        sensor.get_data()
        t = sensor.temperature
        h = sensor.humidity
        m = sensor.moisture

        # Compute Fuzzy Rule Strengths
        low, med, high = compute_watering_duration(t, h, m)

        # Defuzzify to get final minutes
        final_minutes = defuzzify(low, med, high)

        # Print the trace
        print(f"Interval {i:<2}| {t:<6.1f} | {h:<6.1f} | {m:<6.1f} || "
              f"{low:<.2f} {med:<.2f} {high:<.2f} || {final_minutes:.1f} mins")