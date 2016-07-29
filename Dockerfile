FROM andrewosh/binder-base

MAINTAINER Kirstie Whitaker <kw401@cam.ac.uk>

# Switch to root user for installation
USER root

# Update conda and install relevant dependencies
RUN conda update conda --yes --quiet
RUN conda config --add channels conda-forge
RUN conda install --yes --quiet matplotlib \
                                mayavi \
                                networkx \
                                nibabel \
                                numpy \
                                pandas \
                                scipy \
                                seaborn \
                                scikit-learn
RUN conda update anaconda --yes --quiet
RUN python -c "from matplotlib import font_manager"
RUN conda clean -ay

# Install dependencies in pip
RUN pip install --upgrade --quiet pip && \
    pip install --upgrade --quiet community \
                                  pysurfer \
                --ignore-installed

# Install the MCR dependencies and some things we'll need and download the MCR
# from Mathworks -silently install it. Code taken from: 
#   https://github.com/vistalab/docker/blob/master/matlab/runtime/2015b/Dockerfile
RUN apt-get -qq update && \
    apt-get install -y -qq unzip \
                           xorg \
                           wget \
                           curl
RUN mkdir /mcr-install && \
    mkdir /opt/mcr && \
    cd /mcr-install
RUN wget -q http://www.mathworks.com/supportfiles/downloads/R2015b/deployment_files/R2015b/installers/glnxa64/MCR_R2015b_glnxa64_installer.zip
RUN cd /mcr-install
RUN unzip -q MCR_R2015b_glnxa64_installer.zip
RUN ./install -destinationFolder /opt/mcr -agreeToLicense yes -mode silent
RUN cd /
RUN rm -rf mcr-install

# Configure environment variables for MCR
ENV LD_LIBRARY_PATH /opt/mcr/v90/runtime/glnxa64:/opt/mcr/v90/bin/glnxa64:/opt/mcr/v90/sys/os/glnxa64
ENV XAPPLRESDIR /opt/mcr/v90/X11/app-defaults

CMD ["/bin/bash"]
