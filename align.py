from astropy.io import fits
from glob import glob
import numpy as np
import re


def main():
    pattern = re.compile(r'light/(\d+)_([^_]+)_\-(\d+)_(\D+)_(\d+m)\.[fits]+')
    files = list({pattern.match(f).groups() for f in glob('light/*.fit')})

    print('## Processing darks...')
    darks = {dura: load_fits(f'dark/*_Dark_{dura}-*.fit')
             for dura in {i[4] for i in files}}
    print('## Processing flats...')
    flats = {band: load_fits(f'flat/*_Flat_{band}-*.fit')
             for band in {i[3] for i in files}}

    lights = {}
    for f in glob('light/*.fit'):
        [date, target, seq, band, dura] = pattern.match(f).groups()
        print(f'processing {target=}, {date=}, {band=}, {dura=}, {seq=}')

        light = load_fits(f)
        dark = darks[dura]
        flat = flats[band]

        frame = np.clip((light - dark) / flat
                        * np.percentile(flat, 3), 0, 262144)
        lights.setdefault(f'{target}-{date}', {}
                          )[f'{band}-{dura}-{seq}'] = frame
        save_fits(frame,
                  f'calibrated/{target}-{date}-{band}-{dura}-{seq}.fits')

    """
    lights = {}
    for f in glob('calibrated/*.fits'):
        target, key = f[11:-5].split('-', 1)
        lights.setdefault(target, {})[key] = load_fits(f)
    """

    print('## Normalize brightness...')
    for target, frames in lights.items():
        p = {key: np.percentile(frame, 50) for key, frame in frames.items()}
        print(f'processing {target} (len = {len(frames)})')
        for key, frame in frames.items():
            lights[target][key] = frame / p[key] * np.mean(list(p.values()))
            save_fits(lights[target][key], f'normalized/{target}-{key}.fits')

    print('## Aligning frames...')
    for target, frames in lights.items():
        print(f'### processing {target}')

        key = None
        for k in frames.keys():
            if 'V' in k and '-003' in k:
                key = k
        if not key:
            key = list(frames.keys())[0]
            print(f'Warning: no V-002 in {target=}, using {key=}')

        for f in frames.keys():
            [d, ox, oy] = align_frame(frames[key], frames[f])

            print(f'{f=}\t{d:.2f}\t({ox}, {oy})')
            aligned = np.zeros((4567, 6024))
            aligned[96+ox:96+4375+ox, 96+oy:96+5832+oy] = frames[f]
            save_fits(aligned, f'aligned/{target}-{f}.fits')


def align_frame(f0, f1):
    best = [1e9, 0, 0]
    for ox in range(-15, 15):
        for oy in range(-15, 15):
            sample = (f0[800+ox:1200+ox, 800+oy:1200+oy] -
                      f1[800:1200, 800:1200])
            d = np.mean(np.abs(sample))
            if d < best[0]:
                best = [d, ox, oy]
    if abs(best[1]) < 12 and abs(best[2]) < 12:
        return best

    best = [1e9, 0, 0]
    for ox in range(-30, 30):
        for oy in range(-30, 30):
            sample = (f0[600+ox:1400+ox, 600+oy:1400+oy] -
                      f1[600:1400, 600:1400])
            d = np.mean(np.abs(sample))
            if d < best[0]:
                best = [d, ox, oy]
    if abs(best[1]) < 24 and abs(best[2]) < 24:
        return best

    best = [1e9, 0, 0]
    for ox in range(-60, 60):
        for oy in range(-60, 60):
            sample = (f0[600+ox:1400+ox, 600+oy:1400+oy] -
                      f1[600:1400, 600:1400])
            d = np.mean(np.abs(sample))
            if d < best[0]:
                best = [d, ox, oy]
    return best


def load_fits(frame_list):
    print(f'load_fits({frame_list = }):')
    frame_list = glob(frame_list)
    frames = [np.array(fits.open(f)[0].section[:]) for f in frame_list]
    frames = np.array(frames)
    if len(frame_list) == 1:
        return frames[0]
    if len(frame_list) < 5:
        return np.median(frames, 0)
    mean = frames.mean(0)
    stddev = frames.std(0)
    return np.nanmean([nan_if(f, mean, stddev) for f in frames], 0)


def save_fits(frame, filename):
    frame = fits.HDUList([fits.PrimaryHDU(frame)])
    frame.writeto(filename, overwrite=True)


def nan_if(arr, mean, std):
    return np.where(np.abs(arr - mean) > std * 1, np.nan, arr)


if __name__ == '__main__':
    main()
