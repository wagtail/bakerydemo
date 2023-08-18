import os
import shutil
import subprocess
import tempfile

from django.core.files.base import ContentFile
from src.wagtailvideos.ffmpeg import installed


def DEVNULL():
    return open(os.devnull, 'r+b')


def get_thumbnail(file_path):
    if not installed():
        raise RuntimeError('ffmpeg is not installed')

    file_name = os.path.basename(file_path)
    thumb_name = '{}_thumb{}'.format(os.path.splitext(file_name)[0], '.jpg')

    try:
        output_dir = tempfile.mkdtemp()
        output_file = os.path.join(output_dir, thumb_name)
        try:
            subprocess.check_call([
                'ffmpeg',
                '-v', 'quiet',
                '-itsoffset', '-1',
                '-i', file_path,
                '-vcodec', 'mjpeg',
                '-vframes', '1',
                '-an', '-f', 'rawvideo',
                '-vf', 'scale=iw:-1',  # Make thumbnail the size & aspect ratio of the input video
                output_file,
            ], stdin=DEVNULL(), stdout=DEVNULL())
        except subprocess.CalledProcessError:
            return None
        return ContentFile(open(output_file, 'rb').read(), thumb_name)
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)
