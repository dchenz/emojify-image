from PIL import Image
import colorsys

# Source: stackoverflow.com
def to_rgb_colour(im, rgb):
    r, g, b, a = im.split()
    r_data = []
    g_data = []
    b_data = []
    a_data = []
    for rd, gr, bl, al in zip(r.getdata(), g.getdata(), b.getdata(), a.getdata()):
        s, v = colorsys.rgb_to_hsv(rd / 255, gr / 255, bl / 255)[1:]
        h1, s1, v1 = colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        rd, gr, bl = [
            int(x * 255)
            for x in colorsys.hsv_to_rgb(h1, s1 if s1 < s else s, v1 if v1 < v else v)
        ]
        r_data.append(rd)
        g_data.append(gr)
        b_data.append(bl)
        a_data.append(al)
    r.putdata(r_data)
    g.putdata(g_data)
    b.putdata(b_data)
    a.putdata(a_data)
    return Image.merge("RGBA", (r, g, b, a))


def generate_emote_palette(palette_im):
    assert palette_im.width * palette_im.height == 256
    palette_rgb = palette_im.convert("RGB")
    palette_p = palette_im.convert("P")
    emote_256_to_rgb = {}
    duplicate_colours = []
    for y in range(palette_im.height):
        for x in range(palette_im.width):
            colour_rgb = palette_rgb.getpixel((x, y))
            colour_256 = palette_p.getpixel((x, y))
            if colour_256 in emote_256_to_rgb:
                duplicate_colours.append(colour_rgb)
            else:
                emote_256_to_rgb[colour_256] = colour_rgb
    _assign_nearest_vacancies(emote_256_to_rgb, duplicate_colours)
    return emote_256_to_rgb


# Fill any missing colours or remove duplicates
def _assign_nearest_vacancies(emote_256_to_rgb, duplicate_colours):
    vacancies = sorted(set(range(256)).difference(set(emote_256_to_rgb.keys())))
    assert len(vacancies) == len(duplicate_colours)
    for i, vac in enumerate(vacancies):
        emote_256_to_rgb[vac] = duplicate_colours[i]
    assert len(emote_256_to_rgb.keys()) == 256
