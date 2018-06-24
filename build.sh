#!/usr/bin/env bash
#
DIR1=/var/www/cgi-bin
DIR2=/var/www/html/contacts
cp *.py ${DIR1}/ 
cp *.vcf ${DIR1}/
mkdir -p ${DIR2}

