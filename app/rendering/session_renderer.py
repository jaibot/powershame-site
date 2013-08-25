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
    def render( self, prefix, video_key ):
        working_path = os.path.join( self.working_dir, 'powershame-rendering', prefix )
        video_path=os.path.join( working_path, 'session.mkv' )
        try:
            os.makedirs( working_path )
        except OSError:
            pass
        self.download_shots( working_path, prefix )
        self.make_video( working_path, video_path )
        return self.upload_video( video_path, video_key )

    def download_shots( self, working_path, prefix ):
        bucket = self.s3_conn.get_bucket( self.shots_bucket )
        shot_keys_to_download = filter( is_shot, bucket.list( prefix=prefix ) )
        shot_keys_to_download.sort( key = lambda shot_key: shot_key.name )
        for i,shot in enumerate(shot_keys_to_download):
            filename = '%04d.png'%i
            shot.get_contents_to_filename( os.path.join( working_path, filename ) )

    def make_video( self, working_path, video_filename ):
        movie_maker = ffmpeg_str( working_path, video_filename )
        p = subprocess.call( movie_maker )

    def upload_video( self, video_path, key_path ):
        bucket = self.s3_conn.get_bucket( self.video_bucket, validate=False )
        key = Key(bucket)
        #bucket_key = username+'/'+session_name+'.mkv'
        key.key = key_path
        key.set_contents_from_filename( video_path )
        url = self.s3_conn.generate_url(3600*48, 'GET', bucket=self.video_bucket, key=key_path) #THIS IS HACKY - write seperate temp-url getter somewhere else
        return url

# below: utility functions
def is_shot( key ):
    return key.name.endswith('.png')

def ffmpeg_str( dir, outfile ):
    """compose string for rendering call"""
    #explanation of arguments to ffmpeg:
    #    -y: overwrite output file (not an issue in the current version, but preserving expected behavior)
    #    -f image2: input type
    #    -r 1: framerate (1/s=s seconds per frame)
    #    -i %s/%%04d.png: input is all files like dir/0001.png
    #    -vcodec libvpx: x264 codec
    # TODO: calculate resolution based off original resolution
    # TODO: alter framerate to speed up longer videos
    # TODO: time OSD and/or titlecards
    base= "ffmpeg -y -f image2 -r 3 -i %s/%%04d.png -vcodec libx264 -s 800x450 %s" % (dir, outfile )
    return base.split(' ')

if __name__=='__main__':
    renderer = SessionRenderer( access_id, secret, pic_bucket_name, vid_bucket_name, '/tmp/' )
