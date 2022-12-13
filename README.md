# AWS Cloudformation Custom Resource tag fetcher

A custom AWS CloudFormation Resource that returns the tags applied to the current CloudFormation stack.

This is useful if you want to see the tags applied when the current stack was deployed, since this isn't available in the CloudFormation template itself.

Individual tags can be accessed as attributes of the custom resource, see the `Outputs` in [`example-cf.yml`](./example-cf.yml).

**Warning:**
If you update the tags on an existing stack this resource will return the old tags because CloudFormation does not detect that the resource has changed.
You can force a change by adding a dummy property to the stack, e.g. `ForceUpdate: 1`.

## Manual Installation (testing only)

Create a Python lambda called `AwsCfTags` from [`aws_cf_tags.py`](./aws_cf_tags.py) with the default role, then add the `cloudformation:DescribeStacks` permission.

## Automated Installation

Build a CloudFormation template containing the custom resource by running

```
./build_deploy_cf.py > deploy-cf-aws-cf-tags.yml
```

Deploy the template to your AWS account:

```
aws cloudformation deploy --stack-name aws-cf-tags --template-file deploy-cf-aws-cf-tags.yml \
  --capabilities CAPABILITY_NAMED_IAM
```

Or to multiple accounts in the AWS organisation by deploying `deploy-cf-aws-cf-tags.yml` as a StackSet.

## Example

Deploy the example stack [`example-cf.yml`](./example-cf.yml):

```
aws cloudformation deploy --stack-name aws-cf-test --template-file example-cf.yml \
  --tags aaa=123 bbb=Whatever ccc:ddd=sdf
```

The stack outputs should be:

```
aws cloudformation describe-stacks --stack-name aws-cf-test \
  --query 'Stacks[].Outputs' --output text
```

```
CloudFormation stack tags       TagAaa  123
CloudFormation stack tags       TagBbb  Whatever
CloudFormation stack tags       TagCcc  sdf
```
