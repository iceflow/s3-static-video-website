#!/usr/bin/python
# -*- coding: utf8 -*-

import boto3
import urllib
import re
from pprint import *

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

    const_category_map = {
        'NET': 'Networking'
    }

    info = {
        'key': key,
        'category': '',
        'name': '',
        'ext': '',
        'breakout_session_name': ''
    }

    sections = key.split('/')
    #print("key=[len{}={}]".format(len(sections), key))

    if len(sections) < 3:
        return info

    if sections[1] in ['reInvent_playlist']:
        return {}



    # Keynote tags
    #if 'AWS re -Invent 2019 Keynote' in key:
    if 'keynote' in key.lower():
        info['category'] = '0-Keynotes' 
    elif 'Peter DeSantis' in key:
        info['category'] = '0-Keynotes' 
    elif 'Invent 2019 Launchpad Live Streams' in key:
        info['category'] = 'Launchpad Live Streams' 
    else:
        info['category'] = sections[1].split('_')[-1]

    info['name'] = sections[2]
    info['ext'] = sections[2].split('.')[-1]

    info['breakout_session_name'] = info['name']

    # "AWS re -Invent 2019 - [REPEAT 2] AWS networking fundamentals (NET201-R2).mp4"
    # Find breakout session category
    names = re.findall('.*\((.*)\).*', info['name'])
    if len(names) > 0:
        b_name = names[0]
        info['breakout_session_name'] = b_name
        item = re.findall('^(\D+)(.*)', b_name)
        if len(item) > 0:
            info['category'] = item[0][0]
        

    return info

def get_link(bucket_name, key_name):
    '''
    # https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2015/Architecture/AWS+re_Invent+2015+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4
    '''
    #print key_name

    #return "{S3Endpoint}/{Bucket}/{Key}".format(S3Endpoint=S3_ENDPOINT, Bucket=bucket_name, Key=urllib.quote_plus(str(unicode(key_name))))
    return "{S3Endpoint}/{Bucket}/{Key}".format(S3Endpoint=S3_ENDPOINT, Bucket=bucket_name, Key=urllib.quote_plus(str(key_name)))

def make_up_file_list(obj_list):
    '''
        deduplicated, sort needed
        return: category_key_list(list), file_list(dict)
    '''

    category_list_map = {}
    file_list_map = {}

    for obj in obj_list:
        obj_info = get_obj_info(obj)
        if 'category' not in obj_info or 'name' not in obj_info or 'ext' not in obj_info or 'breakout_session_name' not in obj_info:
            continue

        if obj_info['ext'] != 'mp4':
            continue

        pprint(obj_info)

        category = obj_info['category']
        b_name = obj_info['breakout_session_name']

        ## session 
        if category not in file_list_map:
            file_list_map[category] = {}

        file_list_map[category][b_name] = obj_info

    category_key_list = sorted(file_list_map.keys())

    pprint(category_key_list)

    return category_key_list, file_list_map

def make_up_index_file(bucket_name, category_list, file_list_map):
    '''
    # http://leopublic.s3-website.cn-north-1.amazonaws.com.cn
    # https://s3.cn-north-1.amazonaws.com.cn/leopublic/reInvent2015/Architecture/AWS+re_Invent+2015+_+(ARC302)+Running+Lean+Architectures_+Optimizing+for+Cost+Efficiency+-+YouTube+%5B720p%5D.mp4
    '''
    
    FORMAT="<tr>\n<td>{Pos}</td>\n<td>{Category}</td>\n<td><A href='{Link}' target='_blank'>{Name}</A></td>\n</tr>\n"


    with open(INDEX_FILE, 'w') as f:
        pos=1
        for category in category_list:
            if category not in file_list_map:
                print('{} not in file_list_map'.format(category))
                continue

            for k,v in file_list_map[category].items():
                if 'category' in v and 'name' in v and 'ext' in v:
                    #print('category[{}] / name[{}] / ext[{}]'.format(v['category'], v['name'], v['ext']))
                    print(v)
                    f.write(FORMAT.format(Pos=pos, Category=v['category'], Link=get_link(bucket_name, v['key']), Name=v['name']))
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
#    for item in obj_list:
#        print(item)

    # 2. make up file list ( de-duplicated, sort )
    category_list, file_list_map = make_up_file_list(obj_list)

    #pprint(file_list_map)
    #pprint(file_list_map['0-Keynotes'])

    # 2. make up index.html
    make_up_index_file(BUCKET_NAME, category_list, file_list_map)

    # 3. Changed related objects permission to public read
    # change_objects_permission(BUCKET_NAME, obj_list)
