import streamlit as st
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="Kostadin AI Maç Tahmin ⚽", layout="wide")

st.title("Kostadin AI – Maç Tahmin v0.2 🔥")
st.markdown("Telefonunda Ana Ekrana Ekle → App gibi kullan!")

ev = st.text_input("Ev Sahibi Takım", "Fenerbahçe")
dep = st.text_input("Deplasman Takım", "Galatasaray")

st.subheader("Son Form Ortalamaları (Elle Gir – İleride API olacak)")
col1, col2 = st.columns(2)

with col1:
    ev_atlama = st.slider("Ev Sahibinin Attığı Ortalama Gol", 0.5, 4.0, 1.8, 0.1)
    ev_yeme    = st.slider("Ev Sahibinin Yediği Ortalama Gol", 0.5, 4.0, 1.3, 0.1)

with col2:
    dep_atlama = st.slider("Deplasmanın Attığı Ortalama Gol", 0.5, 4.0, 1.5, 0.1)
    dep_yeme   = st.slider("Deplasmanın Yediği Ortalama Gol", 0.5, 4.0, 1.6, 0.1)

if st.button("Tahmin Et 🔥", type="primary"):
    lig_ort_gol = 2.65
    
    ev_attack   = ev_atlama / lig_ort_gol
    ev_def      = ev_yeme   / lig_ort_gol
    dep_attack  = dep_atlama / lig_ort_gol
    dep_def     = dep_yeme   / lig_ort_gol
    
    ev_gol_exp  = ev_attack  * dep_def * lig_ort_gol
    dep_gol_exp = dep_attack * ev_def  * lig_ort_gol
    
    st.subheader("Beklenen Goller")
    c1, c2 = st.columns(2)
    c1.metric(f"🏠 {ev}", f"{ev_gol_exp:.2f}")
    c2.metric(f"🚗 {dep}", f"{dep_gol_exp:.2f}")
    
    home_w = draw = away_w = 0.0
    skorlar = []
    
    for h in range(9):
        for a in range(9):
            p = poisson.pmf(h, ev_gol_exp) * poisson.pmf(a, dep_gol_exp)
            if h > a: home_w += p
            elif h == a: draw += p
            else: away_w += p
            if p > 0.012:
                skorlar.append((h, a, p*100))
    
    skorlar.sort(key=lambda x: x[2], reverse=True)
    
    st.subheader("Olasılıklar")
    st.success(f"🏠 {ev} kazanır: **{home_w*100:.1f}%**")
    st.info(f"Beraberlik: **{draw*100:.1f}%**")
    st.error(f"🚗 {dep} kazanır: **{away_w*100:.1f}%**")
    
    st.subheader("En Olası Skorlar (Top 5)")
    for h,a,p in skorlar[:5]:
        st.write(f"{h}-{a} → **%{p:.1f}**")

st.markdown("---")
st.caption("Yapay zekâ basit Poisson modeli kullanıyor. Gerçek verilerle (API) çok daha güçlü olur!")
