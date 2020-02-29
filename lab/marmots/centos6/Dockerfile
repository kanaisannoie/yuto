FROM centos:centos6

RUN yum -y install openssh-server expect sudo whois libselinux-python selinux-policy

# RUN useradd -m -p `echo "ansible" | mkpasswd -s -m sha-512` ansible && \
RUN useradd -m ansible-yuto -d /home/ansible-yuto && \
echo "ansible-yuto"|passwd --stdin ansible-yuto && \
mkdir -p /home/ansible-yuto/.ssh

ADD ./keys/ansible-yuto.pub /home/ansible-yuto/.ssh/authorized_keys
RUN chmod 600 /home/ansible-yuto/.ssh/* && \
chown ansible-yuto:ansible-yuto /home/ansible-yuto/.ssh/* && \
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config && \
mkdir -p  /var/run/sshd && \
echo "ansible-yuto ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
ssh-keygen -t rsa -N "" -f /etc/ssh/ssh_host_rsa_key && \
touch /etc/sysconfig/network

RUN echo "root"|passwd --stdin root

EXPOSE 22

ENTRYPOINT ["/usr/sbin/sshd","-D"]
