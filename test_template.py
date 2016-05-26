#!/usr/bin/env python

from troposphere import Template, Ref, GetAtt
from troposphere import Parameter, Output
from troposphere.cloudformation import AWSCustomObject



class ECSPortAllocator(AWSCustomObject):
    resource_type = "Custom::ECSPortAllocator"
    props = {
        'ServiceToken': (str, True),
        'ECSCluster': (str, True),
        'FromPort': (str, True),
        'ToPort': (str, True)
    }


t = Template()

t.add_parameter(Parameter(
    'ECSCluster',
    Type='String'
))

t.add_parameter(Parameter(
    'LambdaARN',
    Type='String'
))


t.add_parameter(Parameter(
    'FromPort',
    Type='String'
))


t.add_parameter(Parameter(
    'ToPort',
    Type='String'
))

t.add_resource(ECSPortAllocator(
    'ECSPortAllocator',
    ServiceToken=Ref('LambdaARN'),
    ECSCluster=Ref('ECSCluster'),
    FromPort=Ref('FromPort'),
    ToPort=Ref('ToPort')
))

t.add_output(Output(
    'Port',
    Value=GetAtt('ECSPortAllocator', 'Port')
))

print(t.to_json())
