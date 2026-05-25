#!/usr/bin/env fish
# On NTFS partition, run this as "fish build-linux.fish", not "./build-linux.fish"

set BUILD_PATH ~/Applications/tmp/vocabsieve

rm -rf  $BUILD_PATH
mkdir -p $BUILD_PATH
cp -r (pwd)/* $BUILD_PATH
cd $BUILD_PATH

python3 -m venv .venv
source .venv/bin/activate.fish

pip install wheel
pip install -r requirements.txt
pip install cx_freeze
pip install python-appimage

cp vocabsieve.{desktop,png} recipe/
echo $(pwd) | cat - recipe/requirements.txt > tmpfile && mv tmpfile recipe/requirements.txt
python -m python_appimage build app -p 3.11 recipe
mv VocabSieve-x86_64.AppImage ~/Applications/VocabSieve-v$(grep version setup.cfg | awk '{print $3}')-linux-amd64.AppImage

deactivate

rm -rf  $BUILD_PATH