#!/bin/bash

#bf-p4c --arch tna -I $SDE/install/share/p4c/p4_14include -I $SDE/install/share/p4c/p4include -I $SDE/pkgsrc/p4-examples/p4_16_programs haha.p4 -o out

bf-p4c -I $SDE/install/share/p4c/p4_14include -I $SDE/install/share/p4c/p4include -I $SDE/pkgsrc/p4-examples/p4_16_programs haha.p4 -o out
