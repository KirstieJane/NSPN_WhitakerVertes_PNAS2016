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

CMD ["/bin/bash"]
