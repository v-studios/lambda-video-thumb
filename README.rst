====================
 Lambda Video Thumb
====================

Use Docker to compile ``ffmpeg`` to run in Lambda, and bundle it with
exodus_. We commit that exported tree here so we don't need to do
this each time.

Package it with something like the ``avail_pipeline/videothumb.py``.

We'll probably need API endpoints to probe for dimensions and duration
so the caller can know what sizes to request (e.g., probably don't
want to scale up and pixelize, but our service shouldn't disallow it).

API input should include:

* HTTP URL from which we can GET video (e.g., public, S3 presigned)
* width x height (ints) or scale-percent (int)
* Output: presigned URL to PUT to

So maybe URLs like:

* ``vthumb?inurl=URL&probe``: return JSON {width: w, height: h, seconds: s}
* ``vthumb?inurl=URL&outurl=PSURL&scale=50``: return simple JSON status
* ``vthumb?inurl=URL&outurl=PSURL&wxh=640x480``: return simple JSON status

In all cases, inurl and outurl must be encoded so that internal characters like ``&`` don't break the querystring parsing, e.g.:

  from urllib.parse import urlencode
  urlencode({'urlin':'https://host:80/func&option/file.mp4', 'urlout': 'https://s3/presigned&token=foo.mp4', 'wxh': '640x480'})
  'urlin=https%3A%2F%2Fhost%3A80%2Ffunc%26option%2Ffile.mp4&urlout=https%3A%2F%2Fs3%2Fpresigned%26token%3Dfoo.mp4&wxh=640x480'


Consider breaking up ``ffmpeg`` and ``ffprobe`` into separate lambdas
for packaging. If each one is large, it may be hard to fit both into a
single lambda bundle. Creating probe and thumbnail lambdas should make
individual packages smaller. There's no real point in combining the
functionality in a single lambda anyway. With both ffmpeg and ffprobe,
it's too big to deploy the function by itself, we have to do a full
deploy each time.

Maybe we don't have to build the binary; this post shows using the
static binary as a Lambda layer:

https://serverless.com/blog/publish-aws-lambda-layers-serverless-framework


.. _exodus: https://github.com/intoli/exodus
