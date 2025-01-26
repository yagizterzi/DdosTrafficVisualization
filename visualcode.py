import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv(r'C:\Users\yagiz\OneDrive\Masaüstü\Uygulamalar\kodlar\ddos_visuals\dataset\DDoS_dataset.csv')

# Display the first 10 rows of the dataset
print("First 10 rows of the dataset:")
print(data.head(10))

# Check for missing values in specific columns
print("Missing values in specific columns:")
print(data[['Source Port', 'Dest Port', 'Packet Length', 'Packets/Time', 'target']].isnull().sum())

# Drop rows with missing values in specific columns
data = data.dropna(subset=['Source Port', 'Dest Port', 'Packet Length', 'Packets/Time', 'target'])

# Check the unique values in 'Source Port' and 'Dest Port' columns
print("Unique values in 'Source Port' column:")
print(data['Source Port'].unique())
print("Unique values in 'Dest Port' column:")
print(data['Dest Port'].unique())

# Plot the distribution of normal vs DDoS traffic
target_counts = data['target'].value_counts()
target_counts.plot.pie(autopct='%1.1f%%', labels=['Normal', 'DDoS'], figsize=(8, 8))
plt.title('Normal vs DDoS Traffic')
plt.show()

# Plot the most common transport protocols
transport_counts = data['Transport Layer'].value_counts()
transport_counts = transport_counts.apply(lambda x: x / 1000)  # Convert counts to thousands
transport_counts.plot(kind='bar', figsize=(8, 5), color='skyblue')
plt.title('Most Common Transport Protocols')
plt.xlabel('Transport Protocol')
plt.ylabel('Frequency (in thousands)')
plt.show()

# Plot the top 10 targeted destination IPs for DDoS attacks
ddos_targets = data[data['target'] == 1]['Dest IP'].value_counts()
ddos_targets = ddos_targets.apply(lambda x: x/1000)  # Convert counts to thousands
ddos_targets.plot(kind='barh', figsize=(8, 5), color='orange')
plt.title('Top 10 Targeted Dest IPs (DDoS)')
plt.xlabel('Number of Attacks(in thousands)')
plt.ylabel('Destination IP')
plt.show()

# Plot the distribution of packet lengths
data['Packet Length'].plot(kind='hist', bins=30, figsize=(8, 5), color='green', alpha=0.7)
plt.title('Packet Length Distribution')
plt.xlabel('Packet Length')
plt.ylabel('Frequency')
plt.show()

# Create a scatter plot of source port vs destination port
scatter_data = data.groupby(['Source Port', 'Dest Port']).size().reset_index(name='counts')
print("Scatter plot data (first 5 rows):")
print(scatter_data.head())  # Debug: print the first 5 rows of scatter plot data

plt.figure(figsize=(12, 8))
plt.scatter(scatter_data['Source Port'], scatter_data['Dest Port'], s=scatter_data['counts'], alpha=0.5, c=scatter_data['counts'], cmap='YlGnBu')
plt.colorbar(label='Counts')
plt.title('Source Port vs Destination Port (Scatter Plot)')
plt.xlabel('Source Port')
plt.ylabel('Destination Port')
plt.show()

# Plot a boxplot comparing packet rates for normal traffic vs DDoS attacks
sns.boxplot(x='target', y='Packets/Time', data=data, palette='Set2')
plt.title('Packet Rates: Normal Traffic vs DDoS Attacks')
plt.xlabel('target (0=Normal, 1=DDoS)')
plt.ylabel('Packets/Time')
plt.show()

# Add a timestamp column to the dataset
data['Timestamp'] = pd.date_range(start='1/1/2021', periods=len(data), freq='T')

# Plot the traffic intensity over time
traffic_over_time = data.groupby(data['Timestamp'].dt.hour)['Packets/Time'].sum()
traffic_over_time.plot(kind='line', figsize=(10, 5), color='purple')
plt.title('Traffic Intensity Over Time')
plt.xlabel('Hour of the Day')
plt.ylabel('Total Packets Sent')
plt.show()

# Plot KDE of packet length distribution for normal traffic vs DDoS attacks
plt.figure(figsize=(10, 6))
sns.kdeplot(data=data[data['target'] == 0]['Packet Length'], label='Normal Traffic', fill=True, alpha=0.5, color='blue')
sns.kdeplot(data=data[data['target'] == 1]['Packet Length'], label='DDoS Attack', fill=True, alpha=0.5, color='red')
plt.title('Packet Length Distribution (KDE)')
plt.xlabel('Packet Length')
plt.ylabel('Density')
plt.legend()
plt.show()

# Plot KDE of packets/time distribution for normal traffic vs DDoS attacks
plt.figure(figsize=(10, 6))
sns.kdeplot(data=data[data['target'] == 0]['Packets/Time'], label='Normal Traffic', fill=True, alpha=0.5, color='green')
sns.kdeplot(data=data[data['target'] == 1]['Packets/Time'], label='DDoS Attack', fill=True, alpha=0.5, color='purple')
plt.title('Packets/Time Distribution (KDE)')
plt.xlabel('Packets/Time')
plt.ylabel('Density')
plt.legend()
plt.show()