from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont

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
        image_path = f"static/uploads/{image_file.filename}"
        image_file.save(image_path)
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

        # Make text bigger: increase divisor to smaller number
        font_size = max(40, image.width // 6)  # bigger font
        try:
            font_path = "arial.ttf"
            font = ImageFont.truetype(font_path, size=font_size)
        except:
            font = ImageFont.load_default()

        margin = 10

        def wrap_text(text, font, max_width):
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                line_width = bbox[2] - bbox[0]
                if line_width <= max_width - 2*margin:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)
            return lines

        def draw_text(text, start_y):
            lines = wrap_text(text, font, image.width)
            y = start_y
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (image.width - text_width) / 2

                # Draw thicker outline for bigger text
                outline_range = max(3, font_size // 20)
                for dx in range(-outline_range, outline_range+1):
                    for dy in range(-outline_range, outline_range+1):
                        draw.text((x + dx, y + dy), line, font=font, fill="black")

                draw.text((x, y), line, font=font, fill="white")
                y += text_height + 10  # more spacing for bigger text

        draw_text(upper_text, start_y=10)
        bottom_lines = wrap_text(bottom_text, font, image.width)
        total_bottom_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 10 for line in bottom_lines)
        draw_text(bottom_text, start_y=image.height - total_bottom_height - 10)

        output_path = "static/memes/meme_result.jpg"
        image.save(output_path)

        return render_template("index.html", meme_url=output_path)

    return "No image uploaded."




if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000, debug=True)

