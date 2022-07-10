import colorsys
import os
from argparse import ArgumentParser, Namespace

from PIL import Image

_Image = Image.Image

# An image with mode == "RGB" has 3-tuple RGB colors
# An image with mode == "P" has scalar colors in the range(0, 256)
ColorRGB = tuple[int, int, int]
Color256 = int

# My attempt at speeding up the script
image_cache = {}

# Order of this list matters so be careful when changing it
# For every tuple t, t[0] is an RGB color and t[1] is an x/y coordinate
#
# The code must map "P" pixels to "RGB"
#   hence the list's index will be the "P" value
# The code must reconstruct a 16x16 image for Image.quantize()
#   hence pixel x/y coordinates are included too
palette_pixels: list[tuple[ColorRGB, tuple[int, int]]] = [
    ((144, 38, 17), (0, 2)),
    ((148, 153, 254), (11, 7)),
    ((241, 200, 82), (10, 1)),
    ((253, 186, 84), (11, 2)),
    ((244, 218, 102), (12, 1)),
    ((104, 106, 238), (6, 7)),
    ((255, 202, 107), (14, 2)),
    ((116, 198, 255), (10, 9)),
    ((80, 83, 207), (4, 7)),
    ((177, 182, 255), (15, 7)),
    ((132, 136, 252), (9, 7)),
    ((147, 211, 255), (13, 9)),
    ((165, 170, 255), (13, 7)),
    ((112, 229, 243), (11, 10)),
    ((115, 120, 241), (8, 7)),
    ((166, 85, 214), (6, 6)),
    ((182, 55, 26), (2, 2)),
    ((172, 94, 25), (3, 1)),
    ((49, 135, 3), (3, 12)),
    ((68, 88, 1), (1, 13)),
    ((147, 235, 247), (14, 10)),
    ((184, 102, 229), (8, 6)),
    ((240, 170, 80), (10, 15)),
    ((176, 26, 18), (1, 4)),
    ((77, 167, 239), (7, 9)),
    ((23, 135, 47), (3, 11)),
    ((16, 91, 9), (0, 11)),
    ((121, 229, 140), (11, 11)),
    ((219, 216, 197), (12, 0)),
    ((211, 134, 250), (12, 6)),
    ((218, 153, 252), (14, 6)),
    ((248, 166, 53), (7, 1)),
    ((245, 139, 39), (6, 1)),
    ((208, 202, 183), (10, 0)),
    ((246, 106, 79), (7, 3)),
    ((254, 152, 45), (8, 2)),
    ((255, 165, 172), (13, 4)),
    ((199, 117, 241), (10, 6)),
    ((250, 231, 104), (13, 1)),
    ((232, 231, 211), (14, 0)),
    ((94, 40, 7), (0, 1)),
    ((241, 119, 204), (10, 5)),
    ((198, 70, 152), (5, 5)),
    ((251, 122, 78), (8, 3)),
    ((210, 181, 57), (8, 14)),
    ((243, 88, 73), (6, 4)),
    ((217, 147, 61), (8, 15)),
    ((192, 125, 45), (6, 15)),
    ((204, 65, 36), (4, 3)),
    ((213, 87, 169), (7, 5)),
    ((211, 239, 108), (15, 13)),
    ((230, 65, 53), (5, 4)),
    ((252, 241, 126), (15, 1)),
    ((246, 193, 57), (9, 1)),
    ((248, 209, 89), (11, 1)),
    ((168, 31, 121), (3, 5)),
    ((210, 90, 29), (4, 2)),
    ((220, 83, 42), (5, 3)),
    ((255, 181, 154), (14, 3)),
    ((255, 213, 131), (15, 2)),
    ((247, 232, 134), (15, 14)),
    ((252, 115, 111), (9, 4)),
    ((249, 126, 34), (6, 2)),
    ((255, 141, 101), (10, 3)),
    ((255, 170, 138), (13, 3)),
    ((255, 192, 170), (15, 3)),
    ((222, 97, 179), (8, 5)),
    ((202, 229, 91), (14, 13)),
    ((196, 189, 167), (9, 0)),
    ((194, 220, 87), (13, 13)),
    ((204, 136, 53), (7, 15)),
    ((166, 250, 119), (15, 12)),
    ((255, 181, 190), (15, 4)),
    ((186, 213, 81), (12, 13)),
    ((184, 175, 155), (8, 0)),
    ((166, 137, 15), (5, 14)),
    ((230, 108, 30), (5, 2)),
    ((255, 161, 126), (12, 3)),
    ((251, 145, 221), (13, 5)),
    ((251, 157, 225), (14, 5)),
    ((255, 138, 145), (11, 4)),
    ((249, 134, 216), (12, 5)),
    ((252, 164, 228), (15, 5)),
    ((253, 126, 132), (10, 4)),
    ((255, 149, 157), (12, 4)),
    ((228, 157, 69), (9, 15)),
    ((235, 99, 56), (6, 3)),
    ((244, 178, 50), (8, 1)),
    ((154, 72, 202), (5, 6)),
    ((115, 33, 164), (2, 6)),
    ((105, 83, 9), (2, 14)),
    ((230, 106, 189), (9, 5)),
    ((119, 56, 11), (1, 1)),
    ((109, 135, 4), (5, 13)),
    ((121, 131, 243), (8, 8)),
    ((120, 146, 13), (6, 13)),
    ((148, 236, 101), (13, 12)),
    ((99, 124, 1), (4, 13)),
    ((118, 207, 71), (10, 12)),
    ((122, 110, 96), (4, 0)),
    ((144, 75, 14), (2, 1)),
    ((102, 192, 54), (9, 12)),
    ((151, 18, 106), (2, 5)),
    ((104, 218, 129), (10, 11)),
    ((133, 61, 17), (2, 15)),
    ((146, 63, 193), (4, 6)),
    ((132, 25, 11), (0, 4)),
    ((134, 50, 181), (3, 6)),
    ((171, 159, 141), (7, 0)),
    ((219, 48, 40), (4, 4)),
    ((194, 164, 41), (7, 14)),
    ((168, 194, 61), (10, 13)),
    ((182, 110, 36), (5, 15)),
    ((178, 204, 72), (11, 13)),
    ((177, 46, 16), (2, 3)),
    ((181, 152, 29), (6, 14)),
    ((222, 193, 68), (10, 14)),
    ((181, 47, 134), (4, 5)),
    ((191, 74, 28), (3, 2)),
    ((206, 36, 30), (3, 4)),
    ((169, 246, 180), (15, 11)),
    ((196, 109, 23), (4, 1)),
    ((129, 104, 10), (3, 14)),
    ((136, 238, 151), (13, 11)),
    ((132, 221, 85), (11, 12)),
    ((157, 183, 51), (9, 13)),
    ((155, 164, 255), (12, 8)),
    ((145, 171, 39), (8, 13)),
    ((151, 242, 164), (14, 11)),
    ((132, 158, 26), (7, 13)),
    ((136, 122, 107), (5, 0)),
    ((111, 44, 9), (1, 15)),
    ((150, 121, 10), (4, 14)),
    ((134, 7, 91), (1, 5)),
    ((157, 243, 109), (14, 12)),
    ((22, 36, 171), (0, 7)),
    ((155, 141, 125), (6, 0)),
    ((88, 10, 137), (0, 6)),
    ((88, 70, 8), (1, 14)),
    ((107, 96, 84), (3, 0)),
    ((93, 90, 232), (5, 7)),
    ((79, 63, 7), (0, 14)),
    ((64, 56, 48), (1, 0)),
    ((85, 76, 65), (2, 0)),
    ((91, 99, 214), (5, 8)),
    ((72, 69, 212), (3, 7)),
    ((68, 151, 218), (6, 9)),
    ((86, 109, 0), (3, 13)),
    ((83, 171, 35), (7, 12)),
    ((141, 229, 94), (12, 12)),
    ((157, 80, 24), (3, 15)),
    ((73, 161, 25), (6, 12)),
    ((114, 5, 78), (0, 5)),
    ((97, 18, 148), (1, 6)),
    ((79, 208, 109), (9, 11)),
    ((72, 221, 241), (10, 10)),
    ((91, 181, 44), (8, 12)),
    ((89, 183, 255), (9, 9)),
    ((68, 196, 100), (8, 11)),
    ((46, 53, 170), (1, 8)),
    ((63, 151, 15), (5, 12)),
    ((58, 75, 1), (0, 13)),
    ((33, 107, 190), (3, 9)),
    ((32, 91, 170), (2, 9)),
    ((50, 57, 202), (2, 7)),
    ((34, 103, 0), (1, 12)),
    ((41, 121, 202), (4, 9)),
    ((39, 115, 0), (2, 12)),
    ((55, 136, 209), (5, 9)),
    ((37, 154, 63), (5, 11)),
    ((40, 215, 239), (9, 10)),
    ((61, 182, 92), (7, 11)),
    ((59, 66, 183), (2, 8)),
    ((46, 167, 75), (6, 11)),
    ((15, 181, 204), (6, 10)),
    ((24, 207, 233), (8, 10)),
    ((218, 124, 28), (5, 1)),
    ((255, 152, 114), (11, 3)),
    ((17, 195, 222), (7, 10)),
    ((50, 43, 37), (0, 0)),
    ((5, 139, 166), (3, 10)),
    ((33, 40, 152), (0, 8)),
    ((11, 167, 190), (5, 10)),
    ((29, 45, 192), (1, 7)),
    ((8, 153, 181), (4, 10)),
    ((5, 123, 143), (2, 10)),
    ((6, 109, 23), (1, 11)),
    ((13, 120, 32), (2, 11)),
    ((4, 94, 108), (0, 10)),
    ((30, 75, 151), (1, 9)),
    ((4, 108, 124), (1, 10)),
    ((28, 62, 131), (0, 9)),
    ((208, 202, 183), (11, 0)),
    ((219, 216, 197), (13, 0)),
    ((232, 231, 211), (15, 0)),
    ((250, 231, 104), (14, 1)),
    ((144, 38, 17), (1, 2)),
    ((245, 139, 39), (7, 2)),
    ((254, 152, 45), (9, 2)),
    ((248, 166, 53), (10, 2)),
    ((253, 186, 84), (12, 2)),
    ((241, 200, 82), (13, 2)),
    ((144, 38, 17), (0, 3)),
    ((144, 38, 17), (1, 3)),
    ((182, 55, 26), (3, 3)),
    ((251, 122, 78), (9, 3)),
    ((176, 26, 18), (2, 4)),
    ((243, 88, 73), (7, 4)),
    ((246, 106, 79), (8, 4)),
    ((255, 165, 172), (14, 4)),
    ((198, 70, 152), (6, 5)),
    ((241, 119, 204), (11, 5)),
    ((166, 85, 214), (7, 6)),
    ((184, 102, 229), (9, 6)),
    ((199, 117, 241), (11, 6)),
    ((211, 134, 250), (13, 6)),
    ((218, 153, 252), (15, 6)),
    ((104, 106, 238), (7, 7)),
    ((132, 136, 252), (10, 7)),
    ((148, 153, 254), (12, 7)),
    ((165, 170, 255), (14, 7)),
    ((80, 83, 207), (3, 8)),
    ((80, 83, 207), (4, 8)),
    ((104, 106, 238), (6, 8)),
    ((115, 120, 241), (7, 8)),
    ((132, 136, 252), (9, 8)),
    ((148, 153, 254), (10, 8)),
    ((148, 153, 254), (11, 8)),
    ((165, 170, 255), (13, 8)),
    ((177, 182, 255), (14, 8)),
    ((177, 182, 255), (15, 8)),
    ((77, 167, 239), (8, 9)),
    ((116, 198, 255), (11, 9)),
    ((116, 198, 255), (12, 9)),
    ((147, 211, 255), (14, 9)),
    ((147, 211, 255), (15, 9)),
    ((112, 229, 243), (12, 10)),
    ((112, 229, 243), (13, 10)),
    ((147, 235, 247), (15, 10)),
    ((23, 135, 47), (4, 11)),
    ((121, 229, 140), (12, 11)),
    ((16, 91, 9), (0, 12)),
    ((49, 135, 3), (4, 12)),
    ((68, 88, 1), (2, 13)),
    ((210, 181, 57), (9, 14)),
    ((241, 200, 82), (11, 14)),
    ((241, 200, 82), (12, 14)),
    ((244, 218, 102), (13, 14)),
    ((244, 218, 102), (14, 14)),
    ((94, 40, 7), (0, 15)),
    ((172, 94, 25), (4, 15)),
    ((240, 170, 80), (11, 15)),
    ((253, 186, 84), (12, 15)),
    ((253, 186, 84), (13, 15)),
    ((255, 202, 107), (14, 15)),
    ((255, 202, 107), (15, 15)),
]


