#!/bin/bash

set -x

rm -rf package_dir
mkdir package_dir
cp ecs_cfn_port_allocator.py package_dir
pip2.7 install cfnlambda -t package_dir
pushd package_dir
zip -r lambda_port_allocator.zip .
popd
mv package_dir/lambda_port_allocator.zip .

