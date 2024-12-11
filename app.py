import streamlit as st
import pandas as pd
import joblib

# Load the encoders and classifier
device_name_encoder = joblib.load("Device_Name_encoder.pkl")
attack_encoder = joblib.load("Attack_encoder.pkl")
attack_subtype_encoder = joblib.load("Attack_subType_encoder.pkl")
rf_classifier = joblib.load("rf_classifier")

# Dropdown options
device_names = [
    'Philips_B120N10_Baby_Monitor', 
    'Danmini_Doorbell', 
    'SimpleHome_XCS7_1002_WHT_Security_Camera', 
    'SimpleHome_XCS7_1003_WHT_Security_Camera', 
    'Provision_PT_838_Security_Camera', 
    'Ecobee_Thermostat', 
    'Provision_PT_737E_Security_Camera', 
    'Samsung_SNH_1011_N_Webcam', 
    'Ennio_Doorbell'
]
attacks = ['mirai', 'gafgyt', 'Normal']
attack_subtypes = ['udp', 'tcp', 'scan', 'syn', 'ack', 'Normal', 'udpplain', 'combo', 'junk']

# Streamlit app
st.title("IoT Device Attack Prediction")

# Input form
with st.form("input_form"):
    st.subheader("Input Features")
    
    # Dropdowns for categorical variables
    device_name = st.selectbox("Device Name", device_names)
    attack = st.selectbox("Attack Type", attacks)
    attack_subtype = st.selectbox("Attack Subtype", attack_subtypes)
    
    # Numeric input for other features
    numerical_features = {}
    for feature in [
        "MI_dir_L0.1_weight", "MI_dir_L0.1_mean", "MI_dir_L0.1_variance", 
        "H_L0.1_weight", "H_L0.1_mean", "H_L0.1_variance", 
        "HH_L0.1_weight", "HH_L0.1_mean", "HH_L0.1_std", "HH_L0.1_magnitude", 
        "HH_L0.1_radius", "HH_L0.1_covariance", "HH_L0.1_pcc", 
        "HH_jit_L0.1_weight", "HH_jit_L0.1_mean", "HH_jit_L0.1_variance", 
        "HpHp_L0.1_weight", "HpHp_L0.1_mean", "HpHp_L0.1_std", 
        "HpHp_L0.1_magnitude", "HpHp_L0.1_radius", "HpHp_L0.1_covariance", "HpHp_L0.1_pcc"
    ]:
        numerical_features[feature] = st.number_input(f"{feature}", value=0.0)
    
    submitted = st.form_submit_button("Predict")

if submitted:
    # Encode categorical inputs
    encoded_device_name = device_name_encoder.transform([device_name])[0]
    encoded_attack = attack_encoder.transform([attack])[0]
    encoded_attack_subtype = attack_subtype_encoder.transform([attack_subtype])[0]
    
    # Combine inputs into a single list
    input_data = [
        numerical_features["MI_dir_L0.1_weight"], 
        numerical_features["MI_dir_L0.1_mean"], 
        numerical_features["MI_dir_L0.1_variance"], 
        numerical_features["H_L0.1_weight"], 
        numerical_features["H_L0.1_mean"], 
        numerical_features["H_L0.1_variance"], 
        numerical_features["HH_L0.1_weight"], 
        numerical_features["HH_L0.1_mean"], 
        numerical_features["HH_L0.1_std"], 
        numerical_features["HH_L0.1_magnitude"], 
        numerical_features["HH_L0.1_radius"], 
        numerical_features["HH_L0.1_covariance"], 
        numerical_features["HH_L0.1_pcc"], 
        numerical_features["HH_jit_L0.1_weight"], 
        numerical_features["HH_jit_L0.1_mean"], 
        numerical_features["HH_jit_L0.1_variance"], 
        numerical_features["HpHp_L0.1_weight"], 
        numerical_features["HpHp_L0.1_mean"], 
        numerical_features["HpHp_L0.1_std"], 
        numerical_features["HpHp_L0.1_magnitude"], 
        numerical_features["HpHp_L0.1_radius"], 
        numerical_features["HpHp_L0.1_covariance"], 
        numerical_features["HpHp_L0.1_pcc"], 
        encoded_device_name, 
        encoded_attack, 
        encoded_attack_subtype
    ]
    
    # Predict the label
    prediction = rf_classifier.predict([input_data])[0]
    
    # Display prediction
    st.success(f"The predicted label is: {prediction}")
