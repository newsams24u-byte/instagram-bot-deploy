# 🤖 COMPLETE BANGALORE INSTAGRAM BOT SETUP GUIDE

**An AI-powered bot that automatically posts Bangalore content every 30 minutes!**

---

## 📋 What You Get

✅ **Automated Posting** - Every 30 minutes, completely automatic  
✅ **Multiple Content Types** - News, weather, traffic, metro, memes, polls  
✅ **AI Captions** - Claude generates unique captions each time  
✅ **Comment Replies** - Bot replies intelligently to follower comments  
✅ **Free APIs** - NewsAPI + OpenWeatherMap (no paid tiers)  
✅ **Personal Account** - Works with your Instagram account  
✅ **Custom Images** - Beautiful generated images for each post

---

## 🚀 SETUP: 5 EASY STEPS

### STEP 1️⃣: Get API Keys (5 minutes)

#### NewsAPI (for Bangalore news)

1. Open: https://newsapi.org/
2. Click "Get API Key"
3. Sign up with email
4. Verify email → Click link in inbox
5. Copy your API key from dashboard

#### OpenWeatherMap (for weather & rain alerts)

1. Open: https://openweathermap.org/api
2. Click "Sign Up"
3. Create account & verify
4. Go to "API Keys" tab
5. Copy your API key

**Time: ~5 minutes | Cost: $0** ✅

### STEP 2️⃣: Prepare Your Instagram Credentials (1 minute)

You'll need:

- Your Instagram **username** (e.g., `bengaluru_nagara`)
- Your Instagram **password**

⚠️ **Note:** The bot uses your personal account. Credentials are stored locally in `.env` file (never shared).

### STEP 3️⃣: Run the Setup Script (1 minute)

```bash
cd instagram_agent
chmod +x run_bot.sh
./run_bot.sh
```

### STEP 4️⃣: Enter Your Credentials

The script will ask:

```
Enter your Instagram username: bengaluru_nagara
Enter your Instagram password: ••••••••••
Enter your NewsAPI key: 1a2b3c4d5e...
Enter your OpenWeather API key: abc123def456...
```

### STEP 5️⃣: Watch It Post! 🎉

The bot will:

- ✅ Create `.env` configuration file
- ✅ Set up Python virtual environment
- ✅ Install all dependencies
- ✅ **Post your first content in ~30 seconds**
- ✅ **Continue posting every 30 minutes automatically**

---

## 📱 WHAT GETS POSTED

### Content Types (Random Rotation)

| Type              | Example                                               | Frequency |
| ----------------- | ----------------------------------------------------- | --------- |
| 📰 **News**       | "New Tech Hub Opens in Bangalore"                     | Random    |
| 🌤️ **Weather**    | "28°C, Partly Cloudy, 65% Humidity"                   | Random    |
| ☔ **Rain Alert** | "Rain coming in 4 hours! ⚠️ Umbrella time!"           | Random    |
| 🚗 **Traffic**    | "Silk Board: HEAVY - Construction work"               | Random    |
| 🚆 **Metro**      | "Purple Line: On Time ✅"                             | Random    |
| 😂 **Meme**       | "When you say traffic in Bangalore: 45 mins later..." | Random    |
| 🗳️ **Poll**       | "Best Bangalore biryani place? A·B·C"                 | Random    |

### Example Posts

**Weather Post:**

```
🌤️ BANGALORE WEATHER UPDATE ☀️

🌡️ Temperature: 28°C
💨 Humidity: 65%
Condition: Partly Cloudy

📍 Stay updated with Bangalore weather!

❓ How's the weather where you are?

#BangaloreWeather #WeatherUpdate #BangaloreToday
```

**Traffic Post:**

```
🚗 TRAFFIC UPDATE 🚗🚗

📍 Silk Board
Status: Heavy
Reason: Construction work

🛣️ Plan your route accordingly!
⏰ Leave early or take alternate routes

💬 Tag your commute struggle! 😩

#BangaloreTraffic #TrafficUpdate #Bangalore #Commute
```

