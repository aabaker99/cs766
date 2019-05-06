#!/usr/bin/env python
import argparse, sys
import numpy as np
import skimage
import skimage.io
import skimage.exposure
import easygui


def main():
#   parser = argparse.ArgumentParser(description="""
# Brighten an image with histogram normalization. 
# Note that the file type is determined by the extension of outfile. 
# Some extensions will result in a white image. 
# These include .tif and .tiff. 
# Try .png instead.
# """)
#   parser.add_argument('--infile', required=True)
#   parser.add_argument('--outfile', required=True)
#   args = parser.parse_args()


  path = easygui.fileopenbox()
  print(path)
  #arr = skimage.img_as_float(skimage.io.imread(args.infile))
  arr = skimage.img_as_float(skimage.io.imread(path))

  arr2 = skimage.exposure.equalize_hist(arr)
  #skimage.io.imsave(args.outfile, arr2)
  skimage.io.imsave("temp.png", arr2)

if __name__ == "__main__":
  main()
