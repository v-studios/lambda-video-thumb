#!/usr/bin/env python3

import json
import logging
import os

from lib import run, response


def handler_http_get(event, context):
    logging.debug('# event=%s' % json.dumps(event))
    os.environ['PATH'] = 'bin:' + os.environ['PATH']
    qsps = event['queryStringParameters']  # already url-decoded for us
    try:
        inurl = qsps['inurl']
    except KeyError:
        return response(400, {'message': 'Must specify inurl=...'})
    logging.warning('videoprobe inurl=%s' % inurl)
    ffprobe_cmd = ('ffprobe -v quiet -print_format json -show_streams -select_streams v:0'
                   ' -show_entries stream=width,height,duration').split()
    ffprobe_cmd.append(qsps['inurl'])
    try:
        out_json = run(ffprobe_cmd)
    except RuntimeError as err:
        return response(500, {'message': 'Could not ffprobe inurl=%s err=%s' % (inurl, err)})
    try:
        out = json.loads(out_json)
    except json.decoder.JSONDecodeError:
        return response(500, {'message': 'Could not decode json=%s' % out_json})
    if out == {}:
        return response(500, {'message':
                              'Could not extract anything from inurl=%s (nonexistent?)' % inurl})
    try:
        stream = out['streams'][0]
        width = int(float(stream['width']))
        height = int(float(stream['height']))
        seconds = float(stream['duration'])
    except KeyError as err:
        return response(500, {'message':
                              'Could not extract data from inurl=%s out=%s: %s' % (inurl, out, err)})
    return response(200,
                    {'message': 'probe values',
                     'urlin': inurl, 'width': width, 'height':  height, 'seconds': seconds})
