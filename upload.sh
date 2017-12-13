#!/bin/bash

echo "Start Time:`date`"

pushd /data/s3-static-video-website

./upload_chinakb_2015.sh
./upload_chinakb_2016.sh
./upload_chinakb_2017.sh


popd

echo "End Time:`date`"

exit 0
