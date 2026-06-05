# 🤖 ADVANCED BANGALORE INSTAGRAM BOT

**A powerful, fully-automated AI agent that posts Bangalore-local content to Instagram every 30 minutes!**

## ✨ What It Posts

✅ **Bangalore News** - Latest local news from NewsAPI  
✅ **Weather Updates** - Real-time temp, humidity, conditions  
✅ **Rain Alerts** - "It's going to rain!" warnings with umbr ☔  
✅ **Traffic Updates** - Silk Board, Whitefield, MG Road etc.  
✅ **Metro Status** - Purple, Green, Red, Blue lines  
✅ **Local Memes** - Bangalore traffic, weather, startup culture 😂  
✅ **Polls** - "Best Bangalore biryani?", weather preferences

## 💬 AI Comment Replies

The bot automatically replies to comments with:

- **Witty responses** - Humorous, relatable Bangalore jokes
- **Sensible feedback** - Engaging questions to boost engagement
- **Emoji usage** - Strategic emojis for personality
- **Smart tagging** - Call to action, tag a friend etc.

## 🎯 Key Features

✅ **Multiple Content Types** - 7 different post styles  
✅ **Custom Images** - Auto-generated for each content type  
✅ **AI Captions** - Claude generates unique captions  
✅ **Auto-Reply** - Responds to comments intelligently  
✅ **Free APIs Only** - NewsAPI + OpenWeather (no paid tiers needed)  
✅ **Personal Account** - Works with your Instagram account  
✅ **Fully Automatic** - Runs 24/7 with no manual intervention

## 📋 What You Need

### From Your Side (Just 2 Things)

