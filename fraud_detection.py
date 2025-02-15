import pandas as pd

# Load dataset
df = pd.read_excel("single_user_transactions.xlsx")

# Convert transaction_time to datetime
df['transaction_time'] = pd.to_datetime(df['transaction_time'])

# Rule 1: Flag high-value transactions (5x higher than user’s average)
df['avg_spending'] = df['amount'].mean()
df['high_amount_flag'] = df['amount'] > (df['avg_spending'] * 5)

# Rule 2: Detect rapid transactions (more than 5 transactions in 10 minutes)
df = df.sort_values(by='transaction_time')
df['time_diff'] = df['transaction_time'].diff().dt.total_seconds()
df['rapid_transaction_flag'] = df['time_diff'] < 600  # 600 seconds = 10 minutes

# Rule 3: Transactions from unusual locations
usual_locations = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami', 'San Francisco', 'Dallas']
df['unusual_location_flag'] = ~df['location'].isin(usual_locations)

# Create a fraud score
df['fraud_score'] = df[['high_amount_flag', 'rapid_transaction_flag', 'unusual_location_flag']].sum(axis=1)

# Save suspicious transactions
suspicious_transactions = df[df['fraud_score'] >= 2]
suspicious_transactions.to_excel("suspicious_transactions.xlsx", index=False)

print("Fraud detection completed. Suspicious transactions saved.")
