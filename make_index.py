#!/usr/bin/python
# -*- coding: utf8 -*-

import boto3
import urllib

S3_ENDPOINT='https://s3.cn-north-1.amazonaws.com.cn'

BUCKET_NAME='leopublic'
PREFIX='reInvent2015/'
INDEX_FILE='index.html.td'

def get_obj_list(bucket_name, prefix):

	obj_list = []

	if bucket_name == '':
		return obj_list

	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket_name)

	if prefix == '':
		objects = bucket.objects.all()
	else:
		objects = bucket.objects.filter(Prefix=prefix)
	
	for obj in objects:
		obj_list.append(obj.key)

	return obj_list

def get_obj_info(key):
	''' 
	reInvent2015/storage & Content Delivery/AWS re_Invent 2015 _ (STG406) Using S3 to Build and Scale an Unlimited Storage Service - YouTube [720p].mp4
	'''
	info = {}

	sections = key.split('/')

	if len(sections) < 3:
		return info

	info['category'] = sections[1]
	info['name'] = sections[2]

	return info
	

def get_link(bucket_name, key_name):
	'''
	# https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2015/Architecture/AWS+re_Invent+2015+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4
	'''
	print key_name

	return "{S3Endpoint}/{Bucket}/{Key}".format(S3Endpoint=S3_ENDPOINT, Bucket=bucket_name, Key=urllib.quote_plus(unicode(key_name)))

def make_up_index_file(bucket_name, obj_list):
	'''
	# http://leopublic.s3-website.cn-north-1.amazonaws.com.cn
	# https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2015/Architecture/AWS+re_Invent+2015+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4
	'''
	
	FORMAT="<tr>\n<td>{Pos}</td>\n<td>{Category}</td>\n<td><A href='{Link}' target='_blank'>{Name}</A></td>\n</tr>\n"


	with open(INDEX_FILE, 'w') as f:
		pos=1
		for obj in obj_list:
			obj_info = get_obj_info(obj)
	
			if 'category' in obj_info and 'name' in obj_info:
				f.write(FORMAT.format(Pos=pos, Category=obj_info['category'], Link=get_link(bucket_name, obj), Name=obj_info['name']))
				pos=pos+1

	return 0
	

def change_objects_permission(bucket_name, obj_list):
	s3 = boto3.resource('s3')

	for key in obj_list:
		object_acl = s3.ObjectAcl(bucket_name, key)

		object_acl.put(ACL='public-read')


	return 0

if __name__ == '__main__':
	# 1. Get bucket related objects list
	obj_list = get_obj_list(BUCKET_NAME, PREFIX)

	# 2. make up index.html
	make_up_index_file(BUCKET_NAME, obj_list)

	# 3. Changed related objects permission to public read
	change_objects_permission(BUCKET_NAME, obj_list)
