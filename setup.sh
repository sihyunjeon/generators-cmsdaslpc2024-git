#!/usr/bin/env bash
export GENTUTPATH=${HOME}/nobackup/GENTUTORIAL
export GENMGPATH=${GENTUTPATH}/standalone-tut/MG5_aMC_v2_9_18
export GENGRIDPACKPATH=${GENTUTPATH}/gridpack-tut/genproductions
export GENSHOWERPATH=${GENTUTPATH}/shower-tut
export GENPLOTPATH=${HOME}/GENTUTORIAL/plotter-tut
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${GENTUTPATH}/CMSSW_12_4_14_patch2/src
cmsenv
cd ${GENTUTPATH}

