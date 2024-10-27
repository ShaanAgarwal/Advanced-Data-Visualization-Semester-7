import pandas as pd
from scipy.stats import pearsonr

# Load the dataset
data = pd.read_csv('insurance.csv')

# Calculate Pearson correlation coefficient for BMI vs Charges
bmi = data['bmi']
charges = data['charges']
bmi_charges_corr, bmi_charges_p_value = pearsonr(bmi, charges)

# Calculate Pearson correlation coefficient for Age vs Charges
age = data['age']
age_charges_corr, age_charges_p_value = pearsonr(age, charges)

# Print the results
print(f"BMI vs Charges: Correlation Coefficient = {bmi_charges_corr:.4f}, P-value = {bmi_charges_p_value:.4f}")
print(f"Age vs Charges: Correlation Coefficient = {age_charges_corr:.4f}, P-value = {age_charges_p_value:.4f}")

# Interpretation of the P-value
alpha = 0.05
if bmi_charges_p_value < alpha:
    print("There is a significant correlation between BMI and Charges.")
else:
    print("There is no significant correlation between BMI and Charges.")

if age_charges_p_value < alpha:
    print("There is a significant correlation between Age and Charges.")
else:
    print("There is no significant correlation between Age and Charges.")