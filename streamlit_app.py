import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="IA OMNIBUS V6.1 - Post-Tirage", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main { background: #020617; color: #f8fafc; font-family: 'Urbanist', sans-serif; }
    .card { background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 15px; border: 1px solid #334155; }
    .ball {
        display: inline-flex; align-items: center; justify-content: center;
        width: 55px; height: 55px; border-radius: 50%; font-size: 22px;
        font-weight: bold; margin: 5px; color: #000;
        box-shadow: inset -3px -3px 10px rgba(0,0,0,0.3);
    }
    .euro-ball { background: linear-gradient(135deg, #00f2fe, #4facfe); }
    .loto-ball { background: linear-gradient(135deg, #f093fb, #f5576c); color: white; }
    .status-up { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- CHARGEMENT ---
def load_data():
    if os.path.exists("data_fusion.csv"):
        return pd.read_csv("data_fusion.csv")
    return pd.DataFrame()

df = load_data()

# --- ALGORITHME V6.1 ---
def get_predictions(mode="euro"):
    data = df.copy()
    if mode == "euro":
        # Calcul : Masse + (Ecart x 1.5) + Bonus Zone de Silence (14-41)
        data['score'] = (data['masse_euro'] * 0.2) + (data['ecart_euro'] * 1.5)
        data.loc[(data['numero'] > 14) & (data['numero'] < 41), 'score'] += 25
    else:
        # Calcul Loto : Masse Loto + Ecart Loto
        data['score'] = (data['masse_loto'] * 0.6) + (data['ecart_loto'] * 0.4)
    
    return data.sort_values('score', ascending=False).head(5)

# --- INTERFACE ---
st.title("🧬 IA OMNIBUS V6.1 - Analyse Post-Résultats")
st.write(f"Derniers numéros sortis : **1 - 3 - 9 - 11 - 42** | Étoiles : **46 - 47**")

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🇪🇺 PRONOSTIC PROCHAIN EURO")
        if st.button("CALCULER NOUVEAUX FLUX"):
            preds = get_predictions("euro")
            balls_html = "".join([f"<div class='ball euro-ball'>{int(n)}</div>" for n in sorted(preds['numero'])])
            st.markdown(balls_html, unsafe_allow_html=True)
            st.write("---")
            st.write("**Analyse :** Transfert d'énergie vers le numéro **32** (Ecart 36) et la zone médiane.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 ÉTAT DES TENSIONS (Top 5)")
        tension_df = df.sort_values('ecart_euro', ascending=False).head(5)
        for _, row in tension_df.iterrows():
            st.write(f"Numéro **{int(row['numero'])}** : Écart de {int(row['ecart_euro'])} tirages")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.write("### 📈 Matrice de Recalcul")
    st.dataframe(df, use_container_width=True)
else:
    st.error("Fichier data_fusion.csv manquant !")
