#!/bin/bash

datapath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dijet
higgspath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dihiggs
ditoppath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/ditop
wzpath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/wz

python reweight_higgs.py $higgspath/user.dguest.301488.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301489.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301490.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301492.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301493.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301494.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301496.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301497.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301498.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301499.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301500.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301501.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301502.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301504.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301505.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301507.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301322.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301323.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301324.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301325.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301326.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301327.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301328.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301332.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301333.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301334.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $ditoppath/user.dguest.301335.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301254.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301255.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301256.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301257.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301258.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301259.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301260.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301261.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301262.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301263.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301264.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301265.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301266.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301267.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301268.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301269.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301270.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301271.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301272.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301273.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301274.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301275.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301276.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301277.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301279.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301280.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301282.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301283.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301284.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301285.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301286.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $wzpath/user.dguest.301287.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  -o images/ \

