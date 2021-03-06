#!/bin/bash

# http://leopublic.s3-website.cn-north-1.amazonaws.com.cn
# https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2019/Architecture/AWS+re_Invent+2019+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4

D=reinvent
TD=index_2019.html.td
INDEX=index_2019.html
PROFILE=chinakb
Y=2019

F="$1"

# Need to modify to your working directory
cd /data/s3-static-video-website


# Check whether to refresh
if [ "_$F" = "_" ]; then
	aws --profile $PROFILE s3 ls s3://$D/$Y/LIST.CHANGED > /dev/null 2>&1

	if [ $? -ne 0 ]; then
		echo "Nothing changed. Quit"
		exit 0
	fi
fi

./make_index_chinakb_2019.py

N=`grep -c 'A href' ${TD}`

cp index.html.head $INDEX

echo "Last update time: `date '+%Y/%m/%d %T'`  Total Video Number: $N" >> $INDEX

cat index.html.head.part2 >> $INDEX

cat ${TD} >> $INDEX

cat index.html.tail >> $INDEX

[ -f $INDEX ] && aws --profile $PROFILE s3 cp $INDEX s3://$D
# Default
[ -f $INDEX ] && aws --profile $PROFILE s3 cp $INDEX s3://$D/index.html

PUBLIC_KEYS="$INDEX index.html js/bootstrap.js js/bootstrap.min.js js/npm.js fonts/glyphicons-halflings-regular.eot fonts/glyphicons-halflings-regular.svg fonts/glyphicons-halflings-regular.ttf fonts/glyphicons-halflings-regular.woff fonts/glyphicons-halflings-regular.woff2 css/bootstrap-theme.css css/bootstrap-theme.css.map css/bootstrap-theme.min.css css/bootstrap.css css/bootstrap.css.map css/bootstrap.min.css"

for KEY in ${PUBLIC_KEYS}; do
	aws --profile $PROFILE s3api put-object-acl --bucket $D --key $KEY --grant-read 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'
done

# Delete tag
aws --profile $PROFILE s3 rm s3://$D/$Y/LIST.CHANGED

exit 0
