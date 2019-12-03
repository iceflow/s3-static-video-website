#!/bin/bash

D=reinvent
PROFILE=chinakb
F=$1

echo "Start Time:`date`"

pushd /data/s3-static-video-website

#./upload_chinakb_2015.sh
#./upload_chinakb_2016.sh
#./upload_chinakb_2017.sh
#./upload_chinakb_2018.sh
./upload_chinakb_2019.sh


if [ "_$F" != "_" ]; then
	cp index_2019.html index.html
	for H in *.html; do
		if [ -f $H ]; then
			aws --profile $PROFILE s3 cp $H s3://$D
			aws --profile $PROFILE s3api put-object-acl --bucket $D --key $H --grant-read 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'
		fi
	done
fi


popd

echo "End Time:`date`"

exit 0
