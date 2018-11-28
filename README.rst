====================
 Lambda Video Thumb
====================

Compile ffmpeg to run in Lambda, see
https://docs.google.com/document/d/13RJVk64J983wNo6BWwJqTxIAeaM5GBDfI4ehX1kHD0c/edit#

Packaget it into Lambda with something like the avail_pipeline/videothumb.py

We'll probably need API endpoints to probe for dimensions and duration
so the caller can know what sizes to request (e.g., probably don't
want to scale up and pixelize, but our service shouldn't disallow it).

API input should include:
* HTTP endpoint we can read video from (public HTTP, S3 presigned URL)
* width x height (ints) or scale-percent (int)
* Output: presigned URL to PUT to

FROM
