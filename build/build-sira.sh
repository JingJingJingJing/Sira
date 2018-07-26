if [ -e sira ];then
rm -rf sira
fi
if [ -e build ];then
rm -rf build
fi
if [ -e dist ];then
rm -rf dist
fi
python -m PyInstaller sira.spec
mv dist/sira sira
rm -rf build
rm -rf dist