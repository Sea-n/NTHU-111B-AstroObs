from astropy.io import fits
import numpy as np


def main():
    target = 'M82'
    duration = '60'

    for band in ['b']:
        frames = []
        for seq in range(3):
            filename = f'{target}-{seq+1:03}{band}{duration}s.fits'
            frames.append(np.array(fits.open(filename)[0].section[:]))
        frames = np.array(frames)
        print(f'{band = }\n{seq = }\n{frames = }')
        frame = np.median(frames, 0)
        frame = darkflat(band, duration, frame)
        frame = fits.HDUList([fits.PrimaryHDU(frame)])
        frame.writeto(f'{target}-final-{band}{duration}s.fits')


def darkflat(band, duration, frame):
    frames = []
    for seq in range(10):
        filename = f'dark-{duration}s-{seq+1:03}.fits'
        frames.append(np.array(fits.open(filename)[0].section[:]))
    frames = np.array(frames)
    mean = frames.mean(0)
    stddev = frames.std(0)
    dark = np.nanmean([nan_if(f, mean, stddev) for f in frames], 0)
    print(f'{dark = }')

    frames = []
    for seq in range(5):
        filename = f'flat-{seq+1:03}{band}.fits'
        frames.append(np.array(fits.open(filename)[0].section[:]))
    frames = np.array(frames)
    mean = frames.mean(0)
    stddev = frames.std(0)
    flat = np.nanmean([nan_if(f, mean, stddev) for f in frames], 0)
    print(f'{flat = }')

    frames = []
    for seq in range(10):
        filename = f'bias-{seq+1:03}.fits'
        frames.append(np.array(fits.open(filename)[0].section[:]))
    frames = np.array(frames)
    mean = frames.mean(0)
    stddev = frames.std(0)
    bias = np.nanmean([nan_if(f, mean, stddev) for f in frames], 0)
    print(f'{bias = }')

    print(f'{np.max(frame) = }')
    frame = (frame - dark) / (flat - bias)
    for k in range(10):
        frame1 = frame * np.percentile(flat, k)
        print(f'{k = }, {np.max(frame1) = }')

    return frame


def nan_if(arr, mean, std):
    return np.where(np.abs(arr - mean) > std * 1, np.nan, arr)


if __name__ == '__main__':
    main()
