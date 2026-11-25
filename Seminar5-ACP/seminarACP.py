import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

folder = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(folder, "Wholesale customers data.csv"))

# ---------------------------------------------------------------------------
# 1. Load the dataset and select the six spending variables.
coloane = ["Fresh", "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen"]
X = df[coloane]

# ---------------------------------------------------------------------------
# 2. Standardize the variables.
X_std = pd.DataFrame(StandardScaler().fit_transform(X), columns=coloane)

# ---------------------------------------------------------------------------
# 3. Create the correlation matrix using seaborn.
corelatii = X_std.corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corelatii, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Matricea de corelatie")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
# 4. Apply PCA and calculate the explained variance ratio for each component.
pca = PCA()
pca.fit(X_std)

varianta = pca.explained_variance_ratio_
varianta_cumulata = np.cumsum(varianta)

tabel = pd.DataFrame({
    "Componenta": [f"PC{i + 1}" for i in range(len(varianta))],
    "Varianta explicata": varianta.round(4),
    "Varianta cumulata": varianta_cumulata.round(4),
})
print(tabel.to_string(index=False))

# ---------------------------------------------------------------------------
# 5. Determine how many components are necessary to explain at least 80%
# of the total variance.
n_componente = int(np.argmax(varianta_cumulata >= 0.80) + 1)
print(f"\nComponente necesare pentru cel putin 80% din varianta: {n_componente}")