def generate_palette_image() -> _Image:
    """
    Generates a Pillow image from the global palette.
    """
    im = Image.new("RGBA", (16, 16))
    for rgb, xy in palette_pixels:
        im.putpixel(xy, rgb + (255,))
    return im.convert("P")


def get_palette_rgb(pv: Color256) -> ColorRGB:
    """
    Maps a color from range(0, 256) to an RGB color according to the global palette.
    """
    return palette_pixels[pv][0]


palette_im = generate_palette_image()


def parse_args() -> Namespace:
    """
    Parse command line arguments. Exit if invalid arguments are provided.
    """
    parser = ArgumentParser()

    parser.add_argument("image_path", help="Path to the input image")
    parser.add_argument("emoji_path", help="Path to the emoji image (GIF)")
    parser.add_argument(
        "--use-gif", action="store_true", help="Source image (not emoji) is a GIF"
    )
    parser.add_argument(
        "-l",
        "--per-line",
        type=int,
        default=64,
        help="Number of emojis on every line (default 64)",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=1024,
        help="Pixel width of the output GIF (default 1024)",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=int,
        default=45,
        help="Milliseconds between output GIF frames (default 45)",
    )

    args = parser.parse_args()

    # Not reliable but the user will know quickly if input isn't a GIF
    if args.use_gif and not args.image_path.endswith(".gif"):
        parser.error("--use-gif can only be used with GIF as input.")

    if args.per_line and args.per_line <= 0:
        parser.error("--per-line must be a positive integer")

    if args.width and args.width <= 0:
        parser.error("--width must be a positive integer")

    if args.delay and args.delay <= 0:
        parser.error("--delay must be a positive integer")

    return args


