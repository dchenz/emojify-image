from PIL import Image

# Processing and resizing PNG image
# Mapping RGB pixel colour to 8-bit palette
def resize_colourise_image(im, palette_im, emotes_per_line):
    im = im.convert("RGB")
    if emotes_per_line is None:
        emotes_per_line = im.width
    new_image_size = (
        emotes_per_line,
        int(emotes_per_line / im.width * im.height)
    )
    resized_im = im.resize(new_image_size)
    return resized_im.quantize(palette=palette_im)

# Save GIF to disk
def save_gif(frame_images, emote_im, input_im, options, mode=0):
    input_name = input_im.filename.rsplit("/", 1)[-1].split(".", 1)[0]
    emote_name = emote_im.filename.rsplit("/", 1)[-1].split(".", 1)[0]
    filename = f'{input_name}-{emote_name}' + ("-gif" if mode == 1 else "")
    filename += f'_{options["EMOTES_PER_LINE"]}-{options["GIF_WIDTH"]}.gif'
    frame_images[0].save(filename, save_all=True, format="GIF", duration=options["GIF_FRAME_DELAY"],
        loop=0, transparency=0, disposal=2, append_images=frame_images[1:])
    print("\nSaved:", filename)