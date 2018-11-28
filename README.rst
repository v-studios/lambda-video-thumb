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




.. _exodus: https://github.com/intoli/exodus
