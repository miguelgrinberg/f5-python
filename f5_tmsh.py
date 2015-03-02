#!/usr/bin/env python
# Copyright 2014, Rackspace US, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# (c) 2015, Dennis DeMarco <dennis.demarco@rackspace.com>

from F5rest import F5rest
from F5rest import translate_dash
import argparse


def list_to_dict(list):
    data = {}
    for i in range(0, len(list),2):

        key = translate_dash(list[i])
        value = list[i+1]
        data[key] = value

    return data

def members_parse(members):
    tmp = []
    pos = 0
    pri = False

    for item in members:

        if item == 'priority-group':
            pri = True

        if (item != 'priority-group' and not pri):
           tmp.append({'name': item})
        if (item != 'priority-group' and pri):
           pri=False
           tmp[pos]['priorityGroup']=item
           pos=pos+1

    return tmp

def parse_args(token,args):

    subsets = ['profiles', 'persist',
               'source-address-translation','members'
    ]

    token_words =  len(token.split())
    arg_list= args.split()


    target = arg_list[token_words].split('/')
    if len(target) > 1:
        partition = target[1]
        name = target[2]
    else:
        partition = "Common"
        name = target[0]

    set=0
    data = {}
    pos = token_words+1
    word_string = False
    build_string = ""
    subset_flag = False
    data_return = {}
    tmp = []

    for word in arg_list[pos:]:

        if word == 'replace-all-with':
            continue

        if word == '{':
            set=set+1
            continue
        if word == '}':
            set=set-1
            if set ==1:
                subset_flag=False
            continue

        if word in subsets:
            subset_flag = True
            subset_key = word

        if word[0] == '"' and word_string == False:
            word_string=True

        if word_string == False:
            if subset_flag == False:
               if not data.has_key(set):
                   data[set] = [word]
               else:
                   data[set].append(word)
            else:
                if not data.has_key(subset_key):
                    data[subset_key] = []
                else:
                    data[subset_key].append(word)

        if word_string:
           if len(build_string) >0:
               build_string=build_string + " " + word
           else:
              build_string=build_string + word


        if word[-1] == '"' and word_string == True:
            data[set].append(build_string)
            build_string = ""
            word_string=False

    try:
       tmp = data[1]
    except:
       pass

    for i in range(0, len(tmp),2):
        key = translate_dash(tmp[i])
        value = tmp[i+1]
        data_return[key] = value

    for key in data.keys():
        if key in subsets:
            if key == 'profiles':
                data_return[key] = [{ 'name': data[key][0]}]

            if key == 'persist':
                data_return[key] = data[key][0]

            if key == 'source-address-translation':
                data_return[translate_dash(key)]=list_to_dict(data[key])

            if key == 'members':
               data_return[key]=members_parse(data[key])


    return name,partition,data_return

def status_code(status_obj):
    if status_obj.status_code == 409:
        return "Exists"

    if status_obj.status_code ==200:
        return "Ok"

    if status_obj.status_code ==404:
        return "Error"

    if status_obj.status_code ==400:
        return status_obj.text

    return status_obj.text

def do_create_partition(token,args,my_f5):

    partition = args.split(token)[1].lstrip()
    result = my_f5.create_partition(partition)
    print "Creating New F5 Partition .... [%s] ... [%s]" % (partition,status_code(result))

def do_modify_globalSettings(token,args,my_f5):
    result = my_f5.cli_service_number()
    print "Modifying CLI gloabl-settings ... [%s]" % status_code(result)

