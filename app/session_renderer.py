#From app import aws creds
from multiprocessing import Process
import subprocess
import os
from boto.exception import S3PermissionsError, AWSConnectionError, S3ResponseError
from boto.s3.connection import S3Connection
from boto.s3.key import Key

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
    def run( self, queue ):
        while True:
            session = queue.get()
            self.handle( session )
    def handle( self, session ):
        user = session.user
        prefix = session.prefix
        p = Process( target = self.render, args = (user, prefix) )
        p.start()
    def render( self, username, prefix ):
        working_path = os.path.join( self.working_dir, 'powershame-rendering', username, prefix )
        video_path=os.path.join( working_path, prefix+'.mkv' )
        try:
            os.makedirs( working_path )
        except OSError:
            pass
        self.download_shots( working_path, username, prefix )
        self.make_video( working_path, video_path )
        self.upload_video( video_path, username, prefix )
    def download_shots( self, working_path, username, prefix ):
        bucket = self.s3_conn.get_bucket( self.shots_bucket )
        shot_keys_to_download = filter( is_shot, bucket.list( prefix=username+'/'+prefix) )
        shot_keys_to_download.sort( key = lambda shot_key: shot_key.name )
        for i,shot in enumerate(shot_keys_to_download):
            print shot.name
            filename = '%04d.png'%i
            shot.get_contents_to_filename( os.path.join( working_path, filename ) ) #TODO: Error handling
    def make_video( self, working_path, video_filename ):
        movie_maker = ffmpeg_str( working_path, video_filename )
        p = subprocess.call( movie_maker )
    def upload_video( self, video_path, username, prefix ):
        bucket = self.s3_conn.get_bucket( self.video_bucket, validate=False )
        key = Key(bucket)
        key.key=username+'/'+prefix+'.mkv'
        key.set_contents_from_filename( video_path )

# below: utility functions

def is_shot( key ):
    print 'isshot'
    return key.name.endswith('.png')

def ffmpeg_str( dir, outfile ):
    """compose string for rendering call"""
    #explanation of arguments to ffmpeg:
    #    -y: overwrite output file (not an issue in the current version, but preserving expected behavior)
    #    -f image2: input type
    #    -r 1: framerate (1/s=s seconds per frame)
    #    -i %s/%%04d.png: input is all files like dir/0001.png
    #    -vcodec libvpx: x264 codec
    base= "ffmpeg -y -f image2 -r 3 -i %s/%%04d.png -vcodec libx264 -s 800x450 %s" % (dir, outfile )
    return base.split(' ')

if __name__=='__main__':
    access_id = 'AKIAJA4OAAY6T7HS6GQQ'
    secret = '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'
    pic_bucket_name = 'powershame-upload'
    vid_bucket_name = 'powershame-videos'
    renderer = SessionRenderer( access_id, secret, pic_bucket_name, vid_bucket_name, '/tmp/' )
    renderer.render( 'bob', '20130725210833' )
