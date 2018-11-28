# Use Docker to build ffmpeg that will run on Lambda::
#   docker build -t shentonfreude/build-ffmpeg .
# Copy built bits to `/exodus` directory under our local dir::
#   docker run --rm -v "$PWD":/export shentonfreude/build-ffmpeg
# Run the built ffmpeg and find its version (2.8.15)::
#  docker run --rm  shentonfreude/build-ffmpeg exodus/bin/ffmpeg --version
# Probe an movie at an S3 URL:
#  docker run --rm  shentonfreude/build-ffmpeg exodus/bin/ffprobe $URL
# Create a thumbnail on local disk from $URL:
#  docker run --rm -v ${PWD}:/export shentonfreude/build-ffmpeg \
#         exodus/bin/ffmpeg -v quiet -y -ss 3.1416 \
#         -i $URL -vframes 1 -s 640x480 /export/thumb.jpg
###############################################################################

# Once we get Centos working, switch to AMZ Linux, or lambci
FROM centos:7.5.1804

MAINTAINER Chris Shenton <chris@v-studios.com>

# ffmpeg isn't in distros, add other repo and install:
RUN yum install -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
RUN yum install -y ffmpeg

# install the exodus tool which bundles relocatable binaries
RUN yum install -y python-pip
RUN pip install --user exodus_bundler

# Run the locally-installed exodus: 
RUN ${HOME}/.local/bin/exodus --tarball ffmpeg|tar -zx
RUN ${HOME}/.local/bin/exodus --tarball ffprobe|tar -zx

# Output goes to ./exodus/{bin,bundles,data}/
RUN du -h exodus

# RUN exodus/bin/ffprobe http://images-assets.dev.nasawestprime.com/video/SMALLTOY-WP835/SMALLTOY-WP835~orig.mp4

# RUN exodus/bin/ffmpeg -v quiet -y -ss 3.1416 -i http://images-assets.dev.nasawestprime.com/video/SMALLTOY-WP835/SMALLTOY-WP835~orig.mp4 -vframes 1 -s 640x480 thumb.jpg

CMD cp -r exodus /export/


