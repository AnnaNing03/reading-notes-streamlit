import io
import textwrap
from typing import Any

import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont


def generate_poster_content(
    book_name: str, notes: list[dict[str, Any]]
) -> dict[str, str] | None:
    """Call DeepSeek API to generate poster content from notes."""
    api_key = st.secrets.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        st.error("请配置 DEEPSEEK_API_KEY")
        return None

    notes_text = "\n\n".join(
        f"笔记{i + 1}（{n.get('date', '')}）:\n摘抄：{n.get('sentence', '')}\n想法：{n.get('thought', '')}"
        for i, n in enumerate(notes)
    )

    prompt = f"""你是一位文学评论家和读书博主。以下是用户阅读《{book_name}》时记录的所有笔记：

{notes_text}

请基于以上笔记，生成以下内容（用 JSON 格式返回）：
1. "title": 一个吸引人的标题（不超过10个字）
2. "quote": 最精彩的一句金句（从摘抄中选出，原文引用）
3. "summary": 整体感悟（用一段话总结，基于所有想法，100字以内）
4. "insight": 个人思考精华（一句话概括用户的核心启发，30字以内）

请只返回 JSON 对象，不要包含其他文字。"""

    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一位专业的文学评论家，擅长提炼读书感悟。请只返回有效的 JSON 对象。",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        content = response.choices[0].message.content
        if content is None:
            st.error("DeepSeek 未返回内容")
            return None

        import json

        cleaned = content.replace("```json", "").replace("```", "").strip()
        result: dict[str, str] = json.loads(cleaned)
        return result
    except Exception as e:
        st.error(f"AI 生成失败: {e}")
        return None


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    """Wrap text to fit within max_width pixels."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        # Try character-by-character wrapping for CJK text
        current_line = ""
        for char in paragraph:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
    return lines


def create_poster_image(
    content: dict[str, str], book_name: str, note_date: str
) -> bytes:
    """Generate a poster image using Pillow."""
    width = 750
    height = 1200
    padding = 60
    content_width = width - padding * 2

    # Create image with warm gradient background
    img = Image.new("RGB", (width, height), "#faf7f2")
    draw = ImageDraw.Draw(img)

    # Draw subtle gradient overlay
    for y in range(height):
        r = int(250 - (y / height) * 15)
        g = int(247 - (y / height) * 20)
        b = int(242 - (y / height) * 30)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Try to load fonts - use default if not available
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 42)
        quote_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 24)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
        label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except (OSError, IOError):
        title_font = ImageFont.load_default()
        quote_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    y_pos = padding + 20

    # Decorative top line
    draw.line([(padding, y_pos), (width - padding, y_pos)], fill="#d4c5a9", width=2)
    y_pos += 30

    # Title
    title = content.get("title", "读书感悟")
    title_lines = _wrap_text(title, title_font, content_width, draw)
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_pos), line, fill="#2c2c2c", font=title_font)
        y_pos += bbox[3] - bbox[1] + 8
    y_pos += 10

    # Book name and date
    subtitle = f"《{book_name}》· {note_date}"
    # Use textwrap for ASCII-friendly wrapping as fallback
    bbox = draw.textbbox((0, 0), subtitle, font=label_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y_pos), subtitle, fill="#8a8a8a", font=label_font)
    y_pos += 50

    # Quote section with background
    quote = content.get("quote", "")
    quote_text = f'"{quote}"'
    quote_lines = _wrap_text(quote_text, quote_font, content_width - 40, draw)
    quote_height = len(quote_lines) * 35 + 40

    # Quote background
    draw.rounded_rectangle(
        [(padding - 10, y_pos - 10), (width - padding + 10, y_pos + quote_height)],
        radius=15,
        fill="#f5f0e8",
    )

    y_pos += 15
    for line in quote_lines:
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, y_pos), line, fill="#4a4a4a", font=quote_font)
        y_pos += 35
    y_pos += 40

    # Summary section
    draw.text((padding, y_pos), "整体感悟", fill="#8a8a8a", font=label_font)
    y_pos += 30
    summary = content.get("summary", "")
    summary_lines = _wrap_text(summary, body_font, content_width, draw)
    for line in summary_lines:
        draw.text((padding, y_pos), line, fill="#2c2c2c", font=body_font)
        y_pos += 32
    y_pos += 30

    # Insight section
    draw.text((padding, y_pos), "思考精华", fill="#8a8a8a", font=label_font)
    y_pos += 30
    insight = content.get("insight", "")
    insight_lines = _wrap_text(insight, body_font, content_width, draw)
    for line in insight_lines:
        draw.text((padding, y_pos), line, fill="#2c2c2c", font=body_font)
        y_pos += 32
    y_pos += 40

    # Bottom decorative line
    bottom_y = max(y_pos, height - 80)
    draw.line([(padding, bottom_y), (width - padding, bottom_y)], fill="#d4c5a9", width=1)
    bottom_y += 20

    # Footer
    footer = "读书笔记 · 用阅读丈量世界"
    bbox = draw.textbbox((0, 0), footer, font=small_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, bottom_y), footer, fill="#b0a99f", font=small_font)

    # Crop to actual content height if needed
    actual_height = max(bottom_y + 50, height)
    if actual_height != height:
        new_img = Image.new("RGB", (width, actual_height), "#faf7f2")
        new_draw = ImageDraw.Draw(new_img)
        for y in range(actual_height):
            r = int(250 - (y / actual_height) * 15)
            g = int(247 - (y / actual_height) * 20)
            b = int(242 - (y / actual_height) * 30)
            new_draw.line([(0, y), (width, y)], fill=(r, g, b))
        new_img.paste(img, (0, 0))
        img = new_img

    # Save to bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG", quality=95)
    buffer.seek(0)
    return buffer.getvalue()
