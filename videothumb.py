import json
import logging
import os
import subprocess

QS = ('inurl', 'outurl', 'wxh', 'scale', 'ffprobe')  # inurl or urlin?
FFPROBE = ('ffprobe -v quiet -print_format json -show_streams -select_streams v:0'
           ' -show_entries stream=width,height,duration')
FFPROBE = ('ffprobe -show_streams -select_streams v:0'
           ' -show_entries stream=width,height,duration')
FFPROBE = 'ffprobe -version'


def _run(cmd_list):
    """Run the command and return stdout.

    :param list cmd_list: list of str for components of command
    :returns: string output of the command
    """
    # Let it raise exceptions to our caller; most likely couldn't find the URL
    ret = subprocess.check_output(cmd_list, stderr=subprocess.STDOUT)
    return ret.decode('utf8')


def response(code, body):
    """Return HTTP response code and JSONified body."""
    return {'statusCode': 400,
            'body': json.dumps(body)}


def handler_http_get(event, context):
    # We get our input params from event.input[] like:
    # "queryStringParameters": {"inurl": "INURL", "outurl": "OUTURL", "wxh": "640x480"}
    # And they are already URL decoded for us.
    # FYI: events with s3 key needs:  unquote_plus(record['s3']['object']['key'])
    print('### type(event)=%s' % type(event))
    logging.warning('### event qsp=%s', event['queryStringParameters'])
    logging.warning('### path=%s', os.environ['PATH'])
    os.environ['PATH'] = 'exodus/bin:' + os.environ['PATH']
    logging.warning('### path=%s', os.environ['PATH'])
    qsps = event['queryStringParameters']
    for qsp in qsps:
        if qsp not in QS:
            return response(400, f'Unknown qsp={qsp} use: {QS}')
    inurl = qsps['inurl']

    # TODO: this should be a separate handler or separate lambda
    if 'ffprobe' in qsps:
        ffprobe_cmd = FFPROBE.split()  # don't split the URL, may have embedded spaces
        ####ffprobe_cmd.append(qsps['inurl'])
        try:
            out_json = _run(ffprobe_cmd)
        except subprocess.CalledProcessError as err:
            raise RuntimeError('Could not ffprobe inurl=%s err=%s' % (inurl, err))
        out = json.loads(out_json)
        stream = out['streams'][0]
        return {200,
                {'message': 'probe values',
                 'urlin': inurl,
                 'width': int(float(stream['width'])),
                 'height':  int(float(stream['height'])),
                 'seconds': float(stream['duration'])}
                }
    return response(400, {'message': 'not implemented'})
