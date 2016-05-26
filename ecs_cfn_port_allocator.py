#!/usr/bin/env python2.7
from __future__ import print_function

import json
import boto3
from random import shuffle
from cfnlambda import handler_decorator


@handler_decorator()
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    client = boto3.client('ecs')

    inuse_ports = set()

    cluster = event['ResourceProperties']['ECSCluster']
    from_port = int(event['ResourceProperties']['FromPort'])
    to_port = int(event['ResourceProperties']['ToPort'])

    instances = client.list_container_instances(
        cluster=cluster,
        maxResults=100
    ).get('containerInstanceArns')

    for x in client.describe_container_instances(
        cluster=cluster,
        containerInstances=instances
    ).get('containerInstances'):
        # The current reserved ports are displayed in the remainingResources
        for resource in x['remainingResources']:
            if resource['name'] == 'PORTS':
                for port in resource['stringSetValue']:
                    inuse_ports.add(int(port))

    request_range = [x for x in range(from_port, to_port)]
    shuffle(request_range)
    for p in request_range:
        if p not in inuse_ports:
            return {'Port': p}

    return {'Port': -1}
