if [ -e build ];then
echo "1"
rm -rf build
fi
if [ -e dist ];then
echo "2"
rm -rf dist
fi
python -m PyInstaller sira-query.spec
mv dist/sira-query sira-query
rm -rf build
rm -rf dist