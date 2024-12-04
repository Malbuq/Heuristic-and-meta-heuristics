from PIL import Image, ImageDraw, ImageFont

def printKeyboard(keyboard_layout, language, fitness, initial_fitness):
    key_width, key_height = 60, 60 
    padding = 10
    rows = [keyboard_layout[:11], keyboard_layout[11:22], keyboard_layout[22:]] 
    row_offset = [0, 0.25, 0.75]
    
    img_width = (key_width + padding) * 15 + padding
    img_height = (key_height + padding) * 6 + padding
    
    img = Image.new("RGB", (img_width, img_height), color="black")
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("arial.ttf", 20)

    row2_colors = [
        "#f5a742",  # Light Orange
        "#f5dd42",  # Yellow
        "#42f584",  # Green
        "#42f5e9",  # Blue
        "#3F51B5",  # Medium Blue
        "#9C27B0",  # Medium Purple
        "#E91E63",  # Medium Pink
        "#F44336",  # Medium Red
    ]

    first_colors = [0,1,2,3]
    second_colors = [6,7,8,9]

    for row_index, row in enumerate(rows):
        for col_index, char in enumerate(row):
            x = col_index * (key_width + padding) + padding + row_offset[row_index]*key_width + 130
            y = row_index * (key_height + padding) + padding + 90

            key_color = "white"

            if row_index == 1:
                if col_index in first_colors:
                    key_color = row2_colors[col_index]
                elif col_index in second_colors:
                    key_color = row2_colors[col_index - 2]
            
            draw.rounded_rectangle(
                [x, y, x + key_width, y + key_height], 
                radius=10, 
                outline=key_color,
                width=4,
            )

            text_width = 12
            text_height = 17
            text_x = x + (key_width - text_width) // 2
            text_y = y + (key_height - text_height) // 2
            draw.text((text_x, text_y), char.upper(), fill="white", font=font, stroke_width=1)

    improvement = (initial_fitness - fitness) / initial_fitness * 100
    info_text = f"Melhoria em fitness: {improvement:.0f}% | Língua: {language}"
    text_width, text_height = 1000, 50
    text_x = img_width - text_width - 10 
    text_y = img_height - text_height - 10
    draw.text((text_x, text_y), info_text, fill="white", font=font)
    
    img.show()

