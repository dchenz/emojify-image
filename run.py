from src.args import validate
from src.emote_convert import EmoteConvert

if __name__ == "__main__":

    args = validate()
    emote = EmoteConvert(args.emote_path, "./palette.png")

    if args.fromGIF:
        emote.gif_to_gif(args.image_path, {
            "EMOTES_PER_LINE": 32 if args.line is None else args.line,
            "GIF_WIDTH": 1024 if args.width is None else args.width,
            "GIF_FRAME_DELAY": 45
        })
    else:
        emote.png_to_gif(args.image_path, {
            "EMOTES_PER_LINE": 64 if args.line is None else args.line,
            "GIF_WIDTH": 2048 if args.width is None else args.width,
            "GIF_FRAME_DELAY": 45
        })

