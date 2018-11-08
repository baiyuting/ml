from collections import Counter

from imblearn.over_sampling import SMOTE

data = []
target = []
smo = SMOTE(random_state=42)
X_smo, y_smo = smo.fit_sample(data, target)
print(Counter(y_smo))
