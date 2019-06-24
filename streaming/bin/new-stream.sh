#!/bin/bash
# 1. Copy default/ content to another directory
# 2. Replace path in configuration and playlist: from default/ to newpath/
file=$(test -L "$0" && readlink "$0" || echo "$0")

echo "Name of strem (slug)"
read -r name

name="test"
dir_from="$(pwd $0)/default/"
dir_to="${dir_from/default/$name}"

cp -R $dir_from/ $dir_to
find $dir_to -name '*.liq' -type f -print0  | xargs -0 sed -i._back "s#${dir_from}#${dir_to}#g"
find $dir_to -name '*.lst' -type f -print0  | xargs -0 sed -i._back "s#${dir_from}#${dir_to}#g"
find $dir_to -name '*._back' -type f | xargs rm 
