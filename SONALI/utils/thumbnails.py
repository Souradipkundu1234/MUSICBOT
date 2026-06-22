𝛅𝛊‌֯֟፝𝛈 x‌:
import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from SONALI import app


def truncate(text):
    words = text.split()
    line1 = ""
    line2 = ""

    for word in words:
        if len(line1 + " " + word) <= 30:
            line1 += " " + word
        elif len(line2 + " " + word) <= 30:
            line2 += " " + word
        else:
            break

    return [line1.strip(), line2.strip()]


async def get_thumb(videoid):
    output_path = f"cache/{videoid}_v4.png"

    if os.path.isfile(output_path):
        return output_path

    # =========================
    # Fetch YouTube Video Data
    # =========================
    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)

    title = "Unsupported Title"
    duration = "Unknown"
    views = "Unknown Views"
    thumbnail = None

    for result in (await results.next())["result"]:
        title = re.sub(r"\W+", " ", result.get("title", "Unsupported Title")).title()
        duration = result.get("duration", "Unknown")
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]

    if not thumbnail:
        raise Exception("Thumbnail not found")

    # =========================
    # Download Thumbnail
    # =========================
    thumb_path = f"cache/thumb_{videoid}.jpg"

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                async with aiofiles.open(thumb_path, "wb") as f:
                    await f.write(await resp.read())

    youtube = Image.open(thumb_path).convert("RGB")

    # =========================
    # Background
    # =========================
    bg = youtube.resize((1280, 720))
    bg = bg.filter(ImageFilter.GaussianBlur(25))
    bg = ImageEnhance.Brightness(bg).enhance(0.35)
    bg = bg.convert("RGBA")

    # Dark overlay
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 120))
    bg = Image.alpha_composite(bg, overlay)

    draw = ImageDraw.Draw(bg)

    # =========================
    # Fonts
    # =========================
    font_title = ImageFont.truetype("SONALI/assets/font3.ttf", 52)
    font_text = ImageFont.truetype("SONALI/assets/font2.ttf", 36)
    font_small = ImageFont.truetype("SONALI/assets/font2.ttf", 28)
    font_now = ImageFont.truetype("SONALI/assets/font.ttf", 32)

    # =========================
    # Left Thumbnail with Rounded Border
    # =========================
    thumb = youtube.resize((420, 420)).convert("RGBA")

    # Golden border canvas
    thumb_canvas = Image.new("RGBA", (460, 460), (0, 0, 0, 0))
    canvas_draw = ImageDraw.Draw(thumb_canvas)

    # Outer golden rounded rectangle
    canvas_draw.rounded_rectangle(
        (0, 0, 460, 460),
        radius=40,
        fill=(255, 215, 0, 255)
    )

    # Rounded mask for image
    mask = Image.new("L", (420, 420), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, 420, 420), radius=30, fill=255)

    thumb_canvas.paste(thumb, (20, 20), mask)

    # Paste to background
    bg.paste(thumb_canvas, (80, 130), thumb_canvas)

    # =========================
    # NOW PLAYING Badge
    # =========================
    draw.rounded_rectangle(
        (650, 90, 930, 155),
        radius=30,
        fill=(255, 215, 0)
    )
    draw.text((705, 105), "NOW PLAYING", font=font_now, fill="black")

    # =========================
    # Title
    # =========================
    lines = truncate(title)
    draw.text((650, 190), lines[0], font=font_title, fill="white")
    if lines[1]:
        draw.text((650, 250), lines[1], font=font_title, fill="white")

    # Underline
    draw.line((650, 330, 1180, 330), fill=(255, 215, 0), width=4)# =========================
    # Video Info
    # =========================
    draw.text((650, 370), f"Duration :  {duration}", font=font_text, fill="white")
    draw.text((650, 430), f"Views :  {views}", font=font_text, fill="white")

    bot_username = getattr(app, "username", None)
    if bot_username:
        player_text = f"Player :  @{bot_username}"
    else:
        player_text = "Powered By :  @AntaraUpdates"

    draw.text(
        (650, 490),
        player_text,
        font=font_text,
        fill=(255, 215, 0)
    )

    # =========================
    # Progress Bar
    # =========================
    bar_x1 = 650
    bar_x2 = 1180
    bar_y = 585
    progress = 0.60  # 60%

    # Background line
    draw.rectangle(
        (bar_x1, bar_y, bar_x2, bar_y + 8),
        fill=(200, 200, 200)
    )

    # Progress line
    progress_x = bar_x1 + int((bar_x2 - bar_x1) * progress)
    draw.rectangle(
        (bar_x1, bar_y, progress_x, bar_y + 8),
        fill=(255, 215, 0)
    )

    # Knob
    draw.ellipse(
        (progress_x - 8, bar_y - 8, progress_x + 8, bar_y + 16),
        fill=(255, 215, 0)
    )

    # Time labels
    draw.text((650, 605), "00:00", font=font_small, fill="white")

    duration_bbox = draw.textbbox((0, 0), duration, font=font_small)
    duration_width = duration_bbox[2] - duration_bbox[0]
    draw.text(
        (1180 - duration_width, 605),
        duration,
        font=font_small,
        fill="white"
    )

    # =========================
    # Developer Credit
    # =========================
    dev_text = "Dev :- @TrigXArea"  # এখানে নিজের username দিন

    dev_bbox = draw.textbbox((0, 0), dev_text, font=font_small)
    dev_width = dev_bbox[2] - dev_bbox[0]

    draw.text(
        (1280 - dev_width - 40, 670),
        dev_text,
        font=font_small,
        fill=(255, 215, 0)
    )

    # =========================
    # Save Output
    # =========================
    bg.convert("RGB").save(output_path)

    # Cleanup
    try:
        os.remove(thumb_path)
    except:
        pass

    return output_path
