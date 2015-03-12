"""
Create a AIM user and grant S3 policy.

Create a bucket and a bucket policy using the following JSON.
Replace bucket in Resouece with your bucket name.
{
  "Version": "2008-10-17",
  "Statement": [{
    "Sid": "AllowPublicRead",
    "Effect": "Allow",
    "Principal": { "AWS": "*" },
    "Action": ["s3:GetObject"],
    "Resource": ["arn:aws:s3:::bucket/*" ]
  }]
}
"""

from __future__ import print_function
import os
import boto
from boto.s3.key import Key
import click


def get_bucket(bucket_name, aws_access_key_id, aws_secret_access_key):
    conn = boto.connect_s3(aws_access_key_id, aws_secret_access_key)
    bucket = conn.get_bucket(bucket_name)
    bucket_location = bucket.get_location()

    # Issue workaround
    # https://github.com/boto/boto/issues/2207
    if bucket_location:
        conn = boto.s3.connect_to_region(
            region_name=bucket_location,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)
        bucket = conn.get_bucket(bucket_name)

    return bucket


def upload(bucket, path, root=None, prefix='', versioned=False):
    if root is None:
        root = path
    if versioned:
        prefix = os.path.join(prefix, '0.1')
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fn = os.path.join(dirpath, filename)
            k = Key(bucket)
            k.key = os.path.join(prefix, os.path.relpath(fn, root))
            print('Uploading', k.key, '...')
            k.set_contents_from_filename(fn)


@click.command()
@click.argument('bucket_name')
@click.argument('path')
@click.argument('prefix')
@click.pass_context
def run(ctx, bucket_name, path, prefix):
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    if aws_access_key_id is None:
        click.echo('Cound not get AWS_ACCESS_KEY_ID from environment')
        ctx.exit(1)

    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if aws_secret_access_key is None:
        click.echo('cound not get AWS_SECRET_ACCESS_KEY from environment.')
        ctx.exit(1)

    bucket = get_bucket(bucket_name, aws_access_key_id, aws_secret_access_key)
    upload(bucket, path, root=path, prefix=prefix)
