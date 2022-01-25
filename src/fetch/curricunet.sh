#! /usr/bin/bash

# Programs
wget -i data/curricunet-urls -nc -P data/curricunet

# Index of all CS Courses
for i in  0 1 2 3 ; do 

    html=data/curricunet/cs_$i.html
    json=data/curricunet/cs_$i.json

    test -f $json && continue

    POST="PublicSearchViewModel.KeywordSearch=&PublicSearchViewModel.SerializedSelectedClientIds=null&PublicSearchViewModel.SerializedSelectedClientEntityTypeIds=%5B1%5D&PublicSearchViewModel.SerializedSelectedClientEntitySubTypeIds=null&PublicSearchViewModel.SerializedSelectedSubjectIds=%5B38%2C162%5D&PublicSearchViewModel.SerializedSelectedClientStatusIds=%5B%7B%22Id1%22%3A1%2C%22Id2%22%3A1%7D%5D&PublicSearchViewModel.SerializedSelectedAwardTypeIds=%5B%5D&PublicSearchViewModel.SerializedSelectedOrganizationEntityIds=%5B%5D&PublicSearchViewModel.Page=$i"
    wget -O $html --post-data="$POST" https://santamonica.curricunet.com/Account/Search

    grep -Po '(?<=data-model=")[^"]*' $html | sed 's/&quot;/"/g' >$json

done


# CS Courses
jq -r '.PublicSearch.SearchResults[].Reports[0].url ' data/curricunet/cs_*.json | \
    sed 's_^_https://santamonica.curricunet.com_' | \
    wget -i - -nc -P data/curricunet

find data/curricunet -name '*reportId=5' -exec python3 src/fetch/etl_course.py '{}' \;
