# AWS Cloudformation Custom Resource tag fetcher

A custom AWS CloudFormation Resource that returns the tags applied to the current CloudFormation stack.

This is useful if you want to see the tags applied when the current stack was deployed, since this isn't available in the CloudFormation template itself.

Individual tags can be accessed as attributes of the custom resource, see the `Outputs` in [`example-cf.yml`](./example-cf.yml).

**Warning:**
If you update the tags on an existing stack this resource will return the old tags because CloudFormation does not detect that the resource has changed.
You can force a change by adding a dummy property to the stack, e.g. `ForceUpdate: 1`.

## Installation

TODO: create a CloudFormation template so this can be deployed as a Stackset across multiple AWS accounts in an organisation.

Currently you must manually create a Python lambda called `aws_cf_tags` from [`aws_cf_tags.py`](./aws_cf_tags_lambda/aws_cf_tags.py) with the default role, then add the `cloudformation:DescribeStacks` permission.

## Example

Deploy the example stack:

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
