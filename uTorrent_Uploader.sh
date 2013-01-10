#!/bin/bash

curl -c cookies.txt -u username:password -s http://nas:9090/gui/token.html  | cut -d '>' -f 3 | sed s'/<\/div//' > token.txt; curl -c cookies.txt -b cookies.txt -v -u username:password -F 
torrent_file=@a.torrent -F ADD_FILE_OK= "http://nas:9090/gui/?token=`cat token.txt`&action=add-file"
