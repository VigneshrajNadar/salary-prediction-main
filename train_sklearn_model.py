import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression

# Load data
DATA_PATH = 'salary prediction.csv'
data = pd.read_csv(DATA_PATH)

# Drop irrelevant columns
cols_to_drop = ['FIRST NAME','LAST NAME','DOJ', 'CURRENT DATE','LEAVES USED','LEAVES REMAINING']
data = data.drop(cols_to_drop, axis=1)

# Fill missing values for RATINGS and AGE
import numpy as np
choices = data['RATINGS'].dropna().unique()
data['RATINGS'] = data['RATINGS'].apply(lambda x: float(np.random.choice(choices)) if pd.isnull(x) else x)
choices_age = data['AGE'].dropna().unique()
data['AGE'] = data['AGE'].apply(lambda x: float(np.random.choice(choices_age)) if pd.isnull(x) else x)

# Load encoders and scaler
with open('label_encoder_sex.pkl','rb') as file:
    label_encoder_sex = pickle.load(file)
with open('onehot_encoder_des.pkl','rb') as file:
    onehot_encoder_des = pickle.load(file)
with open('onehot_encoder_unit.pkl','rb') as file:
    onehot_encoder_unit = pickle.load(file)
with open('scaler.pkl','rb') as file:
    scaler = pickle.load(file)
with open('feature_order.pkl', 'rb') as f:
    feature_order = pickle.load(f)

# Encode features
# SEX
data['SEX'] = label_encoder_sex.transform(data['SEX'])
# DESIGNATION
dev_encoded = onehot_encoder_des.transform(data[['DESIGNATION']]).toarray()
dev_encoded_df = pd.DataFrame(dev_encoded, columns=onehot_encoder_des.get_feature_names_out(['DESIGNATION']))
# UNIT
unit_encoded = onehot_encoder_unit.transform(data[['UNIT']]).toarray()
unit_encoded_df = pd.DataFrame(unit_encoded, columns=onehot_encoder_unit.get_feature_names_out(['UNIT']))
# Remove DESIGNATION and UNIT from the original DataFrame
data = data.drop(['DESIGNATION', 'UNIT'], axis=1)
# Combine all features
data = pd.concat([data.reset_index(drop=True), dev_encoded_df, unit_encoded_df], axis=1)
# Reorder columns
X = data[feature_order]
y = data['SALARY']
# Scale features
X_scaled = scaler.transform(X)

# Train model
model = LinearRegression()
model.fit(X_scaled, y)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Trained and saved model.pkl') 