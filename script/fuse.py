#!/usr/bin/env python
from skimage.io import imread, imsave
import argparse, sys
import numpy as np

def rescale(arr):
  arr_min = np.min(arr)
  arr_max = np.max(arr)
  arr_frac = (arr - arr_min) / (arr_max - arr_min)
  rv = (arr_frac * 256).astype('uint8')
  return rv

if __name__ == '__main__':
  parser = argparse.ArgumentParser("""
Rescale and fuse grayscale images together
""")
  parser.add_argument('--images', '-i', help='Grayscale images to fuse', nargs='+', required=True)
  parser.add_argument('--outfile', '-o', help='Output image', required=True)
  args = parser.parse_args()

  images = list(map(lambda x: imread(x), args.images))
  shape0 = images[0].shape
  for i in range(1, len(images)):
    if images[i].shape != shape0:
      sys.stderr.write('Input images are not of the same size: {} != {} for {} and {}\n'.format(shape0, images[i].shape, args.images[0], args.images[i]))
      sys.exit(1)

  images_rescaled = list(map(lambda x: rescale(x), images))
  scalars = (1 / len(images_rescaled)) * np.ones(len(images_rescaled))

  # linearly scale to 0-255 before fusing
  product = np.zeros(shape0)
  for i, image in enumerate(images):
    product += scalars[i] * image

  imsave(args.outfile, product.astype('uint8'))
