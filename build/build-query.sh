if [ -e sira-query ];then
rm -rf sira-query
fi
if [ -e build ];then
rm -rf build
fi
if [ -e dist ];then
rm -rf dist
fi
python -m PyInstaller sira-query.spec
mv dist/sira-query sira-query
rm -rf build
rm -rf dist