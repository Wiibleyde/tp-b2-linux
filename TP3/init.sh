# Init user script

# Create a new user monit
useradd -m -s /bin/bash monit

# Create a new group monit
groupadd monit

# Add monit to the group monit
usermod -a -G monit monit

# Create a new directory /var/monit and set the owner to monit:monit
mkdir /var/monit
chown monit:monit /var/monit

# Add user current user (not root) to the group monit
usermod -a -G monit $USER

