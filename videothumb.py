#!/usr/bin/env python3

import logging
import os
from time import time

import requests

from lib import run, response

THUMB_JPG = '/tmp/thumb.jpg'


def handler_http_get(event, context):
    try:
        qsps = event['queryStringParameters']
        inurl = qsps['inurl']
        outurl = qsps['outurl']
        seconds = qsps['seconds']
        wxh = qsps['wxh']
    except KeyError as err:
        return response(400, {'message': 'Specify inurl, outurl, seconds, wxh (%s)' % err})
    logging.warning('videothumb inurl=%s outurl=%s seconds=%s wxh=%s', inurl, outurl, seconds, wxh)
    try:
        res = make_thumb(inurl, outurl, seconds, wxh)
    except Exception as err:
        return response(500, {'message': 'Something bad happened: %s' % err})
    return response(200, {'message': res})


def make_thumb(inurl, outurl, seconds, wxh):
    """Make the thumbnail and upload, return status message; raise on error."""

    # ffmpeg -v quiet -y -ss 3.1416 -i $URL -vframes 1 -s 640x480 thumb.jpg
    #  '-v', 'quiet',
    ffmpeg_cmd = ['ffmpeg', '-v', 'warning', '-y', '-ss', seconds, '-i', inurl,
                  '-vframes', '1', '-s', wxh, THUMB_JPG]
    logging.warning('videothumb ffmpeg_cmd=%s', ffmpeg_cmd)
    t_0 = time()
    try:
        res = run(ffmpeg_cmd)
        logging.warning('FFMPEG res=%s', res)
    except RuntimeError as err:
        raise RuntimeError('Could not ffmpeg err=%s' % err)
    t_grab = time() - t_0
    logging.warning('url=%s frame_grab_seconds=%s', inurl, t_grab)

    # Can give it filepointer or body (bytes), but must supply size
    thumb_fp = open(THUMB_JPG, 'rb')
    thumb_len = str(os.path.getsize(THUMB_JPG))
    t_1 = time()
    res = requests.put(outurl, data=thumb_fp,
                       headers={'Content-Type': 'image/jpeg', 'Content-Length': thumb_len})
    t_upload = time() - t_1
    if res.status_code != 200:
        raise RuntimeError('Could not upload: %s' % res.text)
    return 'time_grab=%s time_upload=%s outurl=%s' % (t_grab, t_upload, outurl)