def png_to_gif(args: Namespace):
    """
    Converts a PNG image into a GIF with emojis as pixels.
    """
    # Open source PNG and emoji images
    emoji_im = Image.open(args.emoji_path)
    png_im = Image.open(args.image_path)

    # Need to change size to fit desired dimensions
    # Each pixel will be one emoji, so it's args.per_line
    resized_im = png_im
    if args.per_line:
        resized_im = resize_image(png_im, args.per_line)

    # And map all its colors into the global palette's colors
    colored_im = colorize_image(resized_im)

    bg_frame_images = []
    for frame in range(emoji_im.n_frames):

        bg_im = create_gif_frame(emoji_im, colored_im, frame, args)
        bg_frame_images.append(bg_im)

    # Convert GIF frames into an actual GIF
    fn = get_output_filename(emoji_im, png_im, args)
    save_gif(bg_frame_images, fn, args.delay)


def gif_to_gif(args: Namespace):
    """
    Converts a GIF image into a GIF with emojis as pixels.
    """
    # Open source GIF and emoji images
    emoji_im = Image.open(args.emoji_path)
    gif_im = Image.open(args.image_path)

    bg_frame_images = []
    for frame in range(gif_im.n_frames):
        # We treat every GIF frame as its own PNG image
        gif_im.seek(frame)
        png_im = gif_im

        # Need to change size to fit desired dimensions
        # Each pixel will be one emoji, so it's args.per_line
        resized_im = png_im
        if args.per_line:
            resized_im = resize_image(png_im, args.per_line)

        # And map all its colors into the global palette's colors
        colored_im = colorize_image(resized_im)

        bg_im = create_gif_frame(emoji_im, colored_im, frame, args)
        bg_frame_images.append(bg_im)

    # Convert GIF frames into an actual GIF
    fn = get_output_filename(emoji_im, gif_im, args)
    save_gif(bg_frame_images, fn, args.delay)


