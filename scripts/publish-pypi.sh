#!/bin/bash

set -euo pipefail

OPENAPI_URL="${OPENAPI_URL:-https://racinghub.net/api/v1/openapi.json}"
GENERATOR_VERSION="${GENERATOR_VERSION:-7.13.0}"
GENERATOR_JAR="openapi-generator-cli.jar"
PYTHON_OUTPUT="clients/python"
PYTHON_PACKAGE_NAME="${PYTHON_PACKAGE_NAME:-racinghub_client}"

curl -sSL "$OPENAPI_URL" -o openapi.json
VERSION=$(jq -r '.info.version' openapi.json)
if [[ -z "$VERSION" || "$VERSION" == "null" ]]; then
  echo "❌ Could not read version from OpenAPI spec"
  exit 1
fi

curl -sSL "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${GENERATOR_VERSION}/openapi-generator-cli-${GENERATOR_VERSION}.jar" -o "$GENERATOR_JAR"

rm -rf "$PYTHON_OUTPUT"
java -jar "$GENERATOR_JAR" generate -i openapi.json -g python -o "$PYTHON_OUTPUT" --additional-properties=packageName="$PYTHON_PACKAGE_NAME",packageVersion="$VERSION"

cd "$PYTHON_OUTPUT"
python -m pip install --upgrade build twine
python -m build

TWINE_USERNAME="__token__" TWINE_PASSWORD="${PYPI_TOKEN:-}" twine upload dist/* 2>&1 | tee /tmp/pypi_publish.log || {
  if grep -q "File already exists" /tmp/pypi_publish.log; then
    echo "⚠️ Version already exists — skipping"
    exit 0
  else
    echo "❌ PyPI publish failed"
    exit 1
  fi
}

cd - >/dev/null
echo "🎉 Done!"
