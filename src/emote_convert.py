from PIL import Image

from .emote_colours import generate_emote_palette, to_rgb_colour
from .image_utils import resize_colourise_image, save_gif
from .progress_logger import on_load_log, on_progress_log

# The script runs using one of three modes
# Output 1: Discord emote texti
# Output 2: Large GIF containing PNG
# Output 3: Large GIF containing another GIF

class EmoteConvert:
    def __init__(self, emote_path, palette_path):
        self._emote_im = Image.open(emote_path)
        self._palette_im = Image.open(palette_path).convert("P")
        self._palette_map = generate_emote_palette(self._palette_im)

    def png_to_gif(self, png_path, options):
        im = Image.open(png_path)
        on_load_log(self._emote_im, im, mode=0)
        resized_im = resize_colourise_image(im, self._palette_im, options["EMOTES_PER_LINE"])
        assert options["EMOTES_PER_LINE"] is None or options["EMOTES_PER_LINE"] == resized_im.width
        bg_frame_images = []
        for frame in range(self._emote_im.n_frames):
            on_progress_log(self._emote_im, im, frame, mode=0)
            bg_im = self._create_gif_frame(resized_im, frame, options)
            bg_frame_images.append(bg_im)
        save_gif(bg_frame_images, self._emote_im, im, options, mode=0)

    def gif_to_gif(self, gif_path, options):
        gif_im = Image.open(gif_path)
        on_load_log(self._emote_im, gif_im, mode=1)
        bg_frame_images = []
        for frame in range(gif_im.n_frames):
            gif_im.seek(frame)
            gif_frame_im = resize_colourise_image(gif_im, self._palette_im, options["EMOTES_PER_LINE"])
            assert options["EMOTES_PER_LINE"] is None or options["EMOTES_PER_LINE"] == gif_frame_im.width
            on_progress_log(self._emote_im, gif_im, frame, mode=1)
            bg_im = self._create_gif_frame(gif_frame_im, frame, options)
            bg_frame_images.append(bg_im)
        save_gif(bg_frame_images, self._emote_im, gif_im, options, mode=1)

    # Create frames for animated GIF generation
    def _create_gif_frame(self, im, frame, options, cache={}):
        emote_width = options["GIF_WIDTH"] // im.width
        gif_size = (options["GIF_WIDTH"], int(options["GIF_WIDTH"] / im.width * im.height))
        background_im = Image.new("RGB", gif_size, (0, 0, 0))
        for y in range(im.height):
            for x in range(im.width):
                colour_256 = im.getpixel((x, y))
                colour_rgb = self._palette_map[colour_256]
                frame_number = frame % self._emote_im.n_frames
                key = (frame_number, colour_rgb)
                if key not in cache:
                    self._emote_im.seek(frame_number)
                    frame_im = to_rgb_colour(self._emote_im.convert("RGBA"), colour_rgb)
                    cache[key] = frame_im.resize((emote_width, emote_width))
                background_im.paste(cache[key], (emote_width * x, emote_width * y))
        return background_im

