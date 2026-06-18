#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Apply AfyaConnect branding to the Tryton SAO web client.

set -euo pipefail

SAO_ROOT="${1:-/home/node/sao}"
BRAND_DIR="$(cd "$(dirname "$0")" && pwd)"

cp "${BRAND_DIR}/custom.css" "${SAO_ROOT}/custom.css"
cp "${BRAND_DIR}/custom.js" "${SAO_ROOT}/custom.js"
cp "${BRAND_DIR}/images/afyaconnect-icon.svg" "${SAO_ROOT}/images/afyaconnect-icon.svg"

sed -i 's/<title>Tryton<\/title>/<title>AfyaConnect<\/title>/' "${SAO_ROOT}/index.html"
sed -i 's/theme="default"/theme="afyaconnect"/' "${SAO_ROOT}/index.html"
sed -i 's/images\/tryton-icon.png/images\/afyaconnect-icon.svg/' "${SAO_ROOT}/index.html"

echo "AfyaConnect SAO branding applied to ${SAO_ROOT}"
