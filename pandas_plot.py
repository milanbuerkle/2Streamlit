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
    
    #Auseertung des Leistungstests werden hier ausgegeben
    st.write(f"Durchschnittliche Leistung: **{mittelwert_leistung} W**")
    st.write(f"Maximale Leistung: **{maximalwert_leistung} W**")

    # 3. Zonen berechnen
    hf_max = st.number_input("Deine maximale Herzfrequenz (HF max):", value=190, step=1 ,max_value=250, min_value=100)
    zone_grenzen = [0, 0.60 * hf_max, 0.70 * hf_max, 0.80 * hf_max, 0.90 * hf_max, hf_max]
    zone_namen = ["Zone 1 (<60%)", "Zone 2 (60-70%)", "Zone 3 (70-80%)", "Zone 4 (80-90%)", "Zone 5 (90-100%)"]

    df["Zone"] = pd.cut(df["HeartRate"], bins=zone_grenzen, labels=zone_namen)

    watt_max = df["PowerOriginal"].max()
    watt_grenzen = [0, 0.55 * watt_max, 0.75 * watt_max, 0.90 * watt_max, 1.05 * watt_max, watt_max * 1.5]
    return df, zone_grenzen, watt_grenzen

  
def leistungstest_data(df, zone_grenzen, watt_grenzen):
    st.subheader("Interaktiver Kurvenverlauf")

    hintergrund_auswahl = st.radio(
        "Hintergrund-Farbzonen auswählen:",
        options=["Keine", "Herzfrequenz-Zonen", "Leistungs-Zonen (Watt)",],
        horizontal=True
    )
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["PowerOriginal"],
            name="Leistung (W)",
            line=dict(color="blue")
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df["HeartRate"],
            name="Herzfrequenz (bpm)",
            line=dict(color="red")
        )
    )
    
    #Hintergrundfarben an die Y-Achse koppeln
    Herzfrequenz_farben = [
        "rgba(0, 200, 0, 0.15)",    # Zone 1: Grün
        "rgba(255, 215, 0, 0.15)",  # Zone 2: Gelb
        "rgba(255, 140, 0, 0.15)",  # Zone 3: Orange
        "rgba(255, 69, 0, 0.15)",   # Zone 4: Hellrot
        "rgba(200, 0, 0, 0.15)"     # Zone 5: Dunkelrot
    ]
    watt_farben = [
        "rgba(230, 210, 255, 0.25)", # Z1: Sehr helles Lila
        "rgba(200, 160, 255, 0.22)", # Z2: Helles Lila
        "rgba(170, 110, 255, 0.18)", # Z3: Mittleres Lila
        "rgba(130, 50, 230, 0.15)",  # Z4: Kräftiges Lila
        "rgba(80, 0, 160, 0.15)"     # Z5: Dunkellila
        ]
    hintergrund_shapes = []
    
    if hintergrund_auswahl != "Keine":
        if hintergrund_auswahl == "Herzfrequenz-Zonen":
            aktuelle_grenzen = zone_grenzen
            aktuelle_farben = Herzfrequenz_farben  # KORREKTUR: Name angepasst
        else:
            aktuelle_grenzen = watt_grenzen
            aktuelle_farben = watt_farben
            
        # KORREKTUR: Die Schleife ist jetzt richtig eingerückt
        for i in range(5):
            hintergrund_shapes.append(
                dict(
                    type="rect",
                    xref="paper",
                    yref="y", 
                    x0=0,
                    x1=1,
                    y0=aktuelle_grenzen[i],
                    y1=aktuelle_grenzen[i+1],
                    fillcolor=aktuelle_farben[i],
                    line=dict(width=0),
                    layer="below"
                )
            )

    fig.update_layout(   #höhere Höhe damit beide Kurven und die Hintergrundfarben gut sichtbar sind
        shapes=hintergrund_shapes,
        height=650
    )


    fig.update_yaxes(range=[0, max(df["HeartRate"].max(), df["PowerOriginal"].max()) * 1.1])

    st.plotly_chart(fig, use_container_width=True)

  
    # 4. Tabellen erstellen und direkt ausgeben
    zeit_pro_zone = df.groupby("Zone").size().rename("verbrachte Zeit in jeweiliger Zone")
    
    leistung_pro_zone = df.groupby("Zone")["PowerOriginal"].mean().round(2).rename("erbrachte Leistung in jeweiliger Zone")

    st.subheader("Zonen-Analyse")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Zeit pro Zone (Sekunden):**")
        st.dataframe(zeit_pro_zone)
    with col2:
        st.write("**Ø Leistung pro Zone:**")
        st.dataframe(leistung_pro_zone)


if __name__ == "__main__":
    zeige_leistungstest()


    