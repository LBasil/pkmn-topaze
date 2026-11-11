#!/bin/sh
cd /home/claude/pkmn-topaze
trap 'python3 tools/topaze/i18n/lang.py restore; python3 tools/topaze/i18n/names.py restore; rm -f build/firered/data/maps.o' EXIT
python3 tools/topaze/i18n/lang.py apply fr
python3 tools/topaze/i18n/names.py apply fr
rm -f build/firered/data/maps.o
python3 /tmp/gx/mkdbg2.py
