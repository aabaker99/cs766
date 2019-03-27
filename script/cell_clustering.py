#!/usr/bin/env python
import sys, argparse
import numpy as np
import sklearn.cluster
import skimage.io
import skimage.filters

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--cell-centers', required=True)
  parser.add_argument('--image-file', required=True)
  parser.add_argument('--outfile', required=True)
  args = parser.parse_args()

  cell_centers = np.genfromtxt(args.cell_centers, delimiter=",")
  n_cells, n_dim = cell_centers.shape

  arr = skimage.io.imread(args.image_file)
  arr = arr.transpose() # use MATLAB style for image indexes

  # read intensity at cell center, append it
  intensity = np.zeros((n_cells, 1))
  for i in range(n_cells):
    # adjust for Python origin 0 indexes versus Matlab origin 1 indexes
    x = int(round(cell_centers[i,0])) - 1
    y = int(round(cell_centers[i,1])) - 1
    intensity[i,0] = arr[x,y]
  cell_centers = np.concatenate((cell_centers, intensity), axis=1)

  skimage.io.imread(args.image_file)
  kmeans = sklearn.cluster.KMeans(n_clusters=n_cells, init=cell_centers, n_init=1)

  # reformat image file to (x,y,intensity)
  # only apply clustering to pixels exceeding threshold according to Otsu's method
  val = skimage.filters.threshold_otsu(arr)
  I,J = np.where(arr > val)
  n_points = len(I)

  X = np.zeros((n_points, 3))
  k_to_ij = {}
  k = 0
  for k in range(n_points):
    i = I[k]
    j = J[k]
    k_to_ij[k] = (i,j)
    X[k,:] = (i,j,arr[i,j])

  kmeans.fit(X)
  arr_labels = -1 * np.ones(arr.shape)
  for k in range(n_points): 
    i, j = k_to_ij[k]
    arr_labels[i,j] = kmeans.labels_[k]
  np.savetxt(args.outfile, arr_labels, delimiter=",", fmt='%d')

if __name__ == "__main__":
  main()