**Meme Post:**

```
😂 When you say 'traffic' in Bangalore

Me: I'll be there in 10 mins
Reality: 45 mins later... 🚗

🤣 Tag someone this is about!
💬 Can you relate?

#BangaloreMemes #BangaloreLife #RelataBlLE
```

---

## 💬 AI COMMENT REPLIES

The bot automatically replies to comments with witty/sensible responses:

**Comment:** "Traffic is insane today 😫"  
**Bot:** "Tell us about it! Everyone's a Formula 1 driver 🏎️ Where were you stuck?"

**Comment:** "Love this weather!"  
**Bot:** "Perfect day to explore Bangalore! ☀️ What's your plan?"

**Comment:** "Meme is SO relatable!"  
**Bot:** "RIGHT?? Tag someone who needs to see this! 😂"

---

## 📂 FILE STRUCTURE

```
instagram_agent/
├── bot_agent.py                    # Main orchestrator
├── content_fetcher.py              # News, weather, traffic, metro, memes, polls
├── advanced_content_generator.py   # AI captions + comment replies
├── advanced_image_creator.py       # Image generation
├── instagram_poster.py             # Instagram posting
├── comment_reply_bot.py            # Comment engagement
├── requirements.txt                # Python dependencies
├── .env                            # Your credentials (auto-created)
├── run_bot.sh                      # Launcher script
├── posts/                          # Generated images saved here
├── BOT_SETUP.md                    # Full documentation
├── QUICK_START.md                  # Quick reference
└── COMPLETE_SETUP.md               # This file
```

---

## ⚙️ HOW IT WORKS

### Every 30 Minutes:

```
1. Fetch Random Content
   ├─ Bangalore news (NewsAPI)
   ├─ Current weather (OpenWeatherMap)
   ├─ Rain forecast
   ├─ Generate traffic update
   ├─ Generate metro status
   ├─ Generate meme
   └─ Generate poll

2. Generate AI Caption
   ├─ Create unique caption with Claude AI
   ├─ Add viral hashtags
   ├─ Include engagement hook
   └─ Format for Instagram

3. Create Image
   ├─ Generate content-specific design
   ├─ Add title/data overlay
   ├─ Apply beautiful gradients
   └─ Save as Instagram-ready PNG

4. Post to Instagram
   ├─ Upload image via Instagrapi
   ├─ Add caption with hashtags
   └─ Publish live 🎉

5. Save Post Info
   └─ Store media ID for engagement

Every 2.5 Hours:

6. Engage with Followers
   ├─ Read recent comments
   ├─ Generate witty replies
   └─ Post replies automatically
```

---

## 🔧 CUSTOMIZATION

### Change Post Interval

Edit `.env`:

```env
POST_INTERVAL_MINUTES=15    # Post every 15 minutes instead of 30
```

### Disable Comment Replies

Edit `.env`:

```env
REPLY_TO_COMMENTS=false     # Disable auto-replies
```

### Change Max Replies Per Post

Edit `.env`:

```env
MAX_REPLIES_PER_POST=10     # Reply to 10 comments instead of 5
```

### Add Custom Content Type

1. Add method to `content_fetcher.py`
2. Add caption generator to `advanced_content_generator.py`
3. Add image creator to `advanced_image_creator.py`

---

## 🎯 HASHTAG STRATEGY

The bot includes 15+ relevant hashtags per post:

**News:** #BangaloreNews #NewsAlert #BangaloreUpdates  
**Weather:** #BangaloreWeather #WeatherUpdate #BangaloreToday  
**Traffic:** #BangaloreTraffic #Commute #RoadToFreedom  
**Metro:** #BangaloreMetro #CommuteLife #BangaloreTransport  
**Memes:** #BangaloreMemes #BangaloreLife #RelataBlLE  
**Engagement:** #CommunityChoice #YourOpinionMatters #DontMissOut

---

## 🚦 TROUBLESHOOTING

