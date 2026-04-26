import streamlit as st
import pandas as pd
import random

# Configuration de l'interface
st.set_page_config(page_title="Loto-Euro Fusion Pro", page_icon="🧬", layout="wide")

st.title("🧬 Intelligence Croisée : Loto & Euromillions")
st.write("Analyse stratégique basée sur le tirage du **Samedi 25 Avril 2026**")

# --- 1. BASE DE DONNÉES (LOGIQUE CROISÉE) ---
# Tirage Loto du 25/04 : 17 - 22 - 23 - 25 - 49
numeros_loto_chauds = [17, 22, 23, 25, 49, 16, 30, 2, 33, 9, 10, 13]
numeros_euro_chauds = [44, 42, 23, 13, 17, 10, 49, 19, 29, 37, 50, 25]

# Calcul automatique de la convergence
convergence = list(set(numeros_loto_chauds) & set(numeros_euro_chauds))

# --- 2. LOGIQUE DE L'ENTONNOIR ---
def generer_ticket_expert():
    # A. Le Noyau Dur (Incontournables)
    noyau = [13, 44] 
    # B. Le Transfert d'Énergie (Loto vers Euro)
    transfert = [23, 49, 17]
    # C. Les Surprises (Écart ou Forme)
    surprises = [42, 10, 16, 22]
    
    ticket = set()
    ticket.add(13) # On force le pilier
    ticket.add(23) # On force le pivot
    
    # On complète avec les autres listes
    candidats = [n for n in (transfert + surprises + noyau) if n not in ticket]
    while len(ticket) < 5:
        ticket.add(random.choice(candidats))
        
    return sorted(list(ticket))

# --- 3. INTERFACE UTILISATEUR ---
tab1, tab2, tab3 = st.tabs(["🏆 PRONOSTIC EXPERT", "🚀 CONVERGENCE", "🔄 ANALYSE MIROIR"])

with tab1:
    st.header("🏆 La Sélection de l'Entonnoir")
    st.info("Cette méthode filtre les 50 numéros pour ne garder que l'élite : Pivot + Piliers + Écart.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 GÉNÉRER MON TICKET PRIORITAIRE"):
            grille = generer_ticket_expert()
            etoiles = sorted(random.sample([2, 8, 3, 10, 11], 2))
            
            # --- AJUSTEMENT : ANALYSE ÉQUILIBRE ---
            nb_pairs = len([n for n in grille if n % 2 == 0])
            nb_impairs = 5 - nb_pairs
            
            st.success(f"**Numéros :** {', '.join(map(str, grille))}")
            st.warning(f"**Étoiles :** {etoiles[0]} — {etoiles[1]}")
            
            # Affichage de l'équilibre
            st.write(f"⚖️ **Équilibre :** {nb_pairs} Pairs / {nb_impairs} Impairs")
            if nb_pairs == 0 or nb_pairs == 5:
                st.error("⚠️ Alerte : Grille très déséquilibrée. Un rééquilibrage est conseillé.")
            elif nb_pairs == 2 or nb_pairs == 3:
                st.info("✅ Équilibre Statistique Optimal (2/3 ou 3/2).")
            
            st.balloons()
            
    with col2:
        st.write("**Rappel de la Stratégie :**")
        st.write("- **Pivot :** 23 (Confirmé Samedi)")
        st.write("- **Piliers :** 13, 44")
        st.write("- **Énergie Loto :** 17, 49")
        st.write("- **Conseil Expert :** Privilégiez 2 ou 3 numéros pairs pour mardi.")

with tab2:
    st.header("📊 Tableau de Convergence")
    df_conv = pd.DataFrame({
        "Numéro": convergence,
        "Force": [99 if n in [13, 23] else 85 for n in convergence],
        "Statut": ["⭐ Pivot/Pilier" if n in [13, 23] else "✅ Confirmé" for n in convergence]
    }).sort_values(by="Force", ascending=False)
    st.table(df_conv)

with tab3:
    st.header("🔄 Flux Miroir")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Loto ➔ Euro")
        st.write("Numéros du samedi à surveiller mardi :")
        st.code("17, 22, 23, 25, 49")
    with col_b:
        st.subheader("Euro ➔ Loto")
        st.write("Bases historiques pour le prochain Loto :")
        st.code("44, 42, 13, 19")

st.divider()
st.caption("Dernière mise à jour : Dimanche 26 Avril 2026. Basé sur le succès du système (4/5 au Loto du 25/04).")
