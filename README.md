# Instagram News Agent 📸🤖

An AI-powered agent that automatically posts trending Bangalore/India news to Instagram every 30 minutes with AI-generated captions, viral hashtags, and custom images.

## Features

✅ **Automatic News Fetching** - Gets latest Bangalore news, falls back to India news  
✅ **AI Caption Generation** - Uses Claude to create engaging captions with viral hashtags  
✅ **Engagement Hooks** - Adds CTAs like "What do you think?" for user interaction  
✅ **Custom Image Creation** - Generates Instagram-ready images (1080x1350) with titles  
✅ **Scheduled Posting** - Posts automatically every 30 minutes  
✅ **Two Posting Methods**:

- Instagram Graph API (Business Accounts) - Recommended
- Instagrapi (Personal Accounts)

## Setup Instructions

### 1. Install Dependencies

```bash
cd instagram_agent
pip install -r requirements.txt
```

### 2. Get API Keys

#### NewsAPI Key (for fetching news)

1. Go to https://newsapi.org/
2. Sign up for free
3. Get your API key from dashboard

#### Anthropic API Key (for AI captions)

1. Go to https://console.anthropic.com/
2. Sign up and create API key
3. Copy your API key

#### Instagram Credentials (2 Options)

**Option A: Business Account (Recommended) - Instagram Graph API**

1. Create a Facebook App: https://developers.facebook.com/
2. Get Instagram Business Account ID
3. Generate long-lived access token
4. Use credentials in .env

**Option B: Personal Account - Using Instagrapi**

1. Simply use your Instagram username and password
2. Note: Enable "Less secure app access" if needed

### 3. Configure .env File

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Option 1: Business Account (Graph API)
INSTAGRAM_ACCESS_TOKEN=your_long_lived_access_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_business_account_id

# Option 2: Personal Account
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# API Keys
NEWSAPI_KEY=your_newsapi_key
ANTHROPIC_API_KEY=your_anthropic_key

# Settings
POST_INTERVAL_MINUTES=30
```

### 4. Run the Agent

```bash
python main_agent.py
```

The agent will:

- ✅ Post immediately on startup
- 🔄 Post every 30 minutes automatically
- 📤 Upload images to Instagram with captions
- 📱 Add viral hashtags and engagement captions

Press `Ctrl+C` to stop.

## How It Works

```
┌─────────────────────────────────────┐
│  Fetch Bangalore News (NewsAPI)     │
│  → Falls back to India News         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  AI Caption Generation (Claude)     │
│  - Main caption (140 chars)         │
│  - Engagement hook                  │
│  - Viral hashtags                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Create Instagram Image             │
│  - Title: Article title             │
│  - Subtitle: Description            │
│  - Decorative elements              │
│  - Save as 1080x1350 PNG            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Post to Instagram (via API)        │
│  - Upload image                     │
│  - Add caption with hashtags        │
│  - Publish publicly                 │
└─────────────────────────────────────┘
```

## Auto-Posting Mechanism

**Yes, it's fully automatic!**

- Uses **APScheduler** for background scheduling
- Runs every 30 minutes (configurable)
- No manual intervention needed
- Uses **APIs** (not browser automation)
  - NewsAPI for news fetching
  - Claude API for AI caption generation
  - Instagram Graph API or Instagrapi for posting

## Folder Structure

```
instagram_agent/
├── main_agent.py              # Main scheduler and orchestrator
├── news_fetcher.py            # Fetch Bangalore/India news
├── content_generator.py       # AI caption + hashtags
├── image_creator.py           # Create Instagram images
├── instagram_poster.py        # Post to Instagram
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── .env                       # Your credentials (gitignored)
└── posts/                     # Generated images saved here
```

## Customization

### Change posting interval

Edit `.env`:

```env
POST_INTERVAL_MINUTES=15  # Post every 15 minutes
```

### Customize image style

Edit `image_creator.py`:

- Change colors, fonts, layout
- Add logo/branding
- Adjust gradient effects

### Add more hashtags

Edit `content_generator.py`:

```python
self.viral_hashtags = [
    "#YourHashtag1",
    "#YourHashtag2",
    # ... add more
]
```

### Change news sources

Edit `news_fetcher.py` to:

- Query different regions
- Use different news keywords
- Add multiple news sources

## Troubleshooting

**"ModuleNotFoundError"**

```bash
pip install -r requirements.txt
```

**"OSError: Cannot save file"**

```bash
mkdir -p posts
```

**"API Rate Limit Exceeded"**

- NewsAPI has rate limits on free tier
- Increase posting interval in `.env`
- Or upgrade your NewsAPI plan

**"Instagram posting fails"**

- Verify credentials in `.env`
- Check if 2FA is enabled (Graph API recommended)
- Ensure business account is properly connected

## API Costs

- **NewsAPI**: Free tier = 100 requests/day ✅
- **Anthropic (Claude)**: ~$0.001 per post (~$0.03/day at 30-min intervals)
- **Instagram Graph API**: Free ✅

**Total Cost**: ~$1/month for AI captions

## Support

For issues:

1. Check `.env` credentials
2. Review API key validity
3. Check logs in terminal
4. Verify folder `posts/` exists

---

**Made with ❤️ for automated Instagram news posting**
