#!/usr/bin/env python

'''
This is the analyses wrapper for the NSPN_CorticalMyelination analyses that
are reported in Adolescent Consolidation of Assocation Cortical Hubs of the 
Human Brain Connectome.

Created by Kirstie Whitaker in October 2015
Contact kw401@cam.ac.uk 
'''

#==============================================================================
# IMPORTS
#==============================================================================
import itertools as it
import os
import pickle
import sys

#==============================================================================
# DEFINE DIRECTORIES
#------------------------------------------------------------------------------
# These are a bunch of useful directory path names with the locations of:
#    FS_SUBJECTS    - the directory containing the raw MRI data and the 
#                       fsaverage directory that contains the 500 parcellation
#    DATA           - the directory containing the freesurfer extracted values
#                       for each of the three cohorts, demographic data and
#                       input data files for genetic analyses
#    SCRIPTS        - the directory containing all the analysis code 
#                       (except this wrapper)
#    CT_MT_ANALYSES - where all the analysis outputs for this set of analyses
#                       are saved
#==============================================================================
study_dir = os.path.dirname(os.path.abspath(__file__))

sub_data_dir = os.path.join(study_dir, 'FS_SUBJECTS')
fsaverage_dir = os.path.join(sub_data_dir, 'fsaverageSubP')

data_dir = os.path.join(study_dir, 'DATA')

scripts_dir = os.path.join(study_dir, 'SCRIPTS')

paper_dir = os.path.join(study_dir, 'CT_MT_ANALYSES')

matlab_dir = os.path.join('/usr','local','MATLAB','R2012b','bin','matlab')          ##### EDIT HERE FOR YOUR VERSION OF MATLAB!

#==============================================================================
# LOAD THE ANALYSIS CODE MODULES
#==============================================================================
sys.path.append(scripts_dir)
from read_fsaverage_info import *
from make_corr_matrices import *
from fill_measure_dict import *
from make_graphs import *
from call_pls import *
from make_pysurfer_pictures import *
from make_tables import *
from make_figures import *
from make_demo_table import *
from report_stats_tables import *

#==============================================================================
# GET SOME USEFUL INFORMATION FROM FSAVERAGE DIRECTORY
#------------------------------------------------------------------------------
#   Names of each region in the parcellation (aparc_names)
#   Coordinates of the center of mass of these regions (centroids)
#   Pairs of coordiantes for sagital, coronal and axial projections
#   Von economo and lobe labels for each region
#==============================================================================
fsaverage_dict = read_fsaverage_info(fsaverage_dir)


#==============================================================================
# DEFINE THE COVARIATES YOU CARE ABOUT
#------------------------------------------------------------------------------
# While the network analyses in the paper are presented without correction for
# any covariates in order to aid interpretation, it is important to check
# the influence of certain demographic measures on the results.
# Therefor all analyses are repeated with the following combinations of 
# covariates removed before the structural covariance network is created
#    ONES ----------------- only the intercept is removed
#    AGE ------------------ each participant's age at time of scan
#    GENDER --------------- adding an covariate for boys controls for systematic difference
#                           in mean values between genders
#    SITE ----------------- there are three scanner locations in this study
#                           so adding separate intercepts for WBIC and UCL controls 
#                           for systematic differences in the mean values between
#                           scanner locations
#    AGE and GENDER ------- combination of age and male covariates
#    AGE and SITE --------- combination of age, wbic and ucl covariates
#    GENDER and SITE ------ combination of male, wbic and ucl covariates
#    AGE, GENDER and SITE - combination of age, male, wbic and ucl covariates
#==============================================================================
# Define the covars dictionary

'''
covars_dict = { 'ones'            : ['ones'],
                'age'             : ['age'],
                'gender'          : ['male'],
                'site'            : ['wbic', 'ucl'],
                'age_gender'      : ['age', 'male'],
                'age_site'        : ['age', 'wbic', 'ucl'],
                'gender_site'     : ['male', 'wbic', 'ucl'],
                'age_gender_site' : ['age', 'male', 'wbic', 'ucl'] }
'''
covars_dict = { 'ones' : ['ones'] }                                                 ##### EDIT HERE FOR FULL RUNNING!


