import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def zeige_leistungstest():
    # 1. Überschrift anzeigen und Daten laden
    st.header("Auswertung Leistungstest")
    df = pd.read_csv("data/activity.csv")

    # 2. Kennzahlen berechnen und ausgeben
    mittelwert_leistung = round(df["PowerOriginal"].mean(), 2)
    maximalwert_leistung = round(df["PowerOriginal"].max(), 2)
    
    st.write("Durchschnittliche Leistung:", mittelwert_leistung, "W")
    st.write("Maximale Leistung:", maximalwert_leistung, "W")

    # 3. Zonen berechnen
    hf_max = st.number_input("Deine maximale Herzfrequenz (HF max):", value=190, step=1)
    zone_grenzen = [0, 0.60 * hf_max, 0.70 * hf_max, 0.80 * hf_max, 0.90 * hf_max, hf_max]
    zone_namen = ["Zone 1 (<60%)", "Zone 2 (60-70%)", "Zone 3 (70-80%)", "Zone 4 (80-90%)", "Zone 5 (90-100%)"]

    df["Zone"] = pd.cut(df["HeartRate"], bins=zone_grenzen, labels=zone_namen)
    
    # 4. Tabellen erstellen und direkt ausgeben
    zeit_pro_zone = df.groupby("Zone").size().rename("verbrachte Zeit in jeweiliger Zone")
    
    leistung_pro_zone = df.groupby("Zone")["PowerOriginal"].mean().round(2).rename("erbrachte Leistung in jeweiliger Zone")

    st.subheader("Zonen-Analyse")
    st.write("**Zeit pro Zone (Sekunden):**")
    st.dataframe(zeit_pro_zone)
    
    st.write("**Ø Leistung pro Zone:**")
    st.dataframe(leistung_pro_zone)

    # 5. Interaktiven Plot erstellen (Zwei Achsen sind für die Ansicht nötig)
    st.subheader("Interaktiver Kurvenverlauf")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Linien hinzufügen (Plotly wählt die Farben jetzt automatisch)
    fig.add_trace(go.Scatter(x=df.index, y=df["PowerOriginal"], name="Leistung (W)"), secondary_y=False)
    fig.add_trace(go.Scatter(x=df.index, y=df["HeartRate"], name="Herzfrequenz (bpm)"), secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    zeige_leistungstest()


    #hallo