def do_create_monitor_mysql(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_monitor_mysql(partition,name,**data)
    print "Creating MySQL Monitor ... [%s] ... [%s]" % (name,status_code(result))

def do_create_monitor_http(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_monitor_http(partition,name,**data)
    print "Creating Http Monitor ... [%s] ... [%s]" % (name,status_code(result))

def do_create_monitor_https(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_monitor_https(partition,name,**data)
    print "Creating Https Monitor ... [%s] ... [%s]" % (name,status_code(result))


def do_create_monitor_tcp(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_monitor_tcp(partition,name,**data)
    print "Creating TCP Monitor ... [%s] ... [%s]" % (name,status_code(result))

def do_install_cert(token,args,my_f5):
    (file,partition,data) = parse_args(token,args)
    path = '/var/tmp/' + file

    name = file[:-4]
    print "SFTP ssl file ...[%s]" % file
    my_f5.put_sftp(file, path)

    result = my_f5.install_cert(partition,name,path)
    print "Installing cert ... [%s] ... [%s]" % (name,status_code(result))


def do_install_key(token,args,my_f5):
    (file,partition,data) = parse_args(token,args)
    path = '/var/tmp/' + file

    name = file[:-4]
    print "SFTP ssl file ...[%s]" % file
    my_f5.put_sftp(file, path)

    result = my_f5.install_key(partition,name,path)
    print "Installing key ... [%s] ... [%s]" % (name,status_code(result))


def do_create_profile_client_ssl(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_profile_client_ssl(partition,name,**data)
    print "Creating Profile client-ssl ... [%s] ... [%s]" % (name,status_code(result))

def do_create_profile_server_ssl(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_profile_server_ssl(partition,name,**data)
    print "Creating Profile ... [%s] ... [%s]" % (name,status_code(result))


def do_create_persistence_source_addr(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_persistence_source_addr(partition,name,**data)
    print "Creating Persistence source-addr... [%s] ... [%s]" % (name,status_code(result))

def do_create_persistence_cookie(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_persistence_cookie(partition,name,**data)
    print "Creating Persistence cookie... [%s] ... [%s]" % (name,status_code(result))

def do_create_node(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_node(partition,name,**data)
    print "Creating Node ... [%s] ... [%s]" % (name,status_code(result))

def do_create_pool(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_pool(partition,name,**data)
    print "Creating Pool ... [%s] ... [%s]" % (name,status_code(result))

def do_create_monitor_external(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)
    result = my_f5.create_monitor_external(partition,name,**data)
    print "Creating external monitor ... [%s] ...[%s]" % (name,status_code(result))

def do_create_sys_file_external(token,args,my_f5):
    (name,partition,data)=parse_args(token,args)

    path=data['sourcePath']
    file = path.split('/')[-1]

    print "SFTP external monitor ...[%s]" % file
    my_f5.put_sftp(file, '/config/monitors/' + file)
    result = my_f5.create_sys_file_external(partition,name,path)
    print "Creating sys file .. [%s] ...[%s]" % (name,status_code(result))


def do_create_virtual(token,args,my_f5):
    (name,partition,data) = parse_args(token,args)

    result = my_f5.create_virtual(partition,name,**data)
    print "Creating Virtual Server ... [%s] .... [%s]" % (name,status_code(result))

def do_create_snatpool(token,args,my_f5):
     (name,partition,data)=parse_args(token,args)
    # snat pool has just a list of members not a dict unlike almost every other rest call.
     tmp = []

     for member in data['members']:
         tmp.append(member['name'])

     result  = my_f5.create_snatpool(partition,name,tmp)
     print "Creating SNATPool ... [%s] ...[%s]" % (name,status_code(result))

def do_nothing(token,args,my_f5):
    pass

def parse_line(line,my_f5):

    tokens_callables = {'create auth partition': do_create_partition,
                        'modify cli global-settings service number': do_modify_globalSettings,
                        'create ltm snatpool': do_create_snatpool,
                        'create ltm monitor mysql': do_create_monitor_mysql,
                        'create ltm monitor http ' : do_create_monitor_http,
                        'create ltm monitor https ': do_create_monitor_https,
                        'create ltm monitor tcp': do_create_monitor_tcp,
                        'create ltm monitor external': do_create_monitor_external,
                        'create sys file external-monitor': do_create_sys_file_external,
                        'install sys crypto cert': do_install_cert,
                        'install sys crypto key': do_install_key,
                        'create ltm profile client-ssl':do_create_profile_client_ssl,
                        'create ltm profile server-ssl':do_create_profile_server_ssl,
                        'create ltm persistence source-addr': do_create_persistence_source_addr,
                        'create ltm persistence cookie': do_create_persistence_cookie,
                        'create ltm node': do_create_node,
                        'create ltm pool': do_create_pool,
                        'create ltm virtual': do_create_virtual
          }

    for token in tokens_callables.keys():

        if  (line.find(token) >= 0):
         functionToCall = tokens_callables[token]
         functionToCall(token,line,my_f5)

def args():
    """Setup argument Parsing."""
    parser = argparse.ArgumentParser(
        usage='%(prog)s',
        description='Rackspace Openstack, F5 Rest from Inventory Generator output',
        epilog='F5 tmsh parser Licensed "Apache 2.0"')

    parser.add_argument(
        '-f',
        '--file',
        help='Inventory file. Default: [ %(default)s ]',
        required=False,
        default='rpc_f5_config.sh'
    )


    parser.add_argument(
        '--username',
        help='user name to connect to F5',
        required=True,
        default=None
    )

    parser.add_argument(
        '--hostname',
        help='F5 hostname to configure',
        required=True,
        default=None
    )

    parser.add_argument(
        '--password',
        help='Password to connect to F5.',
        required=True,
        default=None
    )

    return vars(parser.parse_args())


def main():

  user_args = args()

  with open(user_args['file']) as f:
    content = f.read().splitlines()

  my_f5 = F5rest(user_args['hostname'],user_args['username'],user_args['password'])


  for line in content:
    parse_line(line,my_f5)

if __name__ == "__main__":
    main()
