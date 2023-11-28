import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Are you an Hambriento Amigo?")
st.markdown("Let's find out")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="pizza", usecols=list(range(5)), ttl=5)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
TYPEOFPIZZA = [
    "PEPERONI",
    "NAPOLITAN",
    "SUPREME",
    "SHRIMPS",
    "VEGGIE",
]
PINEAPPLECHOICE = [
    "Ja, ich liebe es 💖",
    "Nein, ich hasse es 👿",
]
PIZZALOVER=[
    "Ja",
    "Nein",
]
COUNTRIES=[
    "Peru",
    "Usa",
    "Ukraine",
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    pizza = st.selectbox("Do you like pizza 🍕*", options=PIZZALOVER, index=None)
    type = st.multiselect("What's you favorite kind of pizza?*", options=TYPEOFPIZZA)
    pineapple = st.selectbox("pineapple? 👀", options=PINEAPPLECHOICE, index=None)
    age = st.number_input("Wie alt bist du?")
    nationality = st.selectbox("Woher kommst du?", options=COUNTRIES, index=None)

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="push the botton")
    
    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not pizza or not TYPEOFPIZZA:
            st.warning("We need to know more")
            st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "pizza": pizza,
                        "Type": ", ".join(type),
                        "pineapple": pineapple,
                        "age": age,
                        "nationality": nationality
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="pizza", data=updated_df)

            st.success("Bitte Hambriento Amigo")