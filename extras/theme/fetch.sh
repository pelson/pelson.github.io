# Like a poor-man's bower. I just didn't RTFD.

wget https://github.com/scimusmn/html5-demos/raw/master/js/vendor/html5-3.6-respond-1.1.0.min.js
mv html5-3.6-respond-1.1.0.min.js static/js/


url=https://fortawesome.github.io/Font-Awesome/assets/font-awesome-4.4.0.zip
basename=font-awesome-4.4.0
dir_name=font-awesome

wget $url
mkdir -p static/$dir_name
cd static/$dir_name
unzip -x ../../${basename}.zip
mv $basename/* ./
rm -rf $basename HELP*
rm -rf ../../${basename}.zip


url=https://github.com/twbs/bootstrap/releases/download/v3.3.5/bootstrap-3.3.5-dist.zip
basename=bootstrap-3.3.5-dist

wget $url
mkdir -p static/bootstrap
cd static/bootstrap
unzip -x ../../${basename}.zip
mv $basename/* ./
rm -rf $basename

rm -rf ../../${basename}.zip



