from astropy.visualization import make_lupton_rgb
from astropy.io import fits
from glob import glob
import numpy as np


def main():
    print('## Merging frames...')
    for target in {f[8:].rsplit('-', 2)[0] for f in glob('aligned/*.fits')}:
        print(f'processing {target=}')
        frame_list = glob(f'aligned/{target}-*.fits')
        frames = [np.array(fits.open(f)[0].section[:]) for f in frame_list]
        frames = np.array(frames)

        mean = frames.mean(0)
        stddev = frames.std(0)
        frame = np.nanmean([nan_if(f, mean, stddev) for f in frames], 0)

        frame = fits.HDUList([fits.PrimaryHDU(frame)])
        frame.writeto(f'merged/{target}.fits', overwrite=True)

    print('## Making RBG preview...')
    for target in {f[7:].rsplit('-', 1)[0] for f in glob('merged/*.fits')}:
        try:
            frames = [np.array(fits.open(f'merged/{target}-{band}.fits')[0]
                               .section[:]) for band in ['B', 'V', 'R']]
            make_lupton_rgb(*frames, minimum=np.percentile(frames, 90),
                            filename=f'merged/{target}-preview.png')
        except FileNotFoundError:
            print(f'Fail to build (B, V, R) image preview for {target=}')


def nan_if(arr, mean, std):
    return np.where(np.abs(arr - mean) > std * 1, np.nan, arr)


if __name__ == '__main__':
    main()
