import streamlit as st
import pandas as pd
import datetime

# Conversion functions with additional units
st.set_page_config(page_title='Advanced Unit Converter',
                   layout='wide', icon='📐')


def length_conversion(value, from_unit, to_unit):
    factors = {
        'meters': 1, 'kilometers': 0.001, 'centimeters': 100, 'millimeters': 1000,
        'miles': 0.000621371, 'yards': 1.09361, 'feet': 3.28084, 'inches': 39.3701,
        'nautical miles': 0.000539957, 'micrometers': 1e6, 'nanometers': 1e9
    }
    return value * factors[to_unit] / factors[from_unit]


def weight_conversion(value, from_unit, to_unit):
    factors = {
        'grams': 1, 'kilograms': 0.001, 'milligrams': 1000, 'pounds': 0.00220462,
        'ounces': 0.035274, 'tons': 1e-6, 'carats': 5, 'stone': 0.000157473
    }
    return value * factors[to_unit] / factors[from_unit]


def temperature_conversion(value, from_unit, to_unit):
    conversions = {
        'Celsius': {'Fahrenheit': lambda x: (x * 9/5) + 32, 'Kelvin': lambda x: x + 273.15},
        'Fahrenheit': {'Celsius': lambda x: (x - 32) * 5/9, 'Kelvin': lambda x: (x - 32) * 5/9 + 273.15},
        'Kelvin': {'Celsius': lambda x: x - 273.15, 'Fahrenheit': lambda x: (x - 273.15) * 9/5 + 32}
    }
    return conversions[from_unit][to_unit](value)


def area_conversion(value, from_unit, to_unit):
    factors = {
        'square meters': 1, 'square kilometers': 1e-6, 'square miles': 3.861e-7,
        'acres': 0.000247105, 'hectares': 0.0001, 'square feet': 10.7639,
        'square inches': 1550, 'square yards': 1.19599
    }
    return value * factors[to_unit] / factors[from_unit]


def speed_conversion(value, from_unit, to_unit):
    factors = {
        'm/s': 1, 'km/h': 3.6, 'mph': 2.23694, 'knots': 1.94384,
        'ft/s': 3.28084, 'mach': 0.00293858
    }
    return value * factors[to_unit] / factors[from_unit]


def volume_conversion(value, from_unit, to_unit):
    factors = {
        'liters': 1, 'milliliters': 1000, 'cubic meters': 0.001,
        'cubic feet': 0.0353147, 'cubic inches': 61.0237,
        'gallons': 0.264172, 'quarts': 1.05669, 'pints': 2.11338
    }
    return value * factors[to_unit] / factors[from_unit]


# Session state initialization
if 'history' not in st.session_state:
    st.session_state.history = []
if 'realtime' not in st.session_state:
    st.session_state.realtime = True

# Preset examples
presets = {
    'Common Temperature': ('Temperature', 100, 'Celsius', ['Fahrenheit']),
    'Marathon Distance': ('Length', 42.195, 'kilometers', ['miles']),
    'Human Body Weight': ('Weight', 70, 'kilograms', ['pounds']),
    'Olympic Pool Volume': ('Volume', 2500, 'cubic meters', ['liters', 'gallons']),
    'Sound Speed': ('Speed', 343, 'm/s', ['km/h', 'mph'])
}

# App layout

st.title('📐 Advanced Unit Converter')
with st.sidebar:
    st.header("Settings")
    st.checkbox("Real-time Conversion", key='realtime')
    if st.button("Clear History"):
        st.session_state.history = []
    st.download_button("Download History", "\n".join(
        st.session_state.history[-10:]), "conversion_history.txt")

# Preset buttons
st.subheader("Quick Presets")
cols = st.columns(3)
for i, (name, preset) in enumerate(presets.items()):
    with cols[i % 3]:
        if st.button(name):
            conversion_type, value, from_unit, to_units = preset
            st.session_state.conversion_type = conversion_type
            st.session_state.value = value
            st.session_state.from_unit = from_unit
            st.session_state.to_units = to_units

