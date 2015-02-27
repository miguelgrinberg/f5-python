#!/usr/bin/python
import requests, json
import string,os,socket

import paramiko
from paramiko.py3compat import input

requests.packages.urllib3.disable_warnings()


def translate_dash(word):
     """ This function returns the F5 Rest variable name from a ltm dashed variable name """

     words = word.split('-')
     translate=words[0]

     for x in range(1,len(words)):
         translate=translate + string.capitalize(words[x])

     return translate
class F5rest(object):

    def __init__(self,address,user,password):
       self.BIGIP_ADDRESS = address
       self.BIGIP_USER = user
       self.BIGIP_PASS = password
       self.BIGIP_URL_BASE = 'https://%s/mgmt/tm' % self.BIGIP_ADDRESS

       self.bigip = requests.session()
       self.bigip.auth = (self.BIGIP_USER,self.BIGIP_PASS)
       self.bigip.verify = False
       self.bigip.headers.update({'Content-Type' : 'application/json'})

       print "created REST resource for BIG-IP at %s..." % self.BIGIP_ADDRESS


    def put_sftp(self,source,dest):

       hostkeytype = None
       hostkey = None
       try:
            host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
       except IOError:
          try:
              # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
              host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
          except IOError:
               print('*** Unable to open host keys file')
               host_keys = {}

       if self.BIGIP_ADDRESS in host_keys:
           hostkeytype = host_keys[self.BIGIP_ADDRESS].keys()[0]
           hostkey = host_keys[self.BIGIP_ADDRESS][hostkeytype]
           print('Using host key of type %s' % hostkeytype)

       paramiko.util.log_to_file('f5_sftp.log')
       try:
          t = paramiko.Transport((self.BIGIP_ADDRESS, 22))
          t.connect(hostkey, self.BIGIP_USER, self.BIGIP_PASS, gss_host=socket.getfqdn(self.BIGIP_ADDRESS),
                     gss_auth=False, gss_kex=False)

          self.sftp = paramiko.SFTPClient.from_transport(t)

          #self.sftp.put('demo_sftp.py', '/config/monitors/RPC-MON-EXT-ENDPOINT.monitor')
          self.sftp.put(source,dest)

       except Exception as e:
           print('*** Caught exception: %s: %s' % (e.__class__, e))
       try:
            self.t.close()
       except:
            pass

    def translate_slash(self,word):
       """ This function returns ~ where slashes are, REST interfaces hates slashes """
       return word.replace("/","~")


    def create_partition(self,name):
        payload = {}
        payload['name'] = "/" + name
        return self.bigip.post('%s/sys/folder' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_partition(self,name):
        return self.bigip.delete('%s/sys/folder/~%s' % (self.BIGIP_URL_BASE, name))

    def cli_service_number(self):
        payload = {}
        payload['service'] = "number"
        return self.bigip.put('%s/cli/global-settings' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def create_snatpool(self,partition,name,members):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name
        payload['members'] = members

        return self.bigip.post('%s/ltm/snatpool' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_snatpool(self,partition,name):
        return self.bigip.delete('%s/ltm/snatpool/~%s~%s' % (self.BIGIP_URL_BASE,partition,name))

    def create_monitor_mysql(self,partition,name, **kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/monitor/mysql' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_monitor_mysql(self,partition,name):
        return self.bigip.delete('%s/ltm/monitor/mysql/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_monitor_http(self,partition,name, **kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/monitor/http' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_monitor_http(self,partition,name):
        return self.bigip.delete('%s/ltm/monitor/http/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_monitor_https(self,partition,name, **kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/monitor/https' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_monitor_https(self,partition,name):
        return self.bigip.delete('%s/ltm/monitor/https/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_monitor_tcp(self,partition, name, **kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/monitor/tcp' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_monitor_tcp(self,partition,name):
        return self.bigip.delete('%s/ltm/monitor/tcp/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_sys_file_external(self,partition,name,path):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name
        payload['source-path']= path

        return self.bigip.post('%s/sys/file/external-monitor' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_sys_file_external(self,partition,name):
        return self.bigip.delete('%s/sys/file/external-monitor/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_monitor_external(self,partition,name,**kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/monitor/external' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_monitor_external(self,partition,name):
        return self.bigip.delete('%s/ltm/monitor/external/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_persistence_source_addr(self,partition,name,**kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/persistence/source-addr' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_persistence_source_addr(self,partition,name):
        return self.bigip.delete('%s/ltm/persistence/source-addr/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_persistence_cookie(self,partition,name,**kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/persistence/cookie' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_persistence_cookie(self,partition,name):
        return self.bigip.delete('%s/ltm/persistence/cookie/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_profile_client_ssl(self,partition,name,**kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/profile/client-ssl' % self.BIGIP_URL_BASE, data=json.dumps(payload))


    def delete_profile_client_ssl(self,partition,name):
        return self.bigip.delete('%s/ltm/profile/client-ssl/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))


    def create_profile_server_ssl(self,partition,name,**kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/profile/server-ssl' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_profile_server_ssl(self,partition,name):
        return self.bigip.delete('%s/ltm/profile/server-ssl/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))


    def create_node(self,partition,name,**kwargs):
        payload = {}
        payload['partition'] = partition
        payload['name'] = name

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/node' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_node(self,partition,name):
        return self.bigip.delete('%s/ltm/node/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def install_cert(self,partition,name,path):
         payload = {}
         payload['command'] = "install"
         payload['name'] = name
         payload['partition'] = partition
         payload['from-local-file'] = path

         return self.bigip.post('%s/sys/crypto/cert' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_cert(self,partition,name):
         return self.bigip.delete('%s/sys/crypto/cert/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def install_key(self,partition,name,path):
         payload = {}
         payload['command'] = "install"
         payload['name'] = name
         payload['partition'] = partition
         payload['from-local-file'] = path

         return self.bigip.post('%s/sys/crypto/key' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_key(self,partition,name):
         return self.bigip.delete('%s/sys/crypto/key/~%s~%s' % (self.BIGIP_URL_BASE, partition, name))

    def create_pool(self,partition,name, **kwargs):
        payload= {}
        members = []


        for member in kwargs['members']:
            member['kind'] = 'ltm:pool:members'
            members.append(member)

        payload['kind'] = 'tm:ltm:pool:poolstate'
        payload['name'] = name
        payload['partition'] = partition

        payload['members'] = members

        for item in kwargs:
            payload[item] = kwargs[item]

        return self.bigip.post('%s/ltm/pool' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_pool(self, partition, name):
        return self.bigip.delete('%s/ltm/pool/~%s~%s' % (self.BIGIP_URL_BASE, partition,name))

    def create_virtual(self,partition,name, **kwargs):
        payload = {}

        # define test virtual
        payload['kind'] = 'tm:ltm:virtual:virtualstate'
        payload['name'] = name
        payload['partition'] = partition


        for item in kwargs:
            payload[item] = kwargs[item]

        if not 'sourceAddressTranslation' in kwargs.keys():
            payload['sourceAddressTranslation'] = { 'type' : 'automap' }

        if not 'profiles' in kwargs.keys():
            payload['profiles'] = [
            { 'kind' : 'ltm:virtual:profile', 'name' : 'http' },
            { 'kind' : 'ltm:virtual:profile', 'name' : 'tcp' }
        ]

        return self.bigip.post('%s/ltm/virtual' % self.BIGIP_URL_BASE, data=json.dumps(payload))

    def delete_virtual(self, partition,name):
        return self.bigip.delete('%s/ltm/virtual/~%s~%s' % (self.BIGIP_URL_BASE,partition, name))



def main():
    pass

if __name__ == "__main__":
    main()
