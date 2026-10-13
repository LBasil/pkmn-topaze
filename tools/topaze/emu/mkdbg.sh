#!/bin/sh
# Construit /tmp/gx/dbg.gba (ROM de debug) puis restaure les sources et la ROM normale.
set -e
cd "$(dirname "$0")/../../.."
git apply tools/topaze/emu/debug.patch
make -j8 firered >/dev/null 2>&1 || { git apply -R tools/topaze/emu/debug.patch; exit 1; }
mkdir -p /tmp/gx && cp pokefirered.gba /tmp/gx/dbg.gba
git apply -R tools/topaze/emu/debug.patch
make -j8 firered >/dev/null 2>&1
echo "dbg.gba prête"
