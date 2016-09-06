=========================
Allen Human Brain Atlas
=========================

This data set contains all microarray samples for all probes in 1 brain.

MicroarrayExpression.csv

    Contains normalized expression values arranged by (row, column) =
    (probe, samples).  The first column is the probe ID.

PACall.csv 

    Contains a present/absent flag which indicates whether the probe's
    expression is well above background.  It is set to 1 when both of the
    following conditions are met.
    
        1) The 2-sided t-test p-value is lower than 0.01, (indicating the mean
           signal of the probe's expression is significantly different from the
           corresponding background).
        2) The difference between the background subtracted signal and the
           background is significant (> 2.6 * background standard deviation).

Probes.csv

    Metadata for the probes in MicroarrayExpression.csv.

Ontology.csv

    The ontology on brain structures used for sampling.

SampleAnnot.csv

    The samples are listed in the same order as the columns in
    MicroarrayExpression.csv; the locations of all sampled structures are given
    in native MRI voxel coordinates (mri_cx, mri_cy, mri_cz) as well as MNI
    coordinates.

The MRI data can be downloaded from http://human.brain-map.org/mri_viewers/data.
