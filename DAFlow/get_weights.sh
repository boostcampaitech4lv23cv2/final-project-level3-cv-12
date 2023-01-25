#!/bin/sh

echo Download weights !
cd utils
wget https://www.dropbox.com/s/o2mqtdd32ttxk0d/daflow_weights.zip

echo Unzip weights !
unzip daflow_weights.zip
rm -r daflow_weights.zip

cd ../../
echo Done !