### Issue: "ModuleNotFoundError"

**Solution:**

```bash
pip install -r requirements.txt
```

### Issue: "Instagram login failed"

**Solution:**

1. Verify username & password in `.env`
2. Try logging in manually on Instagram first
3. Check if 2FA is enabled (might need app password)

### Issue: "API Key Invalid"

**Solution:**

1. Double-check key is copied completely (no spaces/newlines)
2. Verify key works on the API website
3. Regenerate key if needed

### Issue: "No posts appearing"

**Solution:**

1. Check internet connection
2. Verify all API keys in `.env`
3. Check `posts/` folder for generated images
4. Look at terminal for error messages

### Issue: "Image creation fails"

**Solution:**

```bash
mkdir -p posts
```

---

## 📊 FREE API LIMITS

| API              | Free Tier        | Limit                       | Status |
| ---------------- | ---------------- | --------------------------- | ------ |
| NewsAPI          | 100 requests/day | Enough for 30-min intervals | ✅     |
| OpenWeatherMap   | 60 calls/min     | Plenty for posting          | ✅     |
| Anthropic Claude | Pay-as-you-go    | ~$0.03/day for captions     | ✅     |
| Instagram        | Free             | No limits                   | ✅     |

**Total Monthly Cost: ~$1 for AI captions** (Or $0 if using free caption templates)

---

## 🎨 CONTENT VARIETY

### Daily Content Mix (Random)

- 30% News
- 20% Weather/Rain
- 15% Traffic
- 15% Metro
- 15% Memes/Polls
- 5% Special posts

### Weekly Engagement

- 💬 Replies to 50-100 comments
- 🎯 High engagement rates
- 🔄 Builds community

---

## 📈 GROWTH TIPS

1. **Post Consistently** - Bot posts every 30 mins (automatic)
2. **Engage With Comments** - Bot replies automatically
3. **Use Hashtags** - 15+ hashtags per post
4. **Share Quality Content** - Mix of useful + entertaining
5. **Ask Questions** - Captions include engagement hooks
6. **Tag Followers** - Encourage tagging in comments

---

## 🎬 STARTING THE BOT

### First Time:

```bash
cd instagram_agent
chmod +x run_bot.sh
./run_bot.sh
```

### Subsequent Times:

```bash
cd instagram_agent
./run_bot.sh
```

### Stop Anytime:

```
Press Ctrl+C in terminal
```

---

## ✅ VERIFICATION CHECKLIST

Before running, make sure:

- [ ] Instagram username & password ready
- [ ] NewsAPI key obtained (https://newsapi.org/)
- [ ] OpenWeather API key obtained (https://openweathermap.org/api)
- [ ] `.env` file created (or auto-created by script)
- [ ] Internet connection working
- [ ] Python 3.7+ installed

---

## 🚀 QUICK START

```bash
# 1. Navigate to bot folder
cd instagram_agent

# 2. Make script executable
chmod +x run_bot.sh

# 3. Run the bot
./run_bot.sh

# 4. Enter credentials when prompted
# 5. Watch it post!
```

**That's it! The bot handles everything else.** 🎉

---

## 📞 SUPPORT

- **Check `.env`** - Verify all credentials
- **Check terminal output** - Error messages are clear
- **Review API keys** - Make sure they're valid
- **Restart bot** - Sometimes fixes issues

---

## 🎯 FINAL NOTES

✅ **Fully Automatic** - No manual posting needed  
✅ **AI-Powered** - Each caption is unique  
✅ **Community-Focused** - Bangalore-local content  
✅ **Engagement-Driven** - Auto-replies to comments  
✅ **Cost-Effective** - Free APIs + minimal AI cost  
✅ **24/7 Operation** - Runs continuously

---

**Ready? Let's make your Instagram account blow up! 🚀**

👉 **Next step: Get your API keys and run `./run_bot.sh`**

---

_Made with ❤️ for Bangalore_  
_Automate • Engage • Grow_
