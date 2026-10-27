#!/bin/sh
# Construit la ROM dans la langue demandee :  sh tools/topaze/i18n/build_lang.sh fr   (ou en)
# Les textes sources restent en anglais dans le depot ; le francais est applique le temps du build puis retire.
set -e
L=${1:-en}
cd "$(dirname "$0")/../../.."
if [ "$L" = "en" ]; then make -j8 && cp pokefirered.gba Topaze_EN.gba && echo "OK Topaze_EN.gba"; exit 0; fi
trap 'python3 tools/topaze/i18n/lang.py restore; rm -f build/firered/data/maps.o' EXIT
python3 tools/topaze/i18n/lang.py apply "$L"
rm -f build/firered/data/maps.o
make -j8
cp pokefirered.gba "Topaze_$(echo $L | tr a-z A-Z).gba"
echo "OK Topaze_$(echo $L | tr a-z A-Z).gba"
