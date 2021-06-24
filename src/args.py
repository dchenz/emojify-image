import argparse, os

def validate():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", type=_file_exists, help="Path to the input image.")
    parser.add_argument("emote_path", type=_gif_exists, help="Path to the emote image (GIF).")
    parser.add_argument("-l", "--line", type=_positive_int, help="Maximum emotes on each row.")
    parser.add_argument("-w", "--width", type=_positive_int, help="Width of the output GIF (pixels).")
    parser.add_argument("-g", "--fromGIF", action="store_true", help="IMAGE_PATH is a GIF image.")
    args = parser.parse_args()
    if args.fromGIF and not args.image_path.lower().endswith(".gif"):
      parser.error("--fromGIF can only be used with GIF as input.")
    return args

def _positive_int(n):
  try:
    n = int(n)
    if n <= 0:
      raise Exception
  except:
    raise argparse.ArgumentTypeError("Integer must be non-zero.")
  return n

def _gif_exists(file):
  return file.endswith(".gif") and _file_exists(file)

def _file_exists(file):
  if not os.path.exists(file):
    raise argparse.ArgumentTypeError(f'{file} could not be found.')
  return file