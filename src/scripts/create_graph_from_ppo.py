import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file, skipping blank lines
file_path = "./progress_extended.csv"
df = pd.read_csv(file_path, skip_blank_lines=True)

# Drop completely empty rows if any slipped through
df.dropna(how="all", inplace=True)

# Extract the reward column
reward_col = "env_runners/episode_return_mean"
rewards = df[reward_col].dropna().values

# Apply a moving average smoothing
window = 10
avg_rewards_smooth = pd.Series(rewards).rolling(window=window).mean()

# Plot the smoothed rewards
plt.figure()
plt.plot(range(len(avg_rewards_smooth)), avg_rewards_smooth, label=f"Moving Avg (window={window})", color="black")
plt.xlabel("Episode")
plt.ylabel("Average Reward")
plt.title("Smoothed Average Reward Over Episodes")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("avg_reward_smooth_ppo.png")