def create_gif_frame(
    emoji_im: _Image, png_im: _Image, frame_no: int, args: Namespace
) -> _Image:
    """
    For every frame in the emoji GIF, create a new frame in the output GIF
    using the PNG but all pixels are "replaced" with the emoji frame colored
    to that pixel's RGB.
    """
    # Total GIF width divided by number of emojis required on the X-axis
    # (png_im has been resized to args.per_line)
    emoji_width = args.width // png_im.width

    # Dimensions of final output GIF
    gif_size = (
        args.width,
        int(args.width / png_im.width * png_im.height),
    )

    background_im = Image.new("RGB", gif_size, (0, 0, 0))

    for y in range(png_im.height):
        for x in range(png_im.width):

            # png_im is mode "P", so its color values are range(0, 256)
            # and we map its pixels to an RGB color for the emojis
            color_rgb = get_palette_rgb(png_im.getpixel((x, y)))
            emoji_frame_no = frame_no % emoji_im.n_frames

            # My attempt at speeding up this script
            key = (emoji_frame_no, color_rgb)
            if key not in image_cache:
                # Change the hue of the emoji frame
                emoji_im.seek(emoji_frame_no)
                colored_frame_im = change_image_hue(emoji_im.convert("RGBA"), color_rgb)
                image_cache[key] = colored_frame_im.resize((emoji_width, emoji_width))

            # Copy the colored emoji frame onto the blank image
            background_im.paste(image_cache[key], (emoji_width * x, emoji_width * y))

    return background_im