1. **Instagram Credentials**
   - Your Instagram username
   - Your Instagram password
   - (They're stored securely in `.env`, never shared)

2. **Free API Keys** (Takes 5 minutes each)
   - **NewsAPI**: https://newsapi.org/ (Sign up → Get key)
   - **OpenWeatherMap**: https://openweathermap.org/api (Sign up → Get key)

### Free Tier Limits

- NewsAPI: 100 requests/day (more than enough for 30-min intervals)
- OpenWeather: 1000 calls/day (plenty!)
- **Total Cost: $0** ✅

## 🚀 Quick Setup (3 Minutes)

```bash
cd instagram_agent

# Run the setup script
chmod +x run_bot.sh
./run_bot.sh
```

It will ask for:

1. Instagram username
2. Instagram password
3. NewsAPI key
4. OpenWeather API key

Then **automatically**:

- Creates `.env` file
- Sets up virtual environment
- Installs dependencies
- Starts posting! 🎉

## 🎬 How It Works

**Every 30 minutes (completely automatic):**

1. **Fetch Random Content**
   - News from NewsAPI
   - Weather from OpenWeather
   - Traffic/Metro/Meme generators

2. **Generate Caption**
   - Claude AI creates unique text
   - Adds viral hashtags (#BangaloreNews, #BangaloreTraffic)
   - Includes engagement hook ("What do you think?")

3. **Create Image**
   - Content-specific design
   - Beautiful gradients & colors
   - Text overlay with title/data

4. **Post to Instagram**
   - Uses Instagrapi (personal account)
   - Caption with hashtags published
   - Image saved for history

5. **Reply to Comments** (Every 2.5 hours)
   - Bot reads recent comments
   - Generates witty/sensible replies
   - Posts replies automatically

## 📱 Example Posts

### Weather Post

```
🌤️ BANGALORE WEATHER UPDATE ☀️

🌡️ Temperature: 28°C
💨 Humidity: 65%
Condition: Partly Cloudy

📍 Stay updated with Bangalore weather!

❓ How's the weather where you are?

#BangaloreWeather #WeatherUpdate #BangaloreToday #IndiaWeather
```

### Traffic Post

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

### Meme Post

```
😂 When you say 'traffic' in Bangalore

Me: I'll be there in 10 mins
Reality: 45 mins later...

🤣 Tag someone this is about!
💬 Can you relate?

#BangaloreMemes #BangaloreLife #Relatable
```

## 🎨 Content Variety (7 Types)

| Type          | Frequency | Example                         |
| ------------- | --------- | ------------------------------- |
| 📰 News       | Random    | "New Tech Hub Opens"            |
| 🌤️ Weather    | Random    | "28°C, Partly Cloudy"           |
| ☔ Rain Alert | Random    | "Rain coming! ⚠️"               |
| 🚗 Traffic    | Random    | "Silk Board: Heavy"             |
| 🚆 Metro      | Random    | "Purple Line: On Time"          |
| 😂 Meme       | Random    | "Bangalore traffic = nightmare" |
| 🗳️ Poll       | Random    | "Best biryani place?"           |

## 💬 AI Comment Replies (Examples)

**Comment:** "Traffic is insane today 😫"  
**Bot reply:** "Tell us about it! Everyone's a Formula 1 driver 🏎️ Where were you stuck?"

**Comment:** "Rain prediction wrong again!"  
**Bot reply:** "Mother Nature changes her mind 🌧️☀️ Classic Bangalore move! Did you get caught?"

**Comment:** "I love metro!"  
**Bot reply:** "Metro > Traffic always! 🚆✨ Which line do you use?"

## 🛠️ Customization

### Change Post Frequency

Edit `.env`:

```
POST_INTERVAL_MINUTES=15  # Post every 15 minutes instead of 30
```

### Add More Hashtags

Edit `advanced_content_generator.py` and add to `self.viral_hashtags`

### Change Reply Personality

Modify `advanced_content_generator.py` → `_get_fallback_reply()` method

### Add New Content Types

Add methods to `content_fetcher.py` following the existing pattern

### Customize Image Styles

Modify `advanced_image_creator.py` color schemes and fonts

## 📂 File Structure

```
instagram_agent/
├── bot_agent.py                    ← Main orchestrator
├── content_fetcher.py              ← All content sources
├── advanced_content_generator.py   ← AI captions + replies
├── advanced_image_creator.py       ← Image generation
├── instagram_poster.py             ← Instagram posting
├── comment_reply_bot.py            ← Comment engagement
├── requirements.txt                ← Dependencies
├── .env                            ← Your credentials
├── run_bot.sh                      ← Launcher script
└── posts/                          ← Generated images
```

## 🚦 Getting API Keys (5 Minutes)

### NewsAPI

1. Go to https://newsapi.org/
2. Click "Get API Key"
3. Enter email → Check inbox → Click link
4. Copy your API key from dashboard

### OpenWeatherMap

1. Go to https://openweathermap.org/api
2. Click "Sign Up" → Create account
3. Go to API keys tab
4. Copy default key or create new one

## ⚙️ Troubleshooting

**"ModuleNotFoundError"**

```bash
pip install -r requirements.txt
```

**"Instagram login failed"**

- Verify username/password in `.env`
- Check if 2FA is enabled (might need app password)
- Try: `python3 -c "from instagrapi import Client; cl = Client(); cl.login('user', 'pass')"`

**"API key invalid"**

- Verify key in `.env` file
- Check key is copied completely (no spaces)
- Test key on API website

**"No content posted"**

- Check internet connection
- Verify all API keys are valid
- Check `posts/` folder has images
- Look at terminal output for errors

## 🎯 Advanced Features

### Enable Comment Replies

Already enabled by default! Check `.env`:

```
REPLY_TO_COMMENTS=true
MAX_REPLIES_PER_POST=5
```

### Add Your Own Content

Create new method in `content_fetcher.py`:

```python
def get_custom_content(self):
    return {
        "type": "custom",
        "title": "Your title",
        "description": "Your description"
    }
```

### Schedule Different Intervals

Edit bot_agent.py scheduler to set different intervals for different tasks

## 📊 What Gets Posted

**Weekly Distribution** (Random):

- 30% News
- 20% Weather/Rain
- 15% Traffic
- 15% Metro
- 15% Memes/Polls
- 5% Other

## 🎉 You're All Set!

Run the bot and watch it post Bangalore content automatically! 🚀

**The bot will:**

- ✅ Post within 1 minute of startup
- 🔄 Post every 30 minutes automatically
- 💬 Reply to comments intelligently
- 📱 Create custom images each time
- 🌍 Use real-time weather & traffic data

---

**Made with ❤️ for Bangalore**  
_Automate, engage, grow your Instagram 📈_
