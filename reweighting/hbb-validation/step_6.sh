#!/bin/bash

#python make_jet_pt_hist.py -d data/my_denominator.json -x data/xsec.txt -o images/

datapath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dijet
higgspath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/dihiggs
ditoppath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/ditop
wzpath=/baldig/physicsprojects/atlas/hbb/raw_data/v_6/wz

#python make_jet_pt_hist.py $datapath/user.dguest.361020.hbbTraining.p1_output.h5 \
#                                  $datapath/user.dguest.361021.hbbTraining.p1_output.h5 \
#                                  $datapath/user.dguest.361022.hbbTraining.p1_output.h5 \
python plot_from_calculated_weights.py $datapath/user.dguest.361020.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361021.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361022.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361024.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361025.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361027.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361028.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361029.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $datapath/user.dguest.361031.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
                                  $higgspath/user.dguest.301488.hbbTraining.2018_05_02_T140344_R3342_output.h5 \
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
                                  $wzpath/user.dguest.301323.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301325.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301326.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301328.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301330.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301331.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301332.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301333.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301335.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301489.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301490.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301491.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301492.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301493.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301494.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301497.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301498.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301499.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301501.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301502.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301505.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.301507.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361021.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361024.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361025.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361026.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361028.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361030.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  $wzpath/user.dguest.361031.hbbTraining.2018_04_05_T114349_R31321_output.h5 \
                                  -d data/my_denominator.json -x data/xsec.txt -o images/ \