# Main converter
with st.container():
    st.subheader("Converter")
    conversion_type = st.selectbox('Select conversion type',
                                   ['Length', 'Weight', 'Temperature', 'Area', 'Speed', 'Volume'], key='conversion_type')

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        value = st.number_input('Enter value', value=1.0, key='value')
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↔ Swap") and st.session_state.to_units:
            st.session_state.from_unit, st.session_state.to_units = st.session_state.to_units[0], [
                st.session_state.from_unit]
    with col3:
        units = {
            'Length': ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'yards', 'feet', 'inches'],
            'Weight': ['grams', 'kilograms', 'milligrams', 'pounds', 'ounces', 'tons'],
            'Temperature': ['Celsius', 'Fahrenheit', 'Kelvin'],
            'Area': ['square meters', 'square kilometers', 'square miles', 'acres', 'hectares', 'square feet'],
            'Speed': ['m/s', 'km/h', 'mph', 'knots', 'ft/s'],
            'Volume': ['liters', 'milliliters', 'cubic meters', 'gallons', 'cubic feet']
        }
        from_unit = st.selectbox(
            'From unit', units[conversion_type], key='from_unit')
        to_units = st.multiselect(
            'To units', units[conversion_type], key='to_units')

# Conversion and results
if to_units and (st.session_state.realtime or st.button("Convert")):
    results = []
    for to_unit in to_units:
        if conversion_type == 'Length':
            result = length_conversion(value, from_unit, to_unit)
        elif conversion_type == 'Weight':
            result = weight_conversion(value, from_unit, to_unit)
        elif conversion_type == 'Temperature':
            result = temperature_conversion(value, from_unit, to_unit)
        elif conversion_type == 'Area':
            result = area_conversion(value, from_unit, to_unit)
        elif conversion_type == 'Speed':
            result = speed_conversion(value, from_unit, to_unit)
        elif conversion_type == 'Volume':
            result = volume_conversion(value, from_unit, to_unit)

        results.append((to_unit, result))
        entry = f"{value} {from_unit} → {result:.4f} {to_unit}"
        st.session_state.history.append(entry)

    st.subheader("Results")
    for to_unit, result in results:
        st.markdown(f"""
            <div class="unit-card" style="margin-top: 10px 0; padding: 10px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.1);">
                <b>{value} {from_unit}</b> = 
                <span style="color: #2ecc71; font-size: 1.2em; ">{result:.4f}</span> {to_unit}
            </div>
        """, unsafe_allow_html=True)

# Conversion history
if st.session_state.history:
    with st.expander("📜 Conversion History (Last 10 entries)"):
        for entry in reversed(st.session_state.history[-10:]):
            st.markdown(
                f"<div class='history-item'>{entry}</div>", unsafe_allow_html=True)

# Unit reference table
st.subheader("📚 Unit Reference")
unit_categories = {
    'Area': ['square meters', 'square kilometers', 'acres', 'hectares'],
    'Length': ['meters', 'kilometers', 'miles', 'feet'],
    'Weight': ['grams', 'kilograms', 'pounds', 'ounces'],
    'Temperature': ['Celsius', 'Fahrenheit', 'Kelvin'],
    'Speed': ['m/s', 'km/h', 'mph'],
    'Volume': ['liters', 'gallons', 'cubic meters']
}
with st.expander("📚 Unit Reference Table"):
    st.table(pd.DataFrame([
        {'Category': category, 'Units': unit}
        for category, units in unit_categories.items()
        for unit in units
    ]))

    # Remove duplicate entries in history
    unique_history = []
    for entry in st.session_state.history:
        if entry not in unique_history:
            unique_history.append(entry)
    st.session_state.history = unique_history

year = datetime.datetime.now().year

st.markdown(f"""
    <style>
        .footer {{
            text-align: center;
            padding: 15px 0;
            font-size: 14px;
            color: #777;
            border-top: 1px solid #ddd;
            position: relative;
            bottom: 0;
            width: 100%;
        }}
        @media (max-width: 600px) {{
            .footer {{
                font-size: 12px;
                padding: 10px 0;
            }}
        }}
    </style>
    <footer class="footer">
        © {year} Rafay Nadeem. All rights reserved.
    </footer>
""", unsafe_allow_html=True)
