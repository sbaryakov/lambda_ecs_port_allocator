#!/usr/bin/env python
from troposphere import GetAtt, Template, Ref, Output, Parameter, AWSObject
from troposphere.awslambda import Code, Function
from troposphere.iam import Role
from troposphere.iam import Policy as IAM_Policy
from awacs.aws import Policy, Allow, Action, Principal, Statement


template = Template()

s3_bucket_param = Parameter(
    'S3BucketName',
    Type='String',
    Description='The bucket where the lambda code is uploaded'
)

s3_key_param = Parameter(
    'S3KeyName',
    Type='String',
    Description='The full name of the s3 key containing the lambda zip'
)

assume_role_policy_document = Policy(
    Statement=[
        Statement(
            Effect=Allow,
            Action=[Action('sts', 'AssumeRole')],
            Principal=Principal('Service', 'lambda.amazonaws.com'),
        )
    ]
)

lambda_policy = IAM_Policy(
    PolicyName='ECSPortAllocator',
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Action=[
                    Action('ecs', 'DescribeClusters'),
                    Action('ecs', 'DescribeContainerInstances'),
                    Action('ecs', 'ListContainerInstances'),
                ],
                Resource=['*']
            ),
            Statement(
                Effect=Allow,
                Action=[
                    Action('logs', 'CreateLogGroup'),
                    Action('logs', 'CreateLogStream'),
                    Action('logs', 'PutLogEvents'),
                    Action('logs', 'DeleteLogGroup')
                ],
                Resource=['arn:aws:logs:us-east-1:054713022081:log-group:/aws/lambda/*']
            )
        ]

    )
)

lambda_role = Role(
    'ECSPortAllocatorLambdaRole',
    Path='/',
    AssumeRolePolicyDocument=assume_role_policy_document,
    Policies=[lambda_policy]
)


ecs_port_allocator = Function(
    "ECSPortAllocator",
    Handler="ecs_cfn_port_allocator.lambda_handler",
    Role=GetAtt(lambda_role, "Arn"),
    Code=Code(
        S3Bucket=Ref(s3_bucket_param),
        S3Key=Ref(s3_key_param),
    ),
    Runtime="python2.7",
    Timeout="25",
)


ecs_port_allocator_output = Output(
    'ECSPortAllocatorLambda',
    Description='ECSPortAllocatorLambda',
    Value=GetAtt(ecs_port_allocator, 'Arn')
)

template.add_parameter(s3_bucket_param)
template.add_parameter(s3_key_param)
template.add_resource(lambda_role)
template.add_resource(ecs_port_allocator)
template.add_output(ecs_port_allocator_output)

if __name__ == '__main__':
    print(template.to_json())
