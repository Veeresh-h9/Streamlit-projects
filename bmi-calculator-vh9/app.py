import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="BMI Calculator",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .bmi-result {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .underweight { background: #e3f2fd; color: #1976d2; }
    .normal { background: #e8f5e8; color: #2e7d32; }
    .overweight { background: #fff3e0; color: #f57c00; }
    .obese { background: #ffebee; color: #d32f2f; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💪 BMI Calculator & Health Tracker</h1>
    <p>Calculate your Body Mass Index and get personalized health recommendations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for input
with st.sidebar:
    st.header("📊 Your Information")
    
    # Unit selection
    unit_system = st.selectbox(
        "Unit System",
        ["Metric (kg/cm)", "Imperial (lbs/ft)"],
        index=0
    )
    
    # Input fields based on unit system
    if unit_system == "Metric (kg/cm)":
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=300.0, value=175.0, step=0.1)
        height_m = height / 100  # Convert to meters
    else:
        weight_lbs = st.number_input("Weight (lbs)", min_value=2.0, max_value=1100.0, value=154.0, step=0.1)
        feet = st.number_input("Height (feet)", min_value=1, max_value=9, value=5, step=1)
        inches = st.number_input("Height (inches)", min_value=0, max_value=11, value=9, step=1)
        
        # Convert to metric
        weight = weight_lbs * 0.453592  # Convert lbs to kg
        height_m = (feet * 12 + inches) * 0.0254  # Convert to meters
        height = height_m * 100  # Convert to cm for display
    
    # Additional info
    age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    activity_level = st.selectbox(
        "Activity Level",
        ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
    )

# Calculate BMI
if height_m > 0:
    bmi = weight / (height_m ** 2)
    
    # BMI categories
    def get_bmi_category(bmi):
        if bmi < 18.5:
            return "Underweight", "underweight"
        elif 18.5 <= bmi < 25:
            return "Normal Weight", "normal"
        elif 25 <= bmi < 30:
            return "Overweight", "overweight"
        else:
            return "Obese", "obese"
    
    category, css_class = get_bmi_category(bmi)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="bmi-result {css_class}">
            BMI: {bmi:.1f}<br>
            <small>{category}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # BMI gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = bmi,
            title = {'text': "BMI Scale"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 40]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 18.5], 'color': "lightblue"},
                    {'range': [18.5, 25], 'color': "lightgreen"},
                    {'range': [25, 30], 'color': "yellow"},
                    {'range': [30, 40], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            }
        ))
        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.subheader("📈 Health Metrics")
        
        # Calculate ideal weight range
        ideal_weight_min = 18.5 * (height_m ** 2)
        ideal_weight_max = 24.9 * (height_m ** 2)
        
        # Calculate BMR (Basal Metabolic Rate)
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # Activity multipliers
        activity_multipliers = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extremely Active": 1.9
        }
        
        daily_calories = bmr * activity_multipliers[activity_level]
        
        # Display metrics
        st.metric("Current Weight", f"{weight:.1f} kg")
        st.metric("Ideal Weight Range", f"{ideal_weight_min:.1f} - {ideal_weight_max:.1f} kg")
        st.metric("BMR", f"{bmr:.0f} calories/day")
        st.metric("Daily Calories", f"{daily_calories:.0f} calories/day")
        
        # Weight difference
        weight_diff = weight - ((ideal_weight_min + ideal_weight_max) / 2)
        if weight_diff > 0:
            st.metric("Weight to Lose", f"{weight_diff:.1f} kg", delta=f"-{weight_diff:.1f}")
        elif weight_diff < 0:
            st.metric("Weight to Gain", f"{abs(weight_diff):.1f} kg", delta=f"+{abs(weight_diff):.1f}")
        else:
            st.success("✅ You're at your ideal weight!")
    
    # Health recommendations
    st.subheader("🎯 Personalized Recommendations")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 🍎 Diet Recommendations")
        
        if category == "Underweight":
            st.info("""
            **Gain Weight Healthily:**
            - Increase caloric intake by 300-500 calories/day
            - Focus on nutrient-dense foods
            - Include healthy fats (nuts, avocados)
            - Eat frequent, smaller meals
            - Consider strength training
            """)
        elif category == "Normal Weight":
            st.success("""
            **Maintain Your Weight:**
            - Continue balanced diet
            - Include all food groups
            - Stay hydrated (8-10 glasses water/day)
            - Regular meal timing
            - Monitor portion sizes
            """)
        elif category == "Overweight":
            st.warning("""
            **Lose Weight Gradually:**
            - Reduce caloric intake by 200-500 calories/day
            - Increase fiber intake
            - Choose lean proteins
            - Limit processed foods
            - Practice portion control
            """)
        else:  # Obese
            st.error("""
            **Consult Healthcare Provider:**
            - Seek professional guidance
            - Consider supervised diet plan
            - Focus on whole foods
            - Eliminate sugary drinks
            - Track food intake
            """)
    
    with col4:
        st.markdown("#### 🏃‍♂️ Exercise Recommendations")
        
        if category == "Underweight":
            st.info("""
            **Strength Building:**
            - Resistance training 3-4x/week
            - Compound movements (squats, deadlifts)
            - Progressive overload
            - Limit excessive cardio
            - Focus on muscle building
            """)
        elif category == "Normal Weight":
            st.success("""
            **Balanced Fitness:**
            - 150 minutes moderate cardio/week
            - 2-3 strength training sessions
            - Include flexibility work
            - Try varied activities
            - Maintain consistency
            """)
        elif category == "Overweight":
            st.warning("""
            **Cardio Focus:**
            - 45-60 minutes cardio daily
            - Low-impact exercises initially
            - Gradually increase intensity
            - Include strength training
            - Track progress regularly
            """)
        else:  # Obese
            st.error("""
            **Start Slowly:**
            - Begin with walking
            - Water exercises (low impact)
            - Gradually increase duration
            - Consult fitness professional
            - Focus on consistency over intensity
            """)
    
    # BMI History Tracker
    st.subheader("📊 BMI History Tracker")
    
    # Initialize session state for history
    if 'bmi_history' not in st.session_state:
        st.session_state.bmi_history = []
    
    # Add current BMI to history
    if st.button("📝 Save Current BMI"):
        entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'bmi': round(bmi, 1),
            'weight': round(weight, 1),
            'category': category
        }
        st.session_state.bmi_history.append(entry)
        st.success("BMI saved to history!")
    
    # Display history
    if st.session_state.bmi_history:
        st.markdown("#### Recent BMI Records")
        
        # Create DataFrame for plotting
        import pandas as pd
        df = pd.DataFrame(st.session_state.bmi_history)
        df['date'] = pd.to_datetime(df['date'])
        
        # Plot BMI trend
        fig_trend = px.line(df, x='date', y='bmi', 
                           title='BMI Trend Over Time',
                           markers=True,
                           color_discrete_sequence=['#667eea'])
        
        # Add BMI category zones
        fig_trend.add_hline(y=18.5, line_dash="dash", line_color="blue", annotation_text="Underweight")
        fig_trend.add_hline(y=25, line_dash="dash", line_color="green", annotation_text="Normal")
        fig_trend.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Obese")
        
        fig_trend.update_layout(height=400)
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Show recent entries
        st.dataframe(df.tail(5)[['date', 'bmi', 'weight', 'category']].sort_values('date', ascending=False))
        
        # Clear history button
        if st.button("🗑️ Clear History"):
            st.session_state.bmi_history = []
            st.success("History cleared!")
    
    # BMI Information
    st.subheader("ℹ️ Understanding BMI")
    
    with st.expander("What is BMI?"):
        st.write("""
        **Body Mass Index (BMI)** is a measure of body fat based on height and weight. 
        It's calculated using the formula: BMI = weight (kg) / height (m)²
        
        **BMI Categories:**
        - **Underweight**: BMI < 18.5
        - **Normal Weight**: BMI 18.5-24.9
        - **Overweight**: BMI 25-29.9
        - **Obese**: BMI ≥ 30
        
        **Important Notes:**
        - BMI is a screening tool, not a diagnostic tool
        - It doesn't account for muscle mass, bone density, or body composition
        - Athletes may have high BMI due to muscle mass
        - Consult healthcare providers for personalized advice
        """)
    
    with st.expander("Limitations of BMI"):
        st.write("""
        **BMI doesn't consider:**
        - Muscle vs. fat mass
        - Bone density
        - Body frame size
        - Age and gender differences
        - Distribution of fat
        
        **Better alternatives:**
        - Body fat percentage
        - Waist-to-hip ratio
        - Waist circumference
        - Body composition analysis
        """)

else:
    st.error("Please enter valid height and weight values.")