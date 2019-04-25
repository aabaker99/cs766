#!/usr/bin/env python
import sys, argparse
import os, os.path
import numpy as np

TREATMENTS_HEADER = [
  'plate',
  'well',
  'compound_id',
  'compound_label'
]

def parse_mean_well_profiles(chem_to_label, profiles_dir, ofp):
  """
  Parameters
  ----------
  """
  N_METADATA_FIELDS = 17

  plate_field = 'Metadata_Plate'
  well_field = 'Metadata_Well'
  compound_field = 'Metadata_pert_mfc_id' # <brd-id> (in chemical_annotations.csv) or 'na'
  #role_field = 'Metadata_ASSAY_WELL_ROLE' # 'treated' or 'mock'

  plate_dirs = os.listdir(profiles_dir)
  profile_fps = map(lambda plate_dir: os.path.join(profiles_dir, plate_dir, 'profiles', 'mean_well_profiles.csv'), plate_dirs)

  ofh = open(ofp, 'w')
  ofh.write(','.join(TREATMENTS_HEADER) + '\n')
  for fp in profile_fps:
    header = None
    with open(fp) as fh:
      for line in fh:
        line = line.rstrip()
        header = line.split(',')
        break
      header = header[:N_METADATA_FIELDS]

      field_to_index = {}
      for i,field in enumerate(header):
        field_to_index[field] = i

      for line in fh:
        line = line.rstrip()
        rec = line.split(',')

        compound = rec[field_to_index[compound_field]]
        label = chem_to_label.get(compound)
        if label is None:
          label = 0

        ofh.write(','.join([
          rec[field_to_index[plate_field]],
          rec[field_to_index[well_field]],
          compound,
          str(label)
        ]) + '\n')

  ofh.close()

def parse_chemical_annotations(fp):
  """
  Map compound id to line number (ignoring header)
  """
  rv = {}
  with open(fp) as fh:
    # skip header
    for line in fh:
      break 

    i = 0
    for line in fh:
      i += 1
      line = line.rstrip()
      words = line.split(',')
      rv[words[0]] = i
  return rv

def main():
  parser = argparse.ArgumentParser(description="""
Construct a CSV which labels wells with an integer label for their chemical treatment.
Controls are labelled 0.
Treatments are assigned the integer which is the line number in <--chemical-annotations>.
The output CSV file consists of the fields plate, well, treatment-id, treatment-label

--profiles-dir is the directory obtained from extracting ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100351/profiles.tar.gz
--chemical-annotations is the file available at ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100351/chemical_annotations.csv
""")
  parser.add_argument('--profiles-dir', '-p')
  parser.add_argument('--chemical-annotations', '-c')
  parser.add_argument('--outfile', '-o')
  args = parser.parse_args()

  chem_to_label = parse_chemical_annotations(args.chemical_annotations)
  parse_mean_well_profiles(chem_to_label, args.profiles_dir, args.outfile)

if __name__ == "__main__":
  main()
