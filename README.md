# Auto-Advertiser Bot

## 🚀 Deployment Instructions

### 🌐 Hosting (Railway)
1. Create a new project on [Railway](https://railway.app/).
2. Connect your GitHub repo (push your code to GitHub first).
3. Select the `requirements.txt` file and choose the Python runtime.
4. Deploy the app.

### 🧠 How It Works
- Admins generate keys via `/generatekeyv1`, `/generatekeyv2`, `/generatekeyv3`.
- Users redeem keys via `/panel` to unlock features.
- Users can add user tokens, configure campaigns, and schedule messages.
- The bot enforces plan limits (e.g., V2: 2 users, 8 channels).
- Keys expire after 1 month and cannot be reused.

### 🛠️ How to Use
1. Run `python main.py` to test locally.
2. Replace `YOUR_BOT_TOKEN` in `config.json`.
3. Deploy to Railway or your preferred host.
