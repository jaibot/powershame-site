import subprocess
import os
import time
import logging
from datetime import datetime, timedelta
from boto.exception import S3PermissionsError, AWSConnectionError, S3ResponseError
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from app import app

class SessionRenderer( object ):
    def __init__( self, access_key, secret_key, shots_bucket, video_bucket, working_dir ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.set_s3_conn()
        self.shots_bucket = shots_bucket
        self.video_bucket = video_bucket
        self.working_dir = working_dir

    def set_s3_conn( self ):
        self.s3_conn =  S3Connection(   self.access_key, 
                                        self.secret_key )
    def render( self, session_id, screenshots ):
        working_path = os.path.join( self.working_dir, 'powershame-rendering', str(session_id) )
        shots_path = os.path.join( working_path, 'shots' )
        video_path=os.path.join( working_path, 'session.mkv' )
        try:
            os.makedirs( shots_path )
        except OSError:
            pass
        self.download_shots( shots_path, screenshots )
        self.make_video( shots_path, video_path )
        return self.upload_video( video_path, str(session_id)+'.mkv' )

    def download_shots( self, working_path, screenshots ):
        for i,s in enumerate(screenshots):
            logging.debug( str(s) )
            logging.debug( str(i) )
            bucket = self.s3_conn.get_bucket( s['bucket'] )
            key = bucket.get_key( s['key'] )
            filename = '%04d.png'%i
            key.get_contents_to_filename( os.path.join( working_path, filename ) )

    def make_video( self, shots_path, video_filename ):
        num_shots = len( os.listdir( shots_path ) )
        movie_maker = ffmpeg_str( shots_path, video_filename, num_shots )
        p = subprocess.call( movie_maker )

    def upload_video( self, video_path, key_path ):
        bucket = self.s3_conn.get_bucket( self.video_bucket, validate=False )
        key = Key(bucket)
        key.key = key_path
        key.set_contents_from_filename( video_path, headers={'Content-Type':'video/mp4'} )
        lifetime = int( app.config['VID_URL_LIFETIME'] )
        expiration = datetime.now() + timedelta(seconds=lifetime)
        url = self.s3_conn.generate_url( lifetime, 'GET', bucket=self.video_bucket, key=key_path) 
        return url, expiration

def ffmpeg_str( dir, outfile, num_shots ):
    """compose string for rendering call"""
    #explanation of arguments to ffmpeg:
    #    -y: overwrite output file
    #    -f image2: input type
    #    -r 1: framerate (1/s=s seconds per frame)
    #    -i %s/%%04d.png: input is all files like dir/0001.png
    #    -vcodec libvpx: x264 codec
    #   -f mp4: output container (needed for iOS)
    # TODO: calculate resolution based off original resolution
    # TODO: alter framerate to speed up longer videos
    # TODO: time OSD and/or titlecards
    logging.debug('num_shots: %d'%num_shots)
    vid_length = min( app.config['MAX_VID_TIME'], num_shots*app.config['SECONDS_PER_FRAME'] )
    logging.debug('vid length: %f'%vid_length)
    seconds_per_frame = float(vid_length)/float(num_shots)
    logging.debug('seconds/frame: %f'%seconds_per_frame)
    framerate = 1.0/seconds_per_frame
    base= "ffmpeg -y -f image2 -r %f -i %s/%%04d.png -vcodec libx264 -s 800x450 -f mp4 %s" % (framerate, dir, outfile )
    return base.split(' ')

if __name__=='__main__':
    renderer = SessionRenderer( access_id, secret, pic_bucket_name, vid_bucket_name, '/tmp/' )
