#!/bin/bash

set -euo pipefail


OPENAPI_URL="${OPENAPI_URL:-https://racinghub.net/api/v1/openapi.json}"
GENERATOR_VERSION="${GENERATOR_VERSION:-7.13.0}"
GENERATOR_JAR="openapi-generator-cli.jar"

NODE_OUTPUT="clients/node"
NODE_PACKAGE_NAME="${NODE_PACKAGE_NAME:-@racinghub/client}"

echo "Fetching OpenAPI spec..."
curl -sSL "$OPENAPI_URL" -o openapi.json

VERSION=$(jq -r '.info.version' openapi.json)

if [[ -z "$VERSION" || "$VERSION" == "null" ]]; then
  echo "❌ Could not read version from OpenAPI spec"
  exit 1
fi

echo "Using API version: $VERSION"

echo "Downloading OpenAPI Generator CLI..."
curl -sSL \
  "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/${GENERATOR_VERSION}/openapi-generator-cli-${GENERATOR_VERSION}.jar" \
  -o "$GENERATOR_JAR"


echo "Generating Node SDK..."

rm -rf "$NODE_OUTPUT"

java -jar "$GENERATOR_JAR" generate \
  -i openapi.json \
  -g typescript-fetch \
  -o "$NODE_OUTPUT" \
  --additional-properties=npmName="$NODE_PACKAGE_NAME",npmVersion="$VERSION",supportsES6=true
#
echo "Publishing to npm..."

cd "$NODE_OUTPUT"

echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN:-}" > ~/.npmrc

npm install

if npm publish 2>&1 | tee /tmp/npm_publish.log; then
  echo "✅ Published successfully"
else
  if grep -q "previously published" /tmp/npm_publish.log; then
    echo "⚠️ Version already exists — skipping publish"
  else
    echo "❌ npm publish failed"
    exit 1
  fi
fi

cd - >/dev/null

echo "🎉 Done!"
