"""Library of functions used by probe and thumb code."""

import json
import logging
import subprocess as sp


def run(cmd_list):
    """Run the command and return stdout.

    :param list cmd_list: list of str for components of command
    :returns: string output of the command
    """
    logging.warning('run: cmd_list=%s' % cmd_list)
    try:
        ret = sp.Popen(cmd_list, stdout=sp.PIPE, stderr=sp.PIPE)
    except Exception as err:
        raise RuntimeError('run cmd="%s": %s' % (cmd_list, err))
    logging.warning('run: ret=%s' % ret)
    (stdout, stderr) = ret.communicate()
    logging.warning('run: stdout=%s' % stdout)
    if ret.returncode:
        stderr = stderr.decode('utf8')
        logging.error('run cmd="%s": %s' % (cmd_list, stderr))
        raise RuntimeError(stderr)
    return stdout.decode('utf8')


def response(code, body):
    """Return HTTP response code and JSONified body."""
    return {'statusCode': code,
            'body': json.dumps(body)}
