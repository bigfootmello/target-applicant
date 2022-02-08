#!/bin/bash

######################################################################################################
# Program:      start_app_service.sh
# Project:      Try to work for Target Tech
# Purpose:      Script to start some application service
# Owner:        D. Folks
# Developer:    D. Folks
# Create Date:  02/02/2022
# Comments:     Service account is the only user that can run this script.
#               Kill existing process if being restarted
#               Older files are removed after 99 days
# Exit Codes:   ERROR SH_01: Bad UserId
#               ERROR SH_02: Script running from wrong DIR
#                   (Example: Production running from Develop)
# Revisions:    D. Folks - <DATE> - I changed something
######################################################################################################

#############################
### Environment Setup
#############################
FILE_NAME="app-service"
HOST=$(hostname -s)
DIR=${PWD###*/}         # Get current dir name only
BASEDIR=$(dirname $0) 
SCRIPT=$(basename $0 .sh)
LOG_FILE=${SCRIPT}.log 
LOG_LOCATION=${BASEDIR}/logs
TIMESTAMP=`date +%y-%m-%dT%H%M%S`   # Example: 22-02-17T134355
LOG_HIST_FILE="${SCRIPT}"_"${TIMESTAMP}".log
JAR_LOCATION=/home/service_account/apps/${DIR}/bin
#############################
### Environment End
#############################

#############################
### Functions Setup
#############################
function log_msg() {
    echo -e "\n[`date +%Y-%m-%d\ %T`] $1" >> ${LOG_LOCATION}/${LOG_FILE}
}
#############################
### Functions Setup
#############################

#############################
### MAIN
#############################

### Verify User ###
UserId=`id -u`
if [[ $${UserId} -ne "00000" ]]; then
    log_msg "ERROR SH_01: Bad user id. Script need to run as the service account. Exiting..."
    exit 1
fi

log_msg "Starting service $FILENAME on $HOST $(date)"
cd $(BASEDIR)

### Save logs and remove files >=99 days ###
mkdir -p ${LOG_LOCATION}/log_hist 2>dev/null
mv ${LOG_LOCATION}/${LOG_FILE} ${LOG_LOCATION}/log_hist/${LOG_HIST_FILE} 2>/dev/null
find logs -maxdepth 2 -mtime +99 -type f -name "${SCRIPT}*" -delete 2>/dev/null

### Verify script matches env ###
if [[ $DIR="DEV" && $HOST="known-dev-host" ]] || [[ $DIR="TST" && $HOST="known-test-host" ]] || [[ $DIR="PRD" && $HOST="known-prod-host" ]]; then
    log_msg "Executing script in $DIR as found on $HOST"
else
    log_msg "ERROR SH_02: Script in $DIR should not be run on $HOST. Exiting..."
    exit 2
fi

### Kill service if running ###
MyPID=`ps -ef | grep "java -jar ${JAR_LOCATION}/${FILENAME}" | grep -v grep | awk '{print $2}'`

while [ "${MyPID}" != 0 -a "$MyPID" != "" ]; do
    log_msg "Out with the old PID: $MyPID"
    kill -9 "$MyPID"
    sync
    sleep 2
    MyPID=`ps -ef | grep "java -jar ${JAR_LOCATION}/ ${FILENAME}" | grep -v grep | awk '{print $2}'`
done

### Run Application ###
nohup java -jar ${JAR_LOCATION}/${FILENAME} -Xms1024m -Xmx1024m > ${LOG_LOCATION}/${LOG_FILE} 2>&1 &

#############################
### Script End
#############################