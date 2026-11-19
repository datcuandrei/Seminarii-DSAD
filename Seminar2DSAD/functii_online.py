def nan_replace_df(tabel):
    for coloana in tabel.select_dtypes(include='number').columns:
            media = tabel[coloana].mean()
            tabel[coloana]=tabel[coloana].fillna(media)
    return tabel
import pandas as pd

def salvare_matrice (x, index_linie, index_coloana, fisier):
    df=pd.DataFrame(x, index=index_linie, columns=index_coloana)
    df.to_csv(fisier)