def change_image_hue(im: _Image, rgb: ColorRGB) -> _Image:
    """
    Changes the hue of an image to a given RGB color and returns the new image.

    Source: Stack Overflow
    """
    r, g, b, a = im.split()
    r_data = []
    g_data = []
    b_data = []
    a_data = []

    for rd, gr, bl, al in zip(r.getdata(), g.getdata(), b.getdata(), a.getdata()):
        s, v = colorsys.rgb_to_hsv(rd / 255, gr / 255, bl / 255)[1:]
        h1, s1, v1 = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        hp, sp, vp = colorsys.hsv_to_rgb(h1, s1 if s1 < s else s, v1 if v1 < v else v)
        r_data.append(hp * 255)
        g_data.append(sp * 255)
        b_data.append(vp * 255)
        a_data.append(al)
    r.putdata(r_data)
    g.putdata(g_data)
    b.putdata(b_data)
    a.putdata(a_data)

    return Image.merge("RGBA", (r, g, b, a))


def colorize_image(im: _Image) -> _Image:
    """
    Transform an image's colors to a different color palette.
    """
    return im.convert("RGB").quantize(palette=palette_im)


def resize_image(im: _Image, width: int) -> _Image:
    """
    Resize an image to a certain width while maintaining aspect ratio.
    """
    return im.resize((width, int(width / im.width * im.height)))


# Save GIF to disk
def save_gif(frame_images: list[_Image], filename: str, delay: int):
    """
    Saves a list of Pillow images as a GIF.
    """
    if not frame_images:
        raise ValueError("Must have at least one frame")

    frame_images[0].save(
        filename,
        save_all=True,
        format="GIF",
        duration=delay,
        loop=0,
        transparency=0,
        disposal=2,
        append_images=frame_images[1:],
    )

    print("\nSaved:", filename)


def get_output_filename(emoji_im: _Image, im: _Image, args: Namespace) -> str:
    """
    Create a filename for the output according to program inputs.
    """
    input_name = os.path.basename(getattr(im, "filename")).split(".")[0]
    emoji_name = os.path.basename(getattr(emoji_im, "filename")).split(".")[0]
    dimensions = f"{args.per_line}-{args.width}"
    return f"{input_name}-{emoji_name}-{dimensions}.gif"


def main(args: Namespace):
    if args.use_gif:
        gif_to_gif(args)
    else:
        png_to_gif(args)


if __name__ == "__main__":
    main(parse_args())
