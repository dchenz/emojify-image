# Image Emotify

## Generating GIF using PNG

### Usage

```sh
# Suppose the emote "kek.gif" is located in current directory...
python3 run.py image.png kek.gif

 # Above, but overriding the default values
python3 run.py image.gif kek.gif --fromGIF --width 1536 --line 64
```

### Configuration

- ``EMOTES_PER_LINE``: Number of emotes on one line. (default: 64)
- ``GIF_WIDTH``: Width of the final GIF. Height is automatic. (default: 2048)
- ``GIF_FRAME_DELAY``: Number of milliseconds between GIF frames. (default: 45)

## Generating GIF using GIF

### Usage

```sh
# Suppose the emote "kek.gif" is located in current directory...
python3 run.py image.gif kek.gif --fromGIF

 # Above, but overriding the default values
python3 run.py image.gif kek.gif --fromGIF --width 1536 --line 64
```

- Image must end with ``.gif`` if using ``--fromGIF`` option.

### Configuration

- ``EMOTES_PER_LINE``: Number of emotes on one line. (default: 32)
- ``GIF_WIDTH``: Width of the final GIF. Height is automatic. (default: 1024)
- ``GIF_FRAME_DELAY``: Number of milliseconds between GIF frames. (default: 45)
