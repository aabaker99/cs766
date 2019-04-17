#!/usr/bin/env python
import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.io import imshow

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--image-infile", "-i")
  parser.add_argument("--centers", "-c")
  parser.add_argument("--image-outfile", "-o")
  args = parser.parse_args()

  arr = imread(args.image_infile)
  # coordinates are width,height
  centers = np.genfromtxt(args.centers, delimiter=",")

  imshow(arr)
  fig = plt.gcf()
  ax = fig.axes[0] # imshow comes with associated colorbar, get the axis for the actual image
  xs = list(map(lambda x: x[0], centers))
  ys = list(map(lambda x: x[1], centers))
  ax.plot(xs, ys, 'ro')
  
  plt.savefig(args.image_outfile)

if __name__ == "__main__":
  main()
