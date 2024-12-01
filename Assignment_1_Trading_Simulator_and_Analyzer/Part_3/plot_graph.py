import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("daily_cashflow.csv")

df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")

plt.figure(figsize=(10, 6))
plt.plot(df["Date"], df["Cashflow"])
plt.title("Daily Cashflow")
plt.xlabel("Date")
plt.ylabel("Cashflow")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("plot.png")
