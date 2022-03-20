#! /usr/bin/bash

wget -nc https://www.onetcenter.org/dl_files/database/db_26_2_mysql.zip -P data

unzip -n data/db_26_2_mysql.zip -d data/onet_26_2

for f in $(find data/onet_26_2 -name '*.sql' | sort); do
    echo $f...
    sqlite3 /tmp/onet.sqlite3 ".read $f"
done

 mv /tmp/onet.sqlite3 data/


#function extract_href() {
#
#    jq -r '[ .. | objects | with_entries(select(.key | endswith("href"))) | select(. != {}) ][].href' $*
#}
#
#
#wget -i - --header="$(<.onetauth)" --header="Accept: application/json"  -nc -x -P data/onet --default-page=obj.json
#
#
#for f in "$(find data/onet -type f)" ; do
#    extract_href $f >> data/onet_urls
#done
#
#sort -u data/onet_urls > data/onet_urls_2
#mv data/onet_urls_2 data/onet_urls

