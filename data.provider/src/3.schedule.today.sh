#!/bin/bash

if [ -z "$WOLF_DATA_PROVIDER_HOME" ]; then
	echo variable WOLF_DATA_PROVIDER_HOME undefined
        exit 1
fi

if [ -z "$WOLF_HISTDATA_HOME" ]; then
	echo variable WOLF_HISTDATA_HOME undefined
        exit 1
fi

if [ $# -ne 1 ]
then
	echo "usage: $(basename $0) SYMBOL"
	exit 1
fi

CAT=/bin/cat
PYTHON=/usr/bin/python3

PATH_TO_CSV=$WOLF_HISTDATA_HOME
PATH_TO_SRC=$WOLF_DATA_PROVIDER_HOME/src
PATH_TO_LOG=$WOLF_DATA_PROVIDER_HOME/log

CURR_MONTH=$(TZ="EST" date +"%m")
PREV_MONTH=$(TZ="EST" date +"%m" --date="1 month ago")

CURR_DAY=$(TZ="EST" date +"%d")
NEXT_DAY=$(TZ="EST" date +"%d" --date="next day")

CURR_YEAR=$(TZ="EST" date +"%Y")

SYMBOL=$1

${CAT} ${PATH_TO_CSV}/DAT_ASCII_${SYMBOL}_T_${CURR_YEAR}${PREV_MONTH}.csv | grep ^${CURR_YEAR}${PREV_MONTH}${CURR_DAY} | $PYTHON -u $PATH_TO_SRC/2.provider.py $SYMBOL $CURR_MONTH $CURR_DAY >> $PATH_TO_LOG/$SYMBOL.log
