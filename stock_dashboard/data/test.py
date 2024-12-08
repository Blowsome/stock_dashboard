import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample DataFrame (replace this with your actual dataframe)
data = {
    'Ticker': ['AAPL', 'AAPL', 'AAPL', 'GOOG', 'GOOG', 'MSFT', 'MSFT'],
    'Date': ['2024-12-01', '2024-12-01', '2024-12-02', '2024-12-01', '2024-12-02', '2024-12-01', '2024-12-02'],
    'Stock Price': [150, 152, 155, 2800, 2850, 300, 305]
}
df = pd.DataFrame(data)

print(df)

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Group by Date and calculate the mean, 25th percentile and 75th percentile for stock price
daily_stats = df.groupby('Date')['Stock Price'].agg(
    ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]
).reset_index()

# Rename columns for clarity
daily_stats.columns = ['Date', 'Mean Price', '25th Percentile', '75th Percentile']

# Plotting using seaborn
plt.figure(figsize=(10, 6))

# Plot the Mean Price, 25th, and 75th Percentiles
sns.lineplot(data=daily_stats, x='Date', y='Mean Price', label='Mean Price', color='blue')
sns.lineplot(data=daily_stats, x='Date', y='25th Percentile', label='25th Percentile', color='green', linestyle='--')
sns.lineplot(data=daily_stats, x='Date', y='75th Percentile', label='75th Percentile', color='red', linestyle='--')

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.title('Stock Price Trends with Percentiles')
plt.legend()

# Display the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
