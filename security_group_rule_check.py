import boto3
import boto
import boto.utils
from boto.vpc import VPCConnection


client = boto3.client("ec2")
conn=boto.vpc.connect_to_region("us-west-2")
client.meta.events._unique_id_handlers['retry-config-ec2']['handler']._checker.__dict__['_max_attempts'] = 20

##Below lines will connect to the vpc and look at the instaces (by instance IDs)##

sum=0
tag_list=list()
grp_list=list()
reservations = conn.get_all_reservations()
for r in reservations:
    for inst in r.instances:
#        grp_list=list()
       for group in inst.groups:
           if group.id not in grp_list:grp_list.append(group.id)

##Below Lines will connect check all the security Groups in the AWs environment for port 80 in the inbound Rules and will print out all the security groups which have that Rule##

for i in grp_list:
    response = client.describe_security_groups(
                     GroupIds=[
                     i,
                  ],
                )

    for k in response['SecurityGroups']:
        for l in k['IpPermissionsEgress']:
            if 'ToPort' not in l: continue
            elif l['ToPort']==80: print i
            else: continue
