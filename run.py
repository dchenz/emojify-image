from src.args import validate
from src.emote_convert import EmoteConvert
from configparser import ConfigParser

if __name__ == "__main__":

    args = validate()
    emote = EmoteConvert(args.emote_path, "./palette.png")
    config = ConfigParser()
    config.read("./config.ini")

    try:
        emotes_per_line = int(config.get("graphics", "EmotesPerLine"))
        final_width = int(config.get("graphics", "FinalOutputWidth"))
        gif_frame_delay = int(config.get("graphics", "FrameDelay"))
    except:
        print("Invalid configuration values")
        exit(1)

    options = {
        "EMOTES_PER_LINE": emotes_per_line,
        "GIF_WIDTH": final_width,
        "GIF_FRAME_DELAY": gif_frame_delay,
    }

    if args.gif_source:
        emote.gif_to_gif(args.image_path, options)
    else:
        emote.png_to_gif(args.image_path, options)
