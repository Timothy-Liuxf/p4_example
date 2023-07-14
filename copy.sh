#!/usr/bin/env bash

cp ./out/haha.conf $SDE/install/share/p4/targets/tofino/
rm -rf $SDE/install/out
cp -r ./out/ $SDE/install/
rm -rf $SDE/install/share/tofinopd/haha
cp -r ./out $SDE/install/share/tofinopd/haha
