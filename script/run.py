#!/usr/bin/env python
import sys, argparse
import os, os.path
import subprocess as sp
import requests
import re
import itertools as it

# 406 plates
# 24277
PLATES = [24278, 24279, 24280, 24293, 24294, 24295, 24296, 24297, 24300, 24301, 24302, 24303, 24304, 24305, 24306, 24307, 24308, 24309, 24310, 24311, 24312, 24313, 24319, 24320, 24321, 24352, 24357, 24507, 24508, 24509, 24512, 24514, 24515, 24516, 24517, 24518, 24523, 24525, 24560, 24562, 24563, 24564, 24565, 24566, 24583, 24584, 24585, 24586, 24588, 24590, 24591, 24592, 24593, 24594, 24595, 24596, 24602, 24604, 24605, 24609, 24611, 24617, 24618, 24619, 24623, 24624, 24625, 24631, 24633, 24634, 24635, 24636, 24637, 24638, 24639, 24640, 24641, 24642, 24643, 24644, 24645, 24646, 24647, 24648, 24651, 24652, 24653, 24654, 24655, 24656, 24657, 24661, 24663, 24664, 24666, 24667, 24683, 24684, 24685, 24687, 24688, 24726, 24731, 24732, 24733, 24734, 24735, 24736, 24739, 24740, 24750, 24751, 24752, 24753, 24754, 24755, 24756, 24758, 24759, 24772, 24773, 24774, 24775, 24783, 24785, 24789, 24792, 24793, 24795, 24796, 24797, 25372, 25374, 25376, 25378, 25380, 25382, 25387, 25391, 25392, 25403, 25406, 25408, 25410, 25414, 25416, 25418, 25420, 25422, 25424, 25426, 25428, 25430, 25432, 25434, 25435, 25436, 25438, 25485, 25488, 25490, 25492, 25503, 25553, 25564, 25565, 25566, 25567, 25568, 25569, 25570, 25571, 25572, 25573, 25575, 25576, 25578, 25579, 25580, 25581, 25583, 25584, 25585, 25587, 25588, 25590, 25591, 25592, 25593, 25594, 25598, 25599, 25605, 25638, 25639, 25641, 25642, 25643, 25663, 25664, 25665, 25667, 25674, 25675, 25676, 25677, 25678, 25679, 25680, 25681, 25683, 25686, 25688, 25689, 25690, 25692, 25694, 25695, 25700, 25704, 25707, 25708, 25724, 25725, 25726, 25732, 25738, 25739, 25740, 25741, 25742, 25847, 25848, 25849, 25852, 25853, 25854, 25855, 25856, 25857, 25858, 25859, 25862, 25885, 25890, 25891, 25892, 25903, 25904, 25908, 25909, 25911, 25912, 25913, 25914, 25915, 25918, 25923, 25925, 25929, 25931, 25935, 25937, 25938, 25939, 25943, 25944, 25945, 25949, 25955, 25962, 25965, 25966, 25967, 25968, 25983, 25984, 25985, 25986, 25987, 25988, 25989, 25990, 25991, 25992, 25993, 25994, 25997, 26002, 26006, 26007, 26008, 26009, 26058, 26060, 26061, 26071, 26081, 26092, 26107, 26110, 26115, 26118, 26124, 26126, 26128, 26133, 26135, 26138, 26140, 26159, 26166, 26174, 26181, 26202, 26203, 26204, 26205, 26207, 26216, 26224, 26232, 26239, 26247, 26271, 26521, 26531, 26542, 26544, 26545, 26562, 26563, 26564, 26569, 26572, 26574, 26575, 26576, 26577, 26578, 26579, 26580, 26588, 26592, 26595, 26596, 26598, 26600, 26601, 26607, 26608, 26611, 26612, 26622, 26623, 26625, 26626, 26640, 26641, 26642, 26643, 26644, 26662, 26663, 26664, 26666, 26668, 26669, 26670, 26671, 26672, 26673, 26674, 26675, 26677, 26678, 26679, 26680, 26681, 26682, 26683, 26684, 26685, 26688, 26695, 26702, 26703, 26705, 26724, 26730, 26739, 26744, 26745, 26748, 26752, 26753, 26765, 26767, 26768, 26771, 26772, 26785, 26786, 26794, 26795]
#TEMPLATE = 'https://cildata.crbs.ucsd.edu/broad_data/plate_{}/BBBC022_v1_images_{}w{}.zip'
TEMPLATE = 'https://cildata.crbs.ucsd.edu/broad_data/plate_{}/{}-{}.zip'
#CHANNELS = ['ERSyto', 'ERSytoBleed', 'Hoechst', 'Mito', 'Ph_golgi']

# in same order as ImageXpress w1, w2, ... (check ERSyto and ERSytoBleed, not sure about those)
CHANNELS = ['Hoechst', 'ERSyto', 'ERSytoBleed', 'Ph_golgi', 'Mito']

#https://cildata.crbs.ucsd.edu/broad_data/plate_24278/24278-ERSyto.zip
#https://cildata.crbs.ucsd.edu/broad_data/plate_24278/24278-ERSytoBleed.zip
#https://cildata.crbs.ucsd.edu/broad_data/plate_24278/24278-Hoechst.zip
#https://cildata.crbs.ucsd.edu/broad_data/plate_24278/24278-Mito.zip
#https://cildata.crbs.ucsd.edu/broad_data/plate_24278/24278-Ph_golgi.zip

# Wells 1-384 are numbered A01 to P24
# Fields of view are numbered s1 to s9
g1 = map(lambda x: chr(x), range(ord('A'), ord('P')+1))
g2 = map(lambda x: '{:02d}'.format(x), range(1,24+1))
WELLS = sorted(map(lambda x: x[0]+x[1], it.product(g1, g2)))
WELLS_SET = set(WELLS)
FOVS = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']
FOVS_SET = set(FOVS)

