# f5-python
============

F5-python adds a rest api and tmsh parser for managing F5 bigip load balancers. It was written
to parse the output of the ansible-openstack f5-config.py program.

f5-5-5.py
=========
The f5-5-5.py program is a branch of the f5-config.py script for the 10.x RPC release. It will take
a rpc inventory json file and output tmsh commands that a tech can cut and paste into the shell.


f5_tmsh.py
==========
This program takes the output of the above program tmsh output, parses the commands and makes the rest calls
to configure the F5 device. It will use paramiko to upload ssl keys and certificates as well as external monitors
to the device.

<pre>
usage: f5_tmsh.py

Rackspace Openstack, F5 Rest from Inventory Generator output

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Inventory file. Default: [ rpc_f5_config.sh ]
  --username USERNAME   user name to connect to F5
  --hostname HOSTNAME   F5 hostname to configure
  --password PASSWORD   Password to connect to F5.

F5 tmsh parser Licensed "Apache 2.0"
</pre>

Parsing tmsh
=============

Some considerations are needed when parsing the tmsh. { must be spaced around keywords.
Example below


BAD
<pre>
create ltm snatpool /RPC/RPC_SNATPOOL {members replace-all-with {172.29.236.15}}
</pre>

GOOD
<pre>
create ltm snatpool /RPC/RPC_SNATPOOL { members replace-all-with { 172.29.236.15 } }
</pre>

The parser also expects to see a format like below:

token /Partiton/Name { commands }

BUGS
====

Yes it has, this is an alpha version. It has not been tested extensively. It should work with all previous versions
of f5-config.py