#==============================================================================
# DEFINE THE COHORTS YOU CARE ABOUT
#------------------------------------------------------------------------------
# We have three cohorts, all of which are evenly balanced with respect
# to age and gender in each of 5 age bins (14-15, 16-17, 18-19, 20-21, 22-24)
#    DISCOVERY - the inital 100 participants who were
#                sequestered to ensure that analyses 
#                were not overfit
#    VALIDATION - the additional 200 participants (197 usable)
#    COMPLETE - all 300 participants as the study was designed (297 usable)
#==============================================================================
cohort_list = [ 'DISCOVERY', 'VALIDATION', 'COMPLETE' ]


#==============================================================================
# CREATE A MEASURE_DICT_DICT THAT WILL CONTAIN ALL THE USEFUL VALUES
#------------------------------------------------------------------------------
# Basically, this is a dictionary of dictionaries that will let us compare
# across cohorts later on. If the file already exists you can read it in and
# then the calculations will not be re-done (this saves you a bunch of time)
#==============================================================================
measure_dict_dict_file = os.path.join(paper_dir, "measure_dict_dict.p")

if os.path.isfile(measure_dict_dict_file):
    measure_dict_dict = pickle.load(open(measure_dict_dict_file, 'rb'))
else:
    measure_dict_dict = {}
    
#measure_dict_dict = {}             ##### UNCOMMENT HERE TO RE-WRITE DICTIONARY

