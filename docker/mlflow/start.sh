#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./artifacts \
    --host 0.0.0.0 \
    --port 80 