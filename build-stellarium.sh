#!/bin/bash
# Stellarium Web Engine build script for WSL
set -e

BUILD_DIR="/tmp/stellarium-build"
OUT_DIR="/mnt/d/24history/twz/tianwen-kb/docs/kg/stellarium"

echo "=== Step 1: Install dependencies ==="
sudo apt-get update -qq
sudo apt-get install -y -qq git python3 python3-pip
pip3 install scons

echo "=== Step 2: Install Emscripten SDK ==="
cd /tmp
if [ ! -d emsdk ]; then
  git clone --depth 1 https://github.com/emscripten-core/emsdk.git
fi
cd emsdk
./emsdk install 3.1.45
./emsdk activate 3.1.45
source ./emsdk_env.sh

echo "=== Step 3: Clone Stellarium Web Engine ==="
rm -rf "$BUILD_DIR"
git clone --depth 1 https://github.com/Stellarium/stellarium-web-engine.git "$BUILD_DIR"
cd "$BUILD_DIR"

echo "=== Step 4: Set environment ==="
# EMSCRIPTEN_TOOL_PATH is needed by SConstruct
if [ -z "$EMSCRIPTEN_TOOL_PATH" ]; then
  TOOLS_DIR="$EMSDK/upstream/emscripten/tools"
  if [ -d "$TOOLS_DIR" ]; then
    export EMSCRIPTEN_TOOL_PATH="$TOOLS_DIR"
  else
    echo "Searching for emscripten tools..."
    TOOLS_DIR=$(find "$EMSDK/upstream" -name "site_scons" -type d 2>/dev/null | head -1)
    if [ -n "$TOOLS_DIR" ]; then
      export EMSCRIPTEN_TOOL_PATH=$(dirname "$TOOLS_DIR")
    fi
  fi
fi
echo "EMSCRIPTEN_TOOL_PATH=$EMSCRIPTEN_TOOL_PATH"

echo "=== Step 5: Build (this will take 20-40 minutes) ==="
echo "Start: $(date)"
make js 2>&1 | tee /tmp/build.log
echo "Done: $(date)"

echo "=== Step 6: Copy output ==="
mkdir -p "$OUT_DIR"
cp build/stellarium-web-engine.js "$OUT_DIR/"
cp build/stellarium-web-engine.wasm "$OUT_DIR/"
ls -lh "$OUT_DIR/stellarium-web-engine."*

echo ""
echo "=== BUILD COMPLETE ==="
echo "Files copied to: $OUT_DIR"
