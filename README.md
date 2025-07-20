# -AutoPublishing
# Telegram bot for automatic posting in Telegram groups 🤖💬

A Telegram bot that automatically posts messages to groups. You can set a time for each message, add multiple messages, and choose which groups each message will be posted to.


---

## 📦 Requirements
- Python 3.10+ 
- VPS or RDP to guarantee non-stop work


## 💠 Run bot on ubunto vps
- Clone the repo
```bash
  git clone https://github.com/radfx-2/AutoPublishing && cd AutoPublishing
```
- Install dependencies
```bash
pip install -r requirements.txt
```
- Edit the `env.example` file and add my operating information
   - We open the `env.example` file using `nano` or any other `editor`.
```bash
nano env.example
```
   - `API_KEY` API key from @BotFather
   - `SUDO` My ID is your Telegram account, you can get it from the bot @myidbot

- Run the bot
```bash
 python3 main.py
```
- Or I can run it in the background using the `screen`
```bash
 screen -dmS AutoPublishing python3 main.py
```
- You can change `AutoPublishing` to any name you want.


