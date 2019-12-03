#!/usr/bin/python
# -*- coding: utf8 -*-

import boto3
import urllib

S3_ENDPOINT='https://s3.cn-north-1.amazonaws.com.cn'

BUCKET_NAME='reinvent'
PREFIX='2019/'
INDEX_FILE='index_2019.html.td'

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
    Custom  caterory
    AWS re -Invent 2019 Breakout Sessions _ GPS-Technical/1 - AWS re -Invent 2019 - Networking, Storage, Data Protection Deep Dive w_ VMware Cloud on AWS GPSTEC307.mp4
    AWS re -Invent 2019 _ Launch Announcements/1 - AWS re -Invent 2019 - Announcing Amazon SageMaker Neo.mp4
    '''
    info = {}

    sections = key.split('/')
    #print("key=[len{}={}]".format(len(sections), key))

    if len(sections) < 3:
        return info

    if sections[1] in ['reInvent_playlist']:
        return {}

    # Keynote tags
    if 'AWS re -Invent 2019 Keynote' in key:
        info['category'] = 'Keynotes' 
    elif 'Peter DeSantis' in key:
        info['category'] = 'Keynotes' 
    elif 'Invent 2019 Launchpad Live Streams' in key:
        info['category'] = 'Launchpad Live Streams' 
    else:
        info['category'] = sections[1].split('_')[-1]

    info['name'] = sections[2]
    info['ext'] = sections[2].split('.')[-1]

    return info

def get_link(bucket_name, key_name):
    '''
    # https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2015/Architecture/AWS+re_Invent+2015+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4
    '''
    print key_name

    #return "{S3Endpoint}/{Bucket}/{Key}".format(S3Endpoint=S3_ENDPOINT, Bucket=bucket_name, Key=urllib.quote_plus(str(unicode(key_name))))
    return "{S3Endpoint}/{Bucket}/{Key}".format(S3Endpoint=S3_ENDPOINT, Bucket=bucket_name, Key=urllib.quote_plus(str(key_name)))

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
            #print(obj_info)
    
            if 'category' in obj_info and 'name' in obj_info and 'ext' in obj_info:
                if obj_info['ext'] != 'mp4':
                    continue
                print obj_info['category']+':'+obj
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
    # change_objects_permission(BUCKET_NAME, obj_list)
