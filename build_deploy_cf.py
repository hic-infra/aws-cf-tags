#!/usr/bin/env python

with open("deploy-cf.yml") as f:
    d = f.read().splitlines()

with open("aws_cf_tags.py") as f:
    py = f.read().splitlines()


marker = "# aws_cf_tags.py"

for n, line in enumerate(d):
    if line.strip() == marker:
        indent = line.find(marker)
        break

py_indented = [(" " * indent + line) for line in py]

template = d[: (n + 1)] + py_indented + d[(n + 1) :]
print("\n".join(template))
