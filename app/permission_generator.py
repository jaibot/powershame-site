#!/usr/bin/env python

#from app import app
from boto import sts

from private_config import ISSUER_KEY, ISSUER_SECRET, UPLOAD_BUCKET, UPLOADER_ROLE_ARN
#ISSUER_KEY=app.config['ISSUER_KEY']
#ISSUER_SECRET=app.config['ISSUER_SECRET']
#UPLOAD_BUCKET=app.config['UPLOAD_BUCKET']
#UPLOADER_ROLE_ARN=app.config['UPLOADER_ROLE_ARN']

def get_temp_upload_creds( prefix ):
    """Get creds to temporarily upload to s3 UPLOAD_BUCKET with prefix

    The resulting credentials object will have an access_key, secret_key, and
    session_token which can be safely passed to an end-user to grant temporary
    upload rights limited by prefix. Creds expire after 60 minutes.
    """
    sts_conn = sts.STSConnection(   aws_access_key_id = ISSUER_KEY,
                                    aws_secret_access_key = ISSUER_SECRET )
    # in addition to the policy inherited by UPLOADER_ROLE, we also need
    #   to create a policy that limits by prefix (so users can't upload into
    #   directories other than their own)
    temp_policy = generate_policy_string( prefix )
    assumed_role = sts_conn.assume_role(    UPLOADER_ROLE_ARN, 
                                        'temp_upload_creds', 
                                        policy=temp_policy, 
                                        duration_seconds=3600 )
    return assumed_role.credentials

def generate_policy_string( prefix ):
    """Get AWS policy string for put-only access to UPLOAD_BUCKET with prefix

    WARNING: The prefix argument is a raw string that gets directly dropped
    into an AWS policy! Therefore, THIS FUNCTION SHOULD
    ONLY EVER BE CALLED FROM TRUSTED CODE, AND THE PREFIX SHOULD BE
    CLEAN, OR BAD THINGS COULD HAPPEN. DOOMY DOOMY DOOM
    """
    policy_string = \
    """{                                                                           
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": [
            "s3:PutObject"
          ],
          "Sid": "Stmt1373903371000",
          "Resource": [
            "arn:aws:s3:::%(bucket)s/%(prefix)s/*"
          ],
          "Effect": "Allow"
        }
      ]
    }""" % { 'bucket': UPLOAD_BUCKET, 'prefix': prefix }
    return policy_string

if __name__ == '__main__':
    my_prefix='winning'
    creds = get_temp_upload_creds( my_prefix )
    from boto.s3.connection import S3Connection
    s3_conn = S3Connection( creds.access_key, creds.secret_key, security_token=creds.session_token )
    bucket = s3_conn.lookup(UPLOAD_BUCKET, validate=False)
    key = bucket.new_key(my_prefix + '/testing')
    key.set_contents_from_filename('/tmp/facts.txt')
