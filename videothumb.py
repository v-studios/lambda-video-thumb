#!/usr/bin/env python3

import json
import logging
import os
import subprocess as sp

QS = ('inurl', 'outurl', 'wxh', 'scale', 'ffprobe')  # inurl or urlin?
FFPROBE = ('ffprobe -v quiet -print_format json -show_streams -select_streams v:0'
           ' -show_entries stream=width,height,duration')
# FFPROBE = ('ffprobe -show_streams -select_streams v:0'
#            ' -show_entries stream=width,height,duration')
# FFPROBE = 'ffprobe -version'


def run(cmd_list):
    """Run the command and return stdout.

    :param list cmd_list: list of str for components of command
    :returns: string output of the command
    """
    # Let it raise exceptions to our caller; most likely couldn't find the URL
    # Wasn't capturing stderr that I could see
    # ret = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT)
    logging.warning('# run: about to Popen cmd_list=%s' % cmd_list)
    ret = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
    (stdout, stderr) = ret.communicate()
    logging.warning('# stdout=%s' % stdout.decode('utf8'))
    if stderr:
        loggging.error('# Run got error,  decoding')
        stderr = stderr.decode('utf8')
        logging.error('run "%s" failed: %s' % (run_cmd, stderr))
        raise RuntimeError(stderr)
    return stdout.decode('utf8')


def response(code, body):
    """Return HTTP response code and JSONified body."""
    return {'statusCode': 400,
            'body': json.dumps(body)}


def handler_http_get(event, context):
    # We get our input params from event.input[] like:
    # "queryStringParameters": {"inurl": "INURL", "outurl": "OUTURL", "wxh": "640x480"}
    # And they are already URL decoded for us.
    # FYI: events with s3 key needs:  unquote_plus(record['s3']['object']['key'])
    logging.warning('# event=%s' % json.dumps(event))
    # path=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin
    os.environ['PATH'] = 'bin:' + os.environ['PATH']
    logging.warning('### path=%s', os.environ['PATH'])
    qsps = event['queryStringParameters']
    for qsp in qsps:
        if qsp not in QS:
            return response(400, f'Unknown qsp={qsp} use: {QS}')
    inurl = qsps['inurl']
    logging.warning('# inurl=%s' % inurl)

    # TODO: this should be a separate handler or separate lambda
    if 'ffprobe' in qsps:
        logging.warning('# got ffprobe, building command')
        ffprobe_cmd = FFPROBE.split()  # don't split the URL, may have embedded spaces
        ffprobe_cmd.append(qsps['inurl'])
        try:
            logging.warning('# calling FFPROBE: %s' % ffprobe_cmd)
            out_json = run(ffprobe_cmd)
            logging.warning('# called FFPROBE: %s' % ffprobe_cmd)
        except RuntimeError as err:
            logging.error('# FAILED PROCESS FFPROBE: %s' % ffprobe_cmd)
            return(500, {'message': 'Could not ffprobe inurl=%s err=%s' % (inurl, err)})
        except subprocess.CalledProcessError as err:
            logging.error('# FAILED PROCESS FFPROBE: %s' % ffprobe_cmd)
            return(500, {'message': 'Could not ffprobe inurl=%s err=%s' % (inurl, err)})
        logging.warning('# Getting out from out_json=%s' % out_json)
        out = json.loads(out_json)
        logging.warning('# Getting stream from out=%s' % out)
        stream = out['streams'][0]
        logging.warning('# returning...')
        width = int(float(stream['width']))
        height = int(float(stream['height']))
        seconds = float(stream['duration'])
        return response(200,
                        {'message': 'probe values',
                         'urlin': inurl, 'width': width, 'height':  height, 'seconds': seconds})
    return response(400, {'message': 'not implemented', 'andonemorething': 'foo'})