regexp = re.compile('[^_]+_([^_]+)_([^_]+).*\.tif')
def find_well_and_fov(dirpath, well, fov):
  """
  Wells 1-384 are numbered A01 to P24
  Fields of view 1-9 are called s1 to s9
  Files names in <dirpath> contain the well number and field of view string, but also include 
    a hash function result in the file name, so we do not know the exact file name
  An example is IXMtest_A01_s1_w164FBEEF7-F77C-4892-86F5-72D0160D4FB2.tif

  Returns
  -------
  filepath : str or None
  """
  rv = None
  fnames = os.listdir(dirpath)
  for fname in fnames:
    match_data = regexp.match(fname)
    if match_data is not None:
      if match_data.group(1).upper() == well and match_data.group(2).lower() == fov:
        rv = os.path.join(dirpath, fname)
        break
  return rv

def download_and_extract(outdir, plate, channel):
  """
  Download the data associated with <plate> and <channel> and extract it.
  Place raw download and extracted output in <outdir>.

  Returns
  -------
  dirpath : str
    extracted directory
  """
  url = TEMPLATE.format(plate,plate,channel)
  fp = os.path.join(outdir, os.path.basename(url))
  if not os.path.exists(fp):
    args = ['wget', '-P', outdir, url]
    sp.check_call(args) # raises on failure

  # unzipped output is placed in <outdir>, output assumed to exist in a directory <dir> for <dir>.zip
  dirpath, ext = os.path.splitext(fp) 
  if not os.path.exists(dirpath):
    args = ['unzip', '-d', outdir, fp]
    sp.check_call(args)

  return dirpath

# NOTE different from learning.py version, roughy inverted
def read_treatments(treatments_fp):
  """
  Map integer labels to plates
  """
  rv = {}
  with open(treatments_fp, 'r') as fh:
    for line in fh:
      line = line.rstrip()
      plate, well, drug_id, drug_int = line.split(',')
      if drug_int in rv:
        rv[drug_int].append(plate)
      else:
        rv[drug_int] = [plate]
  return rv

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--outdir", required=True)
  parser.add_argument('--treatments', '-t', required=True)
  parser.add_argument('--treatment-sample')
  parser.add_argument('--plate', '-p', help='Download a specific plate')
  parser.add_argument('--well', '-w')
  parser.add_argument('--field-of-view', '-f')
  parser.add_argument('--list', help='List plates', action='store_true')
  args = parser.parse_args()

  if args.list:
    for plate in PLATES:
      print(plate)
    sys.exit(0)

  # TODO remove
  PLATES = None
  if args.treatment_sample is not None:
    treatment_to_plates = read_treatments(args.treatments)

    # then define plates by the desired treatments to test
    treatments = []
    with open(args.treatment_sample) as fh:
      for line in fh:
        line = line.rstrip()
        treatments.append(line)

    plates_set = set()
    for treatment in treatments:
      plates = treatment_to_plates[treatment]
      for plate in plates:
        plates_set.add(plate)
    PLATES = sorted(list(plates_set))
  else:
    PLATES = ['24278']

  fov = 's1'
  feature_fps = []
  print(PLATES)
  for plate in PLATES:
    for well in WELLS:
      nucleus_dp = download_and_extract(args.outdir, plate, CHANNELS[0])
      nucleus_fp = find_well_and_fov(nucleus_dp, well, fov)
      nucleus_coord_csv = os.path.join(args.outdir, '{}_{}_{}_nucleus_centers.csv'.format(plate, well, fov))

      golgi_dp = download_and_extract(args.outdir, plate, CHANNELS[3])
      golgi_fp = find_well_and_fov(golgi_dp, well, fov)

      # identify nuclei centers to initialize kNN
      matlab_args = ['matlab', '-nosplash', '-nodisplay', '-r', 'cell_centers(\'{}\', \'{}\'); quit'.format(nucleus_fp, nucleus_coord_csv)]
      print(matlab_args)
      sp.check_call(matlab_args)

      # fuse nucleus and golgi channels
      fused_outfile = os.path.join(args.outdir, '{}_{}_{}_fused.tif'.format(plate, well, fov))
      fuse_args = ['fuse.py', '--images', nucleus_fp, golgi_fp, '--outfile', fused_outfile]
      sp.check_call(fuse_args)

      # clustering
      cluster_labels_fp = os.path.join(args.outdir, '{}_{}_{}_clusters.csv'.format(plate, well, fov))
      clustering_args = ['cell_clustering.py', '--cell-centers', nucleus_coord_csv, '--image-file', fused_outfile, '--outfile', cluster_labels_fp] # can also provide --outdir to see images
      sp.check_call(clustering_args)

      # feature extraction
      feature_fp = os.path.join(args.outdir, '{}_{}_{}_features.csv'.format(plate, well, fov))
      extract_args = ['extract_features.py', '-p', plate, '-w', well, '-i', fused_outfile, '-l', cluster_labels_fp, '-t', args.treatments, '-o', feature_fp]
      sp.check_call(extract_args)
      feature_fps.append(feature_fp)

  # concatenate feature files
  all_feature_fp = os.path.join(args.outdir, 'all_features.csv')
  cat_args = ['cat'] + feature_fps
  sp.check_call(cat_args, stdout=all_feature_fp)

  # learning
  learning_args = ['learn.py', '--data', all_feature_fp, '--treatments', args.treatments, '--outdir', args.outdir]
  sp.check_call(learning_args)
  
if __name__ == "__main__":
  main()
