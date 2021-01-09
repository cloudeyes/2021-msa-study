FROM centos:centos7

# Initializing the main user and setting up ssh server.
RUN groupadd smprc; mkdir /users; useradd -g smprc -md /users/smprc smprc; \
PWD=p@ssw0rd; echo -e "$PWD\n$PWD" | (passwd --stdin smprc); \
echo ssh user password: $PWD

# Install required packages and add sudo permission to smprc
RUN yum -y install openssh-server openssh-clients sudo; yum clean all; \
mkdir /var/run/sshd; ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''; \
sed -i 's/^#\s*\(%wheel\s*ALL=(ALL)\s*NOPASSWD:\s*ALL\)/\1/' /etc/sudoers; usermod -aG wheel smprc

# Setting up the miniconda environment.
USER smprc
ADD --chown=smprc https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh /tmp/miniconda-install.sh
RUN sh /tmp/miniconda-install.sh -b -p ~/conda; \
echo 'eval "$(/users/smprc/conda/bin/conda shell.bash hook)"' >> ~/.bash_profile; \
source ~/.bash_profile; \
conda create -y -n lab -c conda-forge python=3.9 jupyterlab; \
conda clean -afy

# Setting up jupyter-lab
COPY --chown=smprc files/jupyter_lab_config.py /users/smprc/.jupyter/jupyter_lab_config.py
COPY --chown=smprc files/jupyter_server_config.json /users/smprc/.jupyter/jupyter_server_config.json

# Restore to the root user.
USER root
COPY files/start.sh /root/start.sh
RUN chmod +x /root/start.sh

ENTRYPOINT /root/start.sh
