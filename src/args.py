import argparse, os


def validate():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to the input image.")
    parser.add_argument("emote_path", help="Path to the emote image (GIF).")
    parser.add_argument(
        "--gif-source", action="store_true", help="IMAGE_PATH is a GIF image."
    )
    args = parser.parse_args()
    if args.gif_source and not args.image_path.endswith(".gif"):
        parser.error("--gif-source can only be used with GIF as input.")
    return args
