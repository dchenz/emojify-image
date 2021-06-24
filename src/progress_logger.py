# PNG to GIF
# ----------
# Emote Size:   24 x 24 (6 frames)
# Input Size:   480 x 480
# Progress:     4 / 6

# GIF to GIF
# ----------
# Emote Size:   24 x 24 (6 frames)
# Input Size:   600 x 600 (73 frames)
# Progress:     12 / 73

# mode 0 == PNG to GIF, mode 1 == GIF to GIF
def on_load_log(emote_im, input_im, mode=0):
  if mode == 0:
    print("\nPNG to GIF")
  else:
    print("\nGIF to GIF")
  print("-" * 10 + "\n")
  _log_emote_size(emote_im.size, emote_im.n_frames)
  _log_input_size(input_im.size, None if mode == 0 else input_im.n_frames)

def on_progress_log(emote_im, input_im, frame, mode=0):
  if frame == 0:
    print()
  _log_progress(frame + 1, emote_im.n_frames if mode == 0 else input_im.n_frames, clear=(frame > 0))

# Do the actual logging here

def _log_emote_size(dimensions, frames):
  print(f'Emote Size:\t{dimensions[0]:4d} x {dimensions[1]:4d} ({frames} frames)')

def _log_input_size(dimensions, frames=None):
  print(f'Input Size:\t{dimensions[0]:4d} x {dimensions[1]:4d}',
    f'({frames} frames)' if frames is not None else "")

def _log_progress(cur, total, clear=False):
  text = f'Progress:       Frame {cur} of {total}'
  if clear:
    print("\b" * len(text), end="")
  print(text, end="" if cur < total else "\n", flush=True)