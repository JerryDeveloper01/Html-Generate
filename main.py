import os
import requests
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import Message, InlineKeyboardMarkup, InlineKeyboardButton

# Initialize MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["sujalbot"]
user_collection = db["sujalbot"] 

# Replace with your API ID, API Hash, and Bot Token
OWNER = "" 
API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
TOKEN = os.environ["BOT_TOKEN"]

# Telegram channel where files will be forwarded
CHANNEL_USERNAME = ""  # Replace with your channel username

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to extract names and URLs from the text file
def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if ":" in line:
            name, url = line.split(":", 1)
            data.append((name.strip(), url.strip()))
    return data

# Function to categorize URLs
def categorize_urls(urls):
    videos = []
    pdfs = []
    others = []

    for name, url in urls:
        new_url = url
        if "media-cdn.classplusapp.com/" in url or "cpvod.testbook" in url:
            new_url = f"https://api.extractor.workers.dev/player?url={url}"
            videos.append((name, new_url))
            
        elif "media-cdn.classplusapp.com/alisg-cdn-a.classplusapp.com/" in url or "media-cdn.classplusapp.com/1681/" in url or "media-cdn.classplusapp.com/tencent/" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://dragoapi.vercel.app/video/{url}"
            videos.append((name, new_url))

        elif "akamaized.net/" in url or "1942403233.rsc.cdn77.org/" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://www.khanglobalstudies.com/player?src={url}"
            videos.append((name, new_url))


        elif "/master.mpd" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://player.rarestudy.site/?id={vid_id}"
            videos.append((name, new_url))

        elif ".zip" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://video.pablocoder.eu.org/appx-zip?url={url}"
            videos.append((name, new_url))

        elif "d1d34p8vz63oiq.cloudfront.net/" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://anonymouspwplayer-b99f57957198.herokuapp.com/pw?url={video_url}?token={your_working_token}"
            videos.append((name, new_url))

        elif "youtube.com/embed" in url:
            yt_id = url.split("/")[-1]
            new_url = f"https://www.youtube.com/watch?v={yt_id}"
            
        elif ".m3u8" in url:
            videos.append((name, url))
        elif ".mp4" in url:
            videos.append((name, url))
        elif "pdf" in url:
            pdfs.append((name, url))
        else:
            others.append((name, url))

    return videos, pdfs, others

# Function to generate HTML file with Video.js player
html_content = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>{html.escape(file_name)}</title>
  <meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'/>
  <style>
    body {{ background: #0a0a0a; color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 20px; overflow-x: hidden; }}
    .player-box {{ max-width: 900px; margin: auto; text-align: center; }}
    video {{ width: 100%; border-radius: 12px; box-shadow: 0 0 15px #00ffe0; }}
    #videoTitle {{ font-size: 20px; font-weight: bold; color: #00ffe0; margin: 10px 0 30px; }}
    .tabs {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }}
    .tab-button {{ padding: 12px 20px; font-size: 16px; background: rgba(255,255,255,0.05); color: #fff; border: 1px solid #444; border-radius: 8px; cursor: pointer; font-weight: bold; transition: all 0.3s; }}
    .tab-button:hover {{ background: #00ffe0; color: #000; }}
    .tab-button.active {{ background: linear-gradient(135deg, #00ffe0, #00ffa2); color: #000; box-shadow: 0 0 12px #00ffe0; }}
    .video {{ background: #1c1c1c; padding: 14px 18px; border-radius: 10px; font-size: 15px; font-weight: 500; transition: 0.3s ease; border-left: 4px solid #00ffe0; margin-bottom: 12px; }}
    .video:hover {{ transform: translateX(6px); background: #2a2a2a; box-shadow: 0 0 10px #00ffe0; }}
    a {{ color: inherit; text-decoration: none; }}
    .footer {{ text-align: center; margin-top: 30px; font-size: 13px; color: #888; }}
    .footer a {{ color: #00ffe0; }}
  </style>
</head><body>
  <div class="player-box"><video id="player" controls autoplay playsinline>
    <source src="" type="application/x-mpegURL">Your browser does not support the video tag.
  </video><div id="videoTitle"></div></div>
  <div class="tabs">
    <button class="tab-button" onclick="showTab('video')">📺 video</button>
    <button class="tab-button" onclick="showTab('pdf')">📄 pdf</button>
    <button class="tab-button" onclick="showTab('other')">🧩 other</button>
  </div>
  {html_blocks}
  <div class="footer">ᗪEᐯEᒪOᑭEᗪ ᗷY <a href="https://t.me/Lallantoop">𓍯𝙎𝙪𝙟𝙖𝙡⚝</a></div>
  <script>
    function playVideo(url, title) {{
      const player = document.getElementById('player');
      const videoTitle = document.getElementById('videoTitle');
      player.src = url; videoTitle.textContent = title;
      window.scrollTo({{ top: 0, behavior: 'smooth' }}); player.play();
    }}
    function showTab(tabId) {{
      const tabs = document.querySelectorAll('.tab-content');
      tabs.forEach(tab => tab.style.display = 'none');
      document.getElementById(tabId).style.display = 'block';
      const buttons = document.querySelectorAll('.tab-button');
      buttons.forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
    }}
    document.addEventListener("DOMContentLoaded", () => {{ showTab('video'); }});
  </script>
</body></html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return len(sections['video']['items']), len(sections['pdf']['items']), len(sections['other']['items'])

def start_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("ＣＨＡＮＮＥＬ", url="https://t.me/studywithsv"),
        InlineKeyboardButton("ＯＷＮＥＲ", url="https://t.me/Lallantoop")
    )
    return keyboard

# ✅ MongoDB me user ID save karo (agar pehle se nahi hai)
    if not user_collection.find_one({"_id": user_id}):
        user_collection.insert_one({"_id": user_id})

# Function to download video using FFmpeg
def download_video(url, output_path):
    command = f"ffmpeg -i {url} -c copy {output_path}"
    subprocess.run(command, shell=True, check=True)

# Command handler for /start
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞! 𝐏𝐥𝐞𝐚𝐬𝐞 𝐮𝐩𝐥𝐨𝐚𝐝 𝐚 .𝐭𝐱𝐭 𝐟𝐢𝐥𝐞 𝐜𝐨𝐧𝐭𝐚𝐢𝐧𝐢𝐧𝐠 𝐔𝐑𝐋𝐬.")

# Message handler for file uploads
@app.on_message(filters.document)
async def handle_file(client: Client, message: Message):
    # Check if the file is a .txt file
    if not message.document.file_name.endswith(".txt"):
        await message.reply_text("Please upload a .txt file.")
        return

    # Download the file
    file_path = await message.download()
    file_name = message.document.file_name

    # Read the file content
    with open(file_path, "r") as f:
        file_content = f.read()

    # Extract names and URLs
    urls = extract_names_and_urls(file_content)

    # Categorize URLs
    videos, pdfs, others = categorize_urls(urls)

    # Generate HTML
    html_content = generate_html(file_name, videos, pdfs, others)
    html_file_path = file_path.replace(".txt", ".html")
    with open(html_file_path, "w") as f:
        f.write(html_content)

    # Send the HTML file to the user
    await message.reply_document(document=html_file_path, caption="✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞!\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 : Jerry™")

    # Forward the .txt file to the channel
    await client.send_document(chat_id=CHANNEL_USERNAME, document=file_path)

    # Clean up files
    os.remove(file_path)
    os.remove(html_file_path)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
