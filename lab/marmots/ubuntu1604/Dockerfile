FROM ubuntu:16.04

RUN apt-get update && \
apt-get -y install python openssh-server sudo whois

RUN useradd -m -p `echo "ansible-yuto" | mkpasswd -s -m sha-512` ansible-yuto && \
mkdir -p /home/ansible-yuto/.ssh

ADD ./keys/ansible-yuto.pub /home/ansible-yuto/.ssh/authorized_keys
RUN chmod 400 /home/ansible-yuto/.ssh/* && \
chown ansible-yuto:ansible-yuto /home/ansible-yuto/.ssh/* && \
echo "AuthorizedKeysFile %h/.ssh/authorized_keys" >> /etc/ssh/sshd_config && \
mkdir -p  /var/run/sshd && \
echo "ansible-yuto ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

EXPOSE 22

ENTRYPOINT ["/usr/sbin/sshd","-D"]
