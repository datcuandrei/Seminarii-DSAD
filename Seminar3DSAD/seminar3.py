import os

import pandas as pd

os.makedirs("data_out", exist_ok=True)

df_industrie = pd.read_csv("data_in/IndustriaAlimentara.csv", index_col=0)
activitati = list(df_industrie.columns)[1:]
df_populatie = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
df_judete = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)

total_angajati_loc = df_industrie[activitati].sum(axis=1)

# ---------------------------------------------------------------------------
# Cerinta 1
# Sa se salveze in fisierul Cerinta1.csv datele privind numarul de angajati
# pe activitatile din industria alimentara, pentru localitatile in care
# numarul de angajati este mai mare decat 0. Fisierul Cerinta1.csv va avea
# aceleasi coloane ca fisierul IndustriaAlimentara.csv.
rez1 = df_industrie[total_angajati_loc > 0]
rez1.to_csv("data_out/Cerinta1.csv")

# ---------------------------------------------------------------------------
# Cerinta 2
# Sa se calculeze si sa se salveze in fisierul Cerinta2.csv, procentul de
# angajati pe fiecare activitate la nivel de localitate.
rez2 = df_industrie[activitati].div(total_angajati_loc, axis=0) * 100
rez2.insert(0, "Localitate", df_industrie["Localitate"])
rez2.to_csv("data_out/Cerinta2.csv")

# ---------------------------------------------------------------------------
# Cerinta 3
# Sa se salveze in fisierul Cerinta3.csv judetele sortate descrescator dupa
# ponderea angajatilor din industria alimentara in populatia totala.
df_loc = df_industrie.merge(df_populatie, left_index=True, right_index=True)
df_pe_judet = df_loc[activitati + ["Populatie", "Judet"]].groupby("Judet").sum()

rez3 = df_pe_judet[activitati].sum(axis=1) / df_pe_judet["Populatie"]
rez3.name = "Pondere"
rez3 = rez3.sort_values(ascending=False)
rez3.to_csv("data_out/Cerinta3.csv")

# ---------------------------------------------------------------------------
# Cerinta 4
# Sa se salveze in fisierul Cerinta4.csv, activitatea cu cei mai multi
# angajati la nivel de judet. Se va afisa indicativul de judet si activitatea
# dominanta.
rez4 = df_pe_judet[activitati].idxmax(axis=1)
rez4.name = "Activitate"
rez4.to_csv("data_out/Cerinta4.csv")

# ---------------------------------------------------------------------------
# Cerinta 5
# Sa se salveze in fisierul Cerinta5.csv numarul mediu de angajati pe fiecare
# activitate la nivel de regiune. Se va calcula media ponderata, folosind ca
# pondere populatia localitatilor.
df_reg = df_loc[activitati + ["Populatie", "Judet"]].merge(
    df_judete["Regiune"], left_on="Judet", right_index=True
)
suma_produse = df_reg[activitati].mul(df_reg["Populatie"], axis=0).groupby(df_reg["Regiune"]).sum()
suma_ponderi = df_reg.groupby("Regiune")["Populatie"].sum()
rez5 = suma_produse.div(suma_ponderi, axis=0)
rez5.round(3).to_csv("data_out/Cerinta5.csv")

# ---------------------------------------------------------------------------
# Cerinta 6
# Sa se calculeze si sa se afiseze in fisierul Cerinta6.csv indicii de
# localizare la nivel de judet pentru fiecare activitate. Un indice de
# localizare se calculeaza ca raport intre ponderea judetului i in activitatea
# j la nivel national si ponderea populatiei din judetul i in totalul
# populatiei.
total_tara = df_pe_judet.sum(axis=0)
pondere_activitate = df_pe_judet[activitati].div(total_tara[activitati], axis=1)
pondere_populatie = df_pe_judet["Populatie"] / total_tara["Populatie"]
rez6 = pondere_activitate.div(pondere_populatie, axis=0)
rez6.round(3).to_csv("data_out/Cerinta6.csv")
