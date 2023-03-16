from astropy.io import fits
from glob import glob
import numpy as np
import re


def main():
    pattern = re.compile(r'light/(\d+)\-([^-]+)\-(\d+)(\D+)(\d+s)\.[fits]+')
    files = list({pattern.match(f).groups() for f in glob('light/*.fits')})

    print('## Processing darks...')
    darks = {d: fits_avg(f'dark/{d}/*.fts') for d in {i[4] for i in files}}
    print('## Processing flats...')
    flats = {f'{d}_{b}': fits_avg(f'flat/{d}/{b}/*.fts')
             for (d, b) in {(i[0], i[3]) for i in files}}

    lights = {}
    for f in glob('light/*.fits'):  # For all file again
        [date, target, seq, band, dura] = pattern.match(f).groups()
        print(f'processing {target=}, {band=}, {dura=}, {seq=}')

        light = fits_avg(f)
        dark = darks[dura]
        flat = flats[f'{date}_{band}']

        frame = (light - dark) / flat * np.percentile(flat, 3)
        lights.setdefault(f'{target}-{band}-{dura}-{date}', {})[seq] = frame

    print('## Normalizing...')
    for target, frames in lights.items():
        p = {seq: np.percentile(frame, 50) for seq, frame in frames.items()}
        for seq, frame in frames.items():
            frame = frame / p[seq] * np.mean(list(p.values()))
            frame = fits.HDUList([fits.PrimaryHDU(frame)])
            frame.writeto(f'clear/{target}-{seq}.fits', overwrite=True)


def fits_avg(frame_list):
    frame_list = glob(frame_list)
    frames = [np.array(fits.open(f)[0].section[:]) for f in frame_list]
    frames = np.array(frames)
    if len(frame_list) < 5:
        return np.median(frames, 0)
    mean = frames.mean(0)
    stddev = frames.std(0)
    return np.nanmean([nan_if(f, mean, stddev) for f in frames], 0)


def nan_if(arr, mean, std):
    return np.where(np.abs(arr - mean) > std * 1, np.nan, arr)


if __name__ == '__main__':
    main()
