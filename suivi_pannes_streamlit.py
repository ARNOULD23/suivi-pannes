
import streamlit as st
import json
from datetime import datetime, timedelta

# Load existing data from JSON file
def load_data():
    try:
        with open('pannes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save data to JSON file
def save_data(data):
    with open('pannes.json', 'w') as f:
        json.dump(data, f, indent=4)

# Add a new panne
def add_panne(description, responsable, priorite, action_requise):
    pannes = load_data()
    new_panne = {
        "id": len(pannes) + 1,
        "description": description,
        "date_creation": datetime.now().strftime("%Y-%m-%d"),
        "responsable": responsable,
        "priorite": priorite,
        "statut": "En cours",
        "action_requise": action_requise,
        "commentaires": ""
    }
    pannes.append(new_panne)
    save_data(pannes)

# Mark a panne as resolved
def mark_as_resolved(panne_id):
    pannes = load_data()
    for panne in pannes:
        if panne["id"] == panne_id:
            panne["statut"] = "Résolu"
            break
    save_data(pannes)

# Calculate days elapsed since creation
def days_elapsed(date_creation):
    date_creation = datetime.strptime(date_creation, "%Y-%m-%d")
    return (datetime.now() - date_creation).days

# Streamlit app
st.title("Suivi des Pannes")

# Add new panne
st.header("Ajouter une nouvelle panne")
description = st.text_input("Description")
responsable = st.text_input("Responsable")
priorite = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute"])
action_requise = st.selectbox("Action requise", ["Oui", "Non"])

if st.button("Ajouter"):
    add_panne(description, responsable, priorite, action_requise)
    st.success("Panne ajoutée avec succès!")

# Display pannes en cours
st.header("Pannes en cours")
pannes = load_data()
for panne in pannes:
    if panne["statut"] == "En cours":
        st.subheader(f"Panne ID: {panne['id']}")
        st.write(f"Description: {panne['description']}")
        st.write(f"Date de création: {panne['date_creation']}")
        st.write(f"Responsable: {panne['responsable']}")
        st.write(f"Priorité: {panne['priorite']}")
        st.write(f"Action requise: {panne['action_requise']}")
        st.write(f"Jours écoulés: {days_elapsed(panne['date_creation'])}")
        if st.button(f"Marquer comme résolu - ID {panne['id']}"):
            mark_as_resolved(panne["id"])
            st.success(f"Panne ID {panne['id']} marquée comme résolue!")

# Display resolved pannes
st.header("Pannes résolues")
for panne in pannes:
    if panne["statut"] == "Résolu":
        st.subheader(f"Panne ID: {panne['id']}")
        st.write(f"Description: {panne['description']}")
        st.write(f"Date de création: {panne['date_creation']}")
        st.write(f"Responsable: {panne['responsable']}")
        st.write(f"Priorité: {panne['priorite']}")
        st.write(f"Action requise: {panne['action_requise']}")
        st.write(f"Commentaires: {panne['commentaires']}")
