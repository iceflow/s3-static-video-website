#!/bin/bash

aws --profile chinakb s3 sync s3://leopublic/reInvent2015/ s3://reinvent/2015/ 
#aws --profile chinakb s3 cp s3://leopublic/reInvent2015/ s3://reinvent/2015/ --recursive

DIRS="css js fonts"
for D in $DIRS; do
	aws --profile chinakb s3 cp  bootstrap-3.3.5-dist/$D s3://reinvent/$D --recursive
done
