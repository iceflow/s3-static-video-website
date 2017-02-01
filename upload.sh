#!/bin/bash

# http://leopublic.s3-website.cn-north-1.amazonaws.com.cn
# https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2015/Architecture/AWS+re_Invent+2015+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4

D=leopublic

#[ -f index.html ] && rm -f index.html


./make_index.py

cp index.html.head index.html
cat index.html.td >> index.html
cat index.html.tail >> index.html

[ -f index.html ] && aws s3 cp index.html s3://$D

aws s3api put-object-acl --bucket leopublic --key index.html --grant-read 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'
