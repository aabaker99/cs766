Review article that describes different problems in the field: https://www.nature.com/articles/nmeth.4397
Paper accompanying cell image dataset: https://academic.oup.com/gigascience/article/6/12/giw014/2865213
Image data for the 5 channels: http://www.cellimagelibrary.org/pages/project_20269
http://gigadb.org/dataset/100351

# profiles/mean\_well\_profiles.csv
- Probably a mean over the 4 replicates done in the experiment (quadruplicates).
- Contains data that is also present in extracted\_features/<ID>.sqlite where columns in the csv are named <TABLE_NAME>_<COLUMN_NAME>
- Contains metadata that is not present in extracted\_features/<ID>.sqlite such as the ID of the chemical used to treat the cells in @Metadata\_broad\_sample@

# Channels
1) Nucleus
2) Endoplasmic reticulum
3) Nucleoli
4) F-actin cytoskeleton, Golgi, plasma membrane
5) Mitochondria

# Segmentation
* Analyze nucleus channel to define cluster centers
  * bwlabel to count the number of objects (use max)
  * find the object centers
* Use the object centers to do a clustering-based object segmentation in the channel 4 images
  * Apply threshold to remove background pixels (Otsu)
  * Apply bwconncomp to find objects
  * Compare to k-means clustering with pixel features: x, y, intensity
  * Beware of gaps in stain between the nuclear membrane and the cell membrane
  * Some cells are close together so bwconncomp may identify two different cells as the same cell: how to fix?
