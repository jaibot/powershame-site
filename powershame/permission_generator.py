#!/usr/bin/env python

from powershame import app
from boto import sts

def get_temp_upload_creds( prefix, lifetime=None ):
    """Get creds to temporarily upload to s3 PIC with prefix

    The resulting credentials object will have an access_key, secret_key, and
    session_token which can be safely passed to an end-user to grant temporary
    upload rights limited by prefix. Creds expire after lifetime seconds
    """
    sts_conn = sts.STSConnection(   
        aws_access_key_id = app.config['ISSUER_KEY'],
        aws_secret_access_key = app.config['ISSUER_SECRET'] )
    # in addition to the policy inherited by UPLOADER_ROLE, we also need
    #   to create a policy that limits by prefix (so users can't upload into
    #   directories other than their own)
    temp_policy = generate_policy_string( prefix )
    if not lifetime:
        lifetime=app.config['UPLOAD_CREDS_LIFETIME']
    assumed_role = sts_conn.assume_role( 
        app.config['UPLOADER_ROLE_ARN'],
        'temp_upload_creds', 
        policy=temp_policy, 
        duration_seconds=lifetime )
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
            "arn:aws:s3:::%(bucket)s/%(prefix)s*"
          ],
          "Effect": "Allow"
        }
      ]
    }""" % { 'bucket': app.config['PIC_BUCKET'], 'prefix': prefix }
    return policy_string
