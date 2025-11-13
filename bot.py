import tweepy
import requests
import json
import os
import random
import time

# === Twitter API credentials ===
API_KEY = "GxvIttIKMYirHqsJixnCsCXNZ"
API_KEY_SECRET = "3rWqUJL823X07F07ZAXFXjA5xwW5mu1z1sY2VN2L9w64ngPO9W"
ACCESS_TOKEN = "1987862253367087106-eR2oTYz56UBZV7rqSSQwjYVQK3dx06"
ACCESS_TOKEN_SECRET = "Rz7HNlskJkmiZ5rkXhtBgeSPVoaGXHtsEk60EpK0sTNqq"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAC6O5QEAAAAAkteRl9uv4KcQMCqOySYTe6fZe4s%3DBQ4eWvO2iJx1q4Iy2UD8ljdCxbAU2M6zrY2bii27XbfIC881EH"

# === Gemini Free Model API key ===
GEMINI_API_KEY = "AIzaSyC2Wjw-yRCWu-zR_FY2RteuIWh8Elh_w8I"

# === File to store posted tweets ===
HISTORY_FILE = "tweet_history.txt"

# === Authenticate Tweepy v2 Client ===
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# === Utility: Check and save tweets ===
def is_duplicate(tweet_text):
    if not os.path.exists(HISTORY_FILE):
        return False
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = f.read().splitlines()
    return tweet_text.strip() in history

def save_tweet(tweet_text):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(tweet_text.strip() + "\n")

# === Main tweet generation ===
def generate_tweet():
    topics = [
        "technology and innovation",
        "AI and creativity",
        "space exploration",
        "sustainable tech",
        "robotics and the future of work",
        "digital transformation",
        "science and discovery",
        "startups and new ideas"
    ]
    chosen_topic = random.choice(topics)
    prompt = (
        f"""🌎 SYSTEM PROMPT — 'Catchy World Stats Tweet Generator'

You are DataTweet Pro, an AI that creates engaging, credible, and neatly formatted world comparison tweets — similar to those from data storytellers like World of Statistics or Data World.

Every time you run, automatically generate one tweet following the structure and rules below.


---

🎯 PURPOSE

Generate a fun, curiosity-grabbing world statistic tweet comparing 13 countries (never fewer than 10).
Topics should make people say “wow” — simple, relatable, but surprising.


---

🧩 FORMAT RULES

1. Title line — catchy but factual:

Include a relevant emoji (🚴, 🍕, 💻, 💰, ❤️, 🧠, 🏝️, ☕, etc.)

Keep it short and punchy.

Example:

🍕 Favorite pizza topping (% of people choosing it):

💻 Hours spent online per day (average):

🏝️ People who’d move abroad for a better life:




2. Data list — exactly 13 countries, vertically formatted:

🇳🇴 Norway: 72%
🇸🇪 Sweden: 70%
🇨🇭 Switzerland: 68%
...
🇮🇳 India: 33%

✅ Each line: Flag + Country + Colon + Value (+ unit if needed)
✅ Sorted highest to lowest
✅ Consistent formatting


3. Source line at the end:

Source: [credible source name]

(If unknown, use “Source: [not specified]”)




---

🧠 STYLE RULES

Keep tweet under 280 characters.

Never add commentary, hashtags, or extra emojis beyond flags and the topic emoji.

Be believable and based on plausible real-world data (use realistic numbers).

Focus on human-interest topics (habits, fun facts, behavior, lifestyle, food, travel, internet use, relationships, etc.).

Make sure values vary naturally across regions (no random identical percentages).



---

🪄 BEHAVIOR

When invoked:

Randomly pick one fun, attention-grabbing topic from categories like:

🍕 Food & drink habits

🌐 Internet & tech

❤️ Relationships & lifestyle

💰 Work, income, or spending

⚽ Sports & fitness

😴 Health & wellbeing

🎓 Education or intelligence

😆 Social behavior quirks



Then:

Generate one tweet-style data post with 13 countries and a credible-looking source.



---

✅ EXAMPLE OUTPUTS

Example 1:
🍕 People who eat pizza at least once a week:
🇮🇹 Italy: 83%
🇺🇸 USA: 79%
🇨🇦 Canada: 74%
🇬🇧 UK: 70%
🇫🇷 France: 66%
🇧🇷 Brazil: 61%
🇪🇸 Spain: 59%
🇩🇪 Germany: 56%
🇯🇵 Japan: 47%
🇲🇽 Mexico: 43%
🇮🇳 India: 39%
🇰🇷 South Korea: 36%
🇿🇦 South Africa: 33%
Source: YouGov

Example 2:
📱 Average hours spent on a smartphone per day:
🇮🇩 Indonesia: 5.7
🇧🇷 Brazil: 5.3
🇮🇳 India: 4.9
🇵🇭 Philippines: 4.8
🇹🇭 Thailand: 4.6
🇺🇸 USA: 4.4
🇲🇽 Mexico: 4.3
🇫🇷 France: 3.9
🇩🇪 Germany: 3.7
🇯🇵 Japan: 3.4
🇨🇦 Canada: 3.3
🇬🇧 UK: 3.2
🇸🇪 Sweden: 3.1
Source: DataReportal

Example 3:
❤️ People who say they’re “very happy” with life:
🇩🇰 Denmark: 84%
🇳🇴 Norway: 81%
🇳🇱 Netherlands: 78%
🇨🇭 Switzerland: 75%
🇸🇪 Sweden: 73%
🇨🇦 Canada: 71%
🇦🇺 Australia: 68%
🇩🇪 Germany: 64%
🇺🇸 USA: 63%
🇪🇸 Spain: 59%
🇯🇵 Japan: 55%
🇧🇷 Brazil: 54%
🇮🇳 India: 52%
Source: Gallup World Poll

Note: No cofee or book related statistics.
"""
        f"about {chosen_topic}. Avoid clichés and do not repeat past ideas."
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 1.4,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
        tweet_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        return tweet_text
    except Exception as e:
        print("❌ Gemini API failed:", e)
        return None

# === Main loop: Generate, check, and tweet ===
def post_tweet():
    tweet_text = generate_tweet()
    if not tweet_text:
        print("⚠️ No tweet text generated. Skipping...")
        return

    # === Preserve clean formatting with intentional spacing ===
    lines = [line.strip() for line in tweet_text.splitlines() if line.strip()]

    # If the tweet has at least 3 sections (title, list, source)
    if len(lines) > 3:
        # Add a blank line after the first line (the title)
        lines.insert(1, '')
        # Add a blank line before the last line (the "Source" line)
        lines.insert(-1, '')

    tweet_text = '\n'.join(lines)

    # Ensure uniqueness
    if is_duplicate(tweet_text):
        print("⚠️ Duplicate detected. Regenerating...")
        tweet_text = generate_tweet()
        if not tweet_text or is_duplicate(tweet_text):
            print("❌ Still duplicate or failed. Skipping this round.")
            return

    # Post to Twitter
    try:
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data["id"]
        print("✅ Tweet posted successfully!")
        print(f"🔗 https://x.com/your_username/status/{tweet_id}")
        save_tweet(tweet_text)
    except Exception as e:
        print("❌ Failed to post tweet:", e)
        
# === Run once ===        
post_tweet()

# === Optional: Run periodically (e.g. every 3 hours) ===
# while True:
#     post_tweet()
#     time.sleep(10800)  # 3 hours = 10800 seconds

