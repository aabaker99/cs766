#!/usr/bin/env python
import sys, argparse
import numpy as np
from skimage.io import imread
from skimage.measure import regionprops
from skimage.feature.texture import greycomatrix, greycoprops

SCALAR_REGION_PROPERTIES = [
  'area',
  'convex_area',
  'eccentricity',
  'equivalent_diameter',
  'euler_number',
  'extent',
  'major_axis_length',
  'minor_axis_length',
  'max_intensity',
  'mean_intensity',
  'min_intensity',
  'orientation',
  'perimeter',
  'solidity',
]

OTHER_REGION_PROPERTIES = [
  'local_centroid_row',
  'local_centroid_col',
  'weighted_centroid_row',
  'weighted_centroid_col'
]

TEXTURE_PROPS = [
  'contrast',
  'dissimilarity',
  'homogeneity',
  'ASM',
  'energy',
  'correlation'
]

HEADER = SCALAR_REGION_PROPERTIES + OTHER_REGION_PROPERTIES + TEXTURE_PROPS

def main():
  parser = argparse.ArgumentParser(description="""
Construct a traditional machine learning data matrix by extracting features from the objects in images.
""")
  parser.add_argument("--input-image", "-i", help="Input image for which cell_clustering.py was run on to produce --label-image.", required=True)
  parser.add_argument("--label-image", "-l", help="Output of cell_clustering.py or other method for segmenting images. Must be a CSV of an array of the same shape as the input image and has an integer in each cell assigning a pixel to an object. -1 is used for background pixels. Objects start counting at 0.", required=True)
  parser.add_argument("--treatments", "-t", help="Treatment metadata file output from parse_treatment.py")
  parser.add_argument("--outfile", "-o", help="Output CSV which is a traditional ML data matrix with shape n_objects x n_features. The objects correspond to the objects in the --infile. The features include region properties, texture properties, and which chemical treatment was used.")
  args = parser.parse_args()

  ofh = open(args.outfile, 'w')

  intensity_image = imread(args.input_image)
  label_image = np.genfromtxt(args.label_image, delimiter=",").astype('int') + 1

  ofh.write('#{}\n'.format(",".join(HEADER)))
  for i in range(np.max(label_image)):
    intensity_image_slice = np.copy(intensity_image)
    intensity_image_slice[label_image != i+1] = 0

    label_image_bool = np.copy(label_image)
    label_image_bool[label_image != i+1] = 0
    label_image_bool[label_image == i+1] = 1

    prop_list = regionprops(label_image_bool, intensity_image_slice)
    prop = prop_list[0]
    # region properties - {{
    # extract simple scalar region properties
    scalar_region_props = list(map(lambda x: prop[x], SCALAR_REGION_PROPERTIES))

    # extract region properties that require some processing
    local_centroid_row = prop['local_centroid'][0]
    local_centroid_col = prop['local_centroid'][1]
    weighted_centroid_row = prop['weighted_centroid'][0]
    weighted_centroid_col = prop['weighted_centroid'][1]

    region_props = scalar_region_props + [local_centroid_row, local_centroid_col, weighted_centroid_row, weighted_centroid_col]
    # }} - region properties

    # extract texture properties for the object i - {{

    # 2nd and 3rd parameters encode a 1-pixel offset to the right, up, left, and down
    # n_dists = 1, n_angle = 4
    grey_rv = greycomatrix(intensity_image_slice, [1], [0, np.pi/2, np.pi, 3*np.pi/2], levels=np.max(intensity_image_slice+1))
    # greycoprops is (n_dist x n_angle)
    # compute average of the texture property
    avg_texture_props = []
    for texture_prop in TEXTURE_PROPS:
      props_rv = greycoprops(grey_rv, texture_prop)
      avg_texture_props.append(np.mean(props_rv))
    # }} - texture properties

    # combine all properties
    all_props = region_props + avg_texture_props
    ofh.write(','.join(map(str, all_props)) + '\n')

if __name__ == "__main__":
  main()
