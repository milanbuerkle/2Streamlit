import streamlit as st
import read_data_1

# Überschriften
st.write("# EKG APP")
st.write("## Versuchsperson auswählen")

# 1. Die echten JSON-Daten über deine Funktion laden
daten = read_data_1.load_person_data()

# 2. Die Namensliste daraus generieren lassen
person_names = read_data_1.get_person_list(daten)

# 3. Auswahlbox mit den echten Namen befüllen
current_user = st.selectbox(
    'Versuchsperson',
    options = person_names, 
    key = "sbVersuchsperson"
)

st.write("Der Name ist: ", current_user)

current_person_data = read_data_1.find_person_data_by_name(daten, current_user)

# 2. Prüfen, ob die Person existiert und ob ein Bildpfad hinterlegt ist
if current_person_data and "picture_path" in current_person_data:
    
    # Den Pfad (z.B. "data/pictures/tb.jpg") auslesen
    bild_pfad = current_person_data["picture_path"]
    
    # Das Bild auf der Webseite anzeigen
    st.image(bild_pfad, caption=f"Foto von {current_user}", width=300)
    
else:
    # Falls in der JSON-Datei kein Bildpfad eingetragen ist oder etwas schiefging
    st.write("Kein Bild für diese Person gefunden.")


