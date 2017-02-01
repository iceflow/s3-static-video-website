# 简介

由于S3支持H.264，AAC格式自动stream, 特别适合点播，只要网速正常，可以随时在线查看。免去下载。

  1. 启用bucket webhosting
  2. 自动生成index.html页面
  3. bootstrap web模版

# 文件说明
css/ fonts/ js/
  - 静态html文件包含的目录
  
make_index*.py: 重点参考最新 make_index_chinakb_2016.py
  1. 使用python boto3
  2. 使用 aws configure 配置credential
  3. 遍历选定Bucket下的对象, 带过滤
  4. 生成下载文件列表 html-<tr>部分
  5. 遍历对象，增加 public read 权限
  
upload*.sh： 重点参考最新 upload_chinakb_2016.sh 
  1. 运行 make_index*.py
  2. 合并生成index*.html
  3. 上传到目标bucket
 
 
reinvent_bucket_policy.json: Bucket策略
   - {AccountID}, {User}, {BucketName} 替换为实际内容
```Bash
{
        "Version": "2012-10-17",
        "Statement": [
                {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": {
                                "AWS": [
                                        "arn:aws-cn:iam::{AccountID}:user/{User}",
                                        "arn:aws-cn:iam::{AccountID}:user/{User}"
                                ]
                        },
                        "Action": "s3:*",
                        "Resource": [
                                "arn:aws-cn:s3:::{BucketName}",
                                "arn:aws-cn:s3:::{BucketName}/*"
                        ]
                },
                {
                        "Sid": "",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                                "s3:Get*",
                                "s3:List*"
                        ],
                        "Resource": [
                                "arn:aws-cn:s3:::{BucketName}/2015/*",
                                "arn:aws-cn:s3:::{BucketName}/2016/*"
                        ]
                }
        ]
}
```

# 配置修改:
  - 修改python默认字符为utf-8：不然很容易出现转码错误
    - 已 python2.7 为例，修改 /usr/lib64/python2.7/site.py
    ```Bash
    def setencoding():
    """Set the string encoding used by the Unicode implementation.  The
    default is 'ascii', but if you're willing to experiment, you can
    change this."""
    encoding = "utf-8" # Default value set by _PyUnicode_Init()
    ```
  - ./upload*.sh  # 遍历目标Bucket内容，生成 index*.html文件，上传到目标bucket
  - 修改: make_index*.py 中的
    - BUCKET_NAME='xxxx'
    - PREFIX='reInvent2015/'
    - INDEX_FILE='index_2015.html.td'
  - 修改：def get_obj_info(key): 部分，根据具体的bucket内视频文件目录结构
 

  
# 使用流程
  - 周期或者触发上传新的视频内容到S3, 例如海外检测youtube频道内容，新增后上传
  - 中国本地，周期或者触发运行 ./upload_chinakb_2016.sh
  - 查看新页面
  
## [站点Sample](http://reinvent.s3-website.cn-north-1.amazonaws.com.cn)
![站点Sample](https://s3.cn-north-1.amazonaws.com.cn/reinvent/docs/s3-directory-sample.png)

## S3静态站点配置
![S3静态站点配置](https://s3.cn-north-1.amazonaws.com.cn/reinvent/docs/s3-static-website.png)

## S3 Bucket目录结构
![S3 Bucket目录结构](https://s3.cn-north-1.amazonaws.com.cn/reinvent/docs/website.png)

# 参考
Boto3
  - 源码:        https://github.com/boto/boto3
  - 快速入门:    https://boto3.readthedocs.org/en/latest/guide/quickstart.html
  - API参考:     https://boto3.readthedocs.org/en/latest/reference/services/index.html
  
# TODO
  - 配置文件独立
  - 触发生成页面: 国内 S3 notification -> SNS -> EC2 Group ; 海外 S3 notification -> Lambda
  - 当文件数量巨大的时候，不适合再遍历bucket内容。需要使用DynamoDB纪录metadata，并生成索引文件(html or js)
  - 已经启用bucket日志功能，分析accesslog
  - WebSite 功能点
    - 用户手工标注: 已观看、未观看、计划观看
    - 用户手工评价: 1-5星
    - ....
