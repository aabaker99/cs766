# CS 766: Vision Approaches in Phenotypic Cell Approaches
_Aaron Baker, Ragini Rathore_

## Motivation
The cost of developing a drug [is estimated to be somewhere between $320 million to $2.7 billion](https://blogs.sciencemag.org/pipeline/archives/2017/10/18/drug-development-costs-revisited).
Recent technological advances have enabled new approaches to drug development.
In particular, automated lab and microscopy equipment facilitates high-throughput [phenotypic cell profiling experiments](http://dx.doi.org/10.1038/nprot.2016.105).
Phenotypic cell profiling experiments often perturb a cell with a chemical and then measure the effect on the cell.
One way to measure the effect is through microscopic imaging.
Many experiments of this form can be conducted simulatenously by organizing each experiment into a well on a multi-well plate, and by using machines designed to process the plates.

![phenotypic cell profiling overview](/Images/intro.png)
*![Source: Bray et al. 2016](http://dx.doi.org/10.1038/nprot.2016.105)*

This project analyzed a part of ![a dataset](http://dx.doi.org/10.1093/gigascience/giw014) which contains images associated with 30,000 chemical treatments of bone cancer cells.
In each experiment, five different dyes are applied to the cells to illuminate different parts of the cell under a microscope.
The cells used for this dataset reside in a DMSO solvent, and DMSO is also used as a treatment control.
The following image shows two sets of sample images from this dataset, one which has been treated with the control and one which has been treated with Parbendazole.

![sample case and control images](/Images/sample_case_control.png)
*![Source: Bray et al. 2017](http://dx.doi.org/10.1093/gigascience/giw014)*

There appears to be a significant difference between these two sets of images.
That is, Parbendazole appears to have some effect.
Our project aims to discover these types of differences at a large scale, using computer vision tools to analyze the cell images.
We developed a software pipeline which identifies drugs that affect bone cancer.
1. Segment images of cell populations into images of individual cells.
2. Featurize individual cell images.
3. Train a classifier to distinguish treated and untreated cells.
While a traditional applications of machine learning would be interested in using the classifier to predict whether a new cell image has been treated or not, we note that this interpretation of the classifier is not particularly useful because we already know if the cells have been treated or not.
Instead, if a classifier is able to achieve good performance, there must be some difference between the features of treated and untreated cells.
In that case, the drug has some apparent effect and we recommend that it is studied more thoroughly.

We focused on innovating in the segmentation task, and applied off-the-shelf methods for featurization and classification.
We adapted ![Watershed segmentation](https://en.wikipedia.org/wiki/Watershed_%28image_processing%29) and compared it to ![k-means clustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html).
We featurized cell images by extracting ![region](https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.regionprops) and ![texture](https://scikit-image.org/docs/0.7.0/api/skimage.feature.texture.html) properties.
Finally, we classified images using a ![simple logistic regression classifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html).
We evaluated the performance of the classifiers by average precision, and plotted precision-recall curves.

## State-of-the-art
![](/Images/voronoi.png)
## Implementation
  ### Pre-processing
  ### Segmentation Algorithms
## Learning using Segmented Cells
## Conclusion
## Difficulties and Challenges
## Learnings and Future Work
- Segmenting cells is difficult due to cell-to-cell contacts.
- Novel frameworks for evaluating drug efficacy.
- Evaluate more drugs with more compute power.

