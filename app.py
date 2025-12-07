from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-meme', methods=['POST'])
def generate_meme():
    upper_text = request.form.get('upper_text', '')
    bottom_text = request.form.get('bottom_text', '')
    image_file = request.files.get('image')

    if image_file:
        # Ensure directories exist
        os.makedirs("static/uploads", exist_ok=True)
        os.makedirs("static/memes", exist_ok=True)

        # Save uploaded image
        image_path = f"static/uploads/{image_file.filename}"
        image_file.save(image_path)
        image = Image.open(image_path)

        # Convert RGBA → RGB (JPEG cannot handle alpha channel)
        if image.mode in ("RGBA", "LA"):
            image = image.convert("RGB")

        draw = ImageDraw.Draw(image)

        # Function to wrap text
        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] <= max_width - 20:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return lines

        # Function to draw text with outline
        def draw_text(text, start_y, font):
            lines = wrap_text(text, font, image.width)
            y = start_y
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (image.width - text_width) / 2

                # Draw outline
                outline_range = max(3, font.size // 12)
                for dx in range(-outline_range, outline_range + 1):
                    for dy in range(-outline_range, outline_range + 1):
                        draw.text((x + dx, y + dy), line, font=font, fill="black")

                # Draw main text
                draw.text((x, y), line, font=font, fill="white")
                y += text_height + 5

        # Determine font size based on image width
        font_size = max(40, image.width // 8)  # larger for memes
        try:
            font = ImageFont.truetype("arial.ttf", size=font_size)
        except:
            font = ImageFont.load_default()

        # Draw upper text
        draw_text(upper_text.upper(), start_y=10, font=font)

        # Draw bottom text
        bottom_lines = wrap_text(bottom_text.upper(), font, image.width)
        total_bottom_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 5 for line in bottom_lines)
        draw_text(bottom_text.upper(), start_y=image.height - total_bottom_height - 10, font=font)

        # Save meme
        output_path = "static/memes/meme_result.jpg"
        image.save(output_path)

        return render_template("index.html", meme_url=output_path)

    return "No image uploaded."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
