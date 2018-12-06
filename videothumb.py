#!/usr/bin/env python3

import logging
import os

from lib import run, response


def handler_http_get(event, context):
    os.environ['PATH'] = 'bin:' + os.environ['PATH']
    qsps = event['queryStringParameters']
    try:
        inurl = qsps['inurl']
        outurl = qsps['outurl']
        wxh = qsps['wxh']
    except KeyError as err:
        return response(400, {'message': 'Specify inurl, outurl, wxh (%s)' % err})
    logging.warning('videothumb inurl=%s outurl=%s wxh=%s' % (inurl, outurl, wxh))

    # Construct the command, only adding the optional scaling "-s WxH" if needed
    # ffmpeg -v quiet -y -ss 3.1416 -i $URL -vframes 1 -s 640x480 thumb.jpg
    ffmpeg_cmd = ['ffmpeg', '-v', 'quiet', '-y', '-ss', str(seconds), '-i', self.url,
                  '-vframes', '1', '-s', '%sx%s' % (width, height), '/tmp/out.jpg']
    t_0 = time()
    try:
        run(ffmpeg_cmd)
    except RuntimeError as err:
        raise RuntimeError('Could not ffmpeg err=%s' % err)
    t_grab = time() - t_0
    self.log.debug('url=%s frame_grab_seconds=%s', inurl, t_grab)
    # Can give it body (bytes) or filepointer, but must supply size
    thumb_fp = open('/tmp/out.jpg', 'rb')
    thumb_len = str(os.path.getsize('/tmp/out.jpg'))
    t_1 = time()
    res = requests.put(psurl, data=thumb_fp, headers={'Content-Type': 'image/jpeg', 'Content-Length': thumb_len})
    t_upload = time() - t_1
    if res.code != 200:
        return response(500, {'message': 'could not upload: %s' % res.text})
    return response(200, {'message': 'time_grab=%s time_upload%s outurl=%s' % (t_grab, t_upload, outurl)})



def main():
    from urllib.parse import urlencode
    inurl = s3.generate_presigned_url('put_object',
                                      ExpiresIn=600,
                                      Params={'Bucket': 'cshenton-test-presigned',
                                              'Key': 'video.mp4'})
    outurl = s3.generate_presigned_url('put_object',
                                       ExpiresIn=600,
                                       Params={'Bucket': 'cshenton-test-presigned',
                                               'Key': 'thumbout.jpg',
                                               'ContentType': 'image/jpeg'})
    secs = 4
    params = urlencode({'urlin': urlin, 'urlout': outurl, 'wxh': '640x480'})
    # invoke our lambda with those params