#==============================================================================
# START THE ANALYSIS LOOP FOR EACH COMBINATION OF PARTICIPANTS
# AND COVARIATES
#==============================================================================
for mpm, cohort in it.product(['MT'], cohort_list):
    
    #==========================================================================
    # Define some useful locations
    #--------------------------------------------------------------------------
    # Although these are the directory names used for the analyses you can
    # change these if you'd like. Just makes sure the files in the data_dir
    # are copied over or replaced with your own data
    #==========================================================================
    cohort_dir = os.path.join(paper_dir, cohort)
    
    cohort_data_dir = os.path.join(data_dir, cohort)
    
    pls_dir = os.path.join(cohort_dir, 'PLS')
    pysurfer_dir = os.path.join(cohort_dir, 'PYSURFER_IMAGES')
    figures_dir = os.path.join(cohort_dir, 'FIGS')
    corrmat_dir = os.path.join(cohort_dir, 'CORR_MATS')
    graph_dir = os.path.join(cohort_dir, 'GRAPHS')
    tables_dir = os.path.join(cohort_dir, 'TABLES')
    
    for d in [ pls_dir, pysurfer_dir, figures_dir, corrmat_dir, graph_dir, tables_dir ]:
        if not os.path.isdir(d):
            os.makedirs(d)
    
    #==========================================================================
    # Print the cohort name to screen so you know where you're up to
    #==========================================================================
    print 'COHORT: {}'.format(cohort)

    #==========================================================================
    # The CT data file is important for a lot of analyses so we're going
    # to set explicitly here
    #==========================================================================
    ct_data_file = os.path.join(cohort_data_dir, 'PARC_500aparc_thickness_behavmerge.csv')
    
    
    #==========================================================================
    # Make the correlation matrices
    #--------------------------------------------------------------------------
    # These files can take a little while to make, so they've already been
    # created. If you'd like to re-make them you can either delete the files
    # that are already there, or re-name the corrmat_dir (above)
    #
    # The matrices are saved in dictionary (mat_dict) for future use within 
    # this wrapper code
    #==========================================================================
    mat_dict = make_corr_matrices(corrmat_dir, 
                                    covars_dict, 
                                    ct_data_file, 
                                    fsaverage_dict['aparc_names'])


    #==========================================================================
    # Save a bunch of useful measures
    #--------------------------------------------------------------------------
    # So that you can easily access the output of a bunch of different analyses
    # from a bunch of different files (such as the different MPM depths) we're
    # going to save them all to a dictionary that can easily be passed to 
    # the reporting functions such as those that make figures and tables.
    # It takes a bit of time to calculate all these values, so if the dictionary
    # already exists we'll just read it in, and not bother making a new one,
    # otherwise we'll create an empty one and fill it up.
    #--------------------------------------------------------------------------
    # This is the part of the code that is doing all the statistical
    # tests! So it's kind of a big deal! 
    # There are too many measures to outline here, but please see the 
    # documentation for the fill_measure_dict function for all the details
    #==========================================================================
    measure_dict = measure_dict_dict.get('{}_{}'.format(cohort, mpm), {})
    
    measure_dict = fill_measure_dict_part1(measure_dict,
                                                mpm, 
                                                cohort_data_dir, 
                                                fsaverage_dict, 
                                                n_perm=1000)


    #==========================================================================
    # Save the measure dictionary in a dictionary of dictionaries
    #--------------------------------------------------------------------------
    # This is so you can compare different cohorts and different MPM measures
    # later on, and also so you don't have to re-calculate all the stats over
    # and over again :)
    #==========================================================================
    measure_dict_dict['{}_{}'.format(cohort, mpm)] = measure_dict
    
    pickle.dump(measure_dict_dict, open(measure_dict_dict_file, "wb" ) )
    
    
    #==========================================================================
    # Run PLS
    #--------------------------------------------------------------------------
    # The PLS code is written in matlab so we need to call those commands
    #==========================================================================
    measure_dict = pls_commands(measure_dict,
                                    mpm,
                                    pls_dir,
                                    scripts_dir,
                                    matlab_dir,
                                    data_dir)
    
    
    #==========================================================================
    # Make the graphs
    #--------------------------------------------------------------------------
    # These files can take a little while to make, so they've already been
    # created. If you'd like to re-make them you can either delete the files
    # that are already there, or re-name the graph_dir (above)
    #
    # The graphs and nodal and global measures are saved in dictionary 
    # (graph_dict) for future use within this wrapper code
    #
    # n is the number of random graphs to create for comparison to the actual
    # graph
    #==========================================================================
    graph_dict = make_graphs(graph_dir,
                                mat_dict, 
                                fsaverage_dict['centroids'],
                                fsaverage_dict['aparc_names'],
                                n_rand=1000)
    
    
    #==========================================================================
    # Save a bunch of useful measures (part 2)
    #==========================================================================
    measure_dict = fill_measure_dict_part2(measure_dict,
                                                graph_dict, 
                                                n_perm=1000)
    
    
    #==========================================================================
    # Save the measure dictionary in a dictionary of dictionaries (again)
    #==========================================================================
    measure_dict_dict['{}_{}'.format(cohort, mpm)] = measure_dict
    
    pickle.dump(measure_dict_dict, open(measure_dict_dict_file, "wb" ) )
    
    
    #==========================================================================
    # Make the tables
    #--------------------------------------------------------------------------
    # These tables summarise the regional measures and are sorted by dMT
    #==========================================================================
    make_tables(measure_dict, tables_dir, cohort_name=cohort.title())
    
    
    #==========================================================================
    # Make the figures
    #--------------------------------------------------------------------------
    # We've done the statistics so now we're going to make some pretty pictures
    #==========================================================================
    make_pysurfer_figures(measure_dict, 
                            pysurfer_dir, 
                            sub_data_dir, 
                            scripts_dir, 
                            paper_dir,
                            overwrite=False)
    
    make_figures(measure_dict, figures_dir, pysurfer_dir, data_dir, graph_dict)
    

#==========================================================================
# Youre done with the cohorts separately!
#--------------------------------------------------------------------------
# Now just make the summary stats tables and combined figures and relax :)
#==========================================================================
make_demo_table(data_dir, paper_dir)
make_stats_tables(measure_dict_dict, paper_dir)

make_combo_figures(measure_dict_dict, paper_dir)

#==========================================================================
# Aaaaaaand.....you're done!! Thanks for playing along :)
# Kx
#==========================================================================
