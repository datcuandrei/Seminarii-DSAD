import pandas as pd

#Cerinta 1-> Încărcați winequality-red.csv cu separator corect.
# Afișați shape, primele 5 rânduri, tipurile coloanelor.
df = pd.read_csv("winequality-red.csv", sep = ";")
print("Shape: ")
print(df.shape)

print("\nPrimele 5 randuri:")
print(df.head())
print("\nTipurile coloanelor: ")
print(df.dtypes)

#Cerinta 2 ->Implementați nan_replace_df(tabel) în functii_online.py (media pe coloană pentru numerice).
# Aplicați pe tabel; confirmați că nu rămân NaN (setul UCI nu are de obicei lipsuri — codul trebuie să fie general, ca la examen).
import pandas as pd
from functii_online import nan_replace_df

df = pd.read_csv("winequality-red.csv", sep = ";")

df=nan_replace_df(df)
print(df.isna().sum().sum())

#Cerinta 3 -> Salvați în data_out/vinuri_calitate_min7.csv toate vinurile cu quality >= 7.
# Păstrați toate coloanele.
vinuri_bune = df[df["quality"] >= 7]

print("Numar vinuri cu quality >= 7: ")
print(vinuri_bune.shape[0])

vinuri_bune.to_csv("data_out/vinuri_calitate_min7.csv", index=False)

#Cerinta 4 ->Salvați în data_out/top50_alcool.csv cele 50 de vinuri
# cu cel mai mare alcohol, sortate descrescător.
df_sortat = df.sort_values(by="alcohol", ascending=False)
top50 = df_sortat.head(50)
top50.to_csv("data_out/top50_alcool.csv", index=False)

#Cerinta 5 -> Salvați în data_out/medii_pe_calitate.csv media coloanelor
# alcohol și pH pentru fiecare valoare a coloanei quality (un rând per notă de calitate).
medii = df.groupby("quality")[["alcohol", "pH"]].mean()

medii = medii.reset_index()
print(medii)
medii.to_csv("data_out/medii_pe_calitate.csv", index=False)

#Cerinta 6 -> Adăugați coloana aciditate_totala = fixed acidity + volatile acidity + citric acid.
#Salvați în data_out/vinuri_cu_aciditate.csv doar coloanele:
#quality, alcohol, aciditate_totala, pH.
df["aciditate_totala"] = (df["fixed acidity"] + df["volatile acidity"] + df["citric acid"])

rezultat = df[["quality", "alcohol", "aciditate_totala", "pH"]]
rezultat.to_csv("data_out/vinuri_cu_aciditate.csv", index=False)

#Cerinta 7 -> Determinați nota de calitate (quality) pentru care media alcohol este maximă.
#Salvați un fișier data_out/calitate_max_alcool.csv cu o singură coloană quality și o singură valoare.
medie_alcool_pe_calitate = df.groupby("quality")["alcohol"].mean()
calitate_max = medie_alcool_pe_calitate.idxmax()
rezultat = pd.DataFrame({"quality": [calitate_max]})
rezultat.to_csv("data_out/calitate_max_alcool.csv", index=False)

#Cerinta 8 -> Pentru coloanele:fixed acidity, volatile acidity, citric acid, alcohol, quality
#calculați matricea de corelație și salvați data_out/R.csv (cu nume de rând/coloană = numele variabilelor)
subset = df[ ["fixed acidity", "volatile acidity", "citric acid",
            "alcohol", "quality"]]
R = subset.corr()
print(R)
R.to_csv("data_out/R.csv")

#Cerinta 9 -> Creați alcohol_std = (alcohol − media) / deviația standard (populație sau eșantion — documentați în comentariu ce folosiți).
#Salvați data_out/alcohol_standardizat.csv cu coloanele alcohol, alcohol_std.
    #Pandas std() => ddof =1)

media = df["alcohol"].mean()
deviatia = df["alcohol"].std()

df["alcohol_std"]=(df["alcohol"]-media)/deviatia

rezultat = df[["alcohol", "alcohol_std"]]
rezultat.to_csv(
    "data_out/alcohol_standardizat.csv",
    index=False
)

#Cerinta 10 -> Pe primele 20 de vinuri și pe coloanele standardizate
#fixed acidity, volatile acidity, alcohol (standardizați fiecare coloană),
#calculați matricea distanțelor euclidiene 20×20 (scipy.spatial.distance.cdist sau formula voastră).
#Salvați data_out/d_euclid_20.csv. + Bonus

from scipy.spatial.distance import cdist

top20 = df.head(20).copy()
coloane = ["fixed activity", "volatile acidity", "alcohol"]
for c in coloane :
        media = top20[c].mean()
        dev = top20[c].std()

        top20[c] = (top20[c]-media)/dev
D = cdist(top20[coloane], top20[coloane], metric = "euclidiean")

salvare_matrice(D, range(20), range(20), "data_out/d_euclid_20.csv")


