#!/bin/bash

VERSION=0.0.10

BASE_PATH=$(cd `dirname $0`; cd ..; pwd)


POM=$BASE_PATH/pom.xml
POM_VERSION=`awk '/<version>[^<]+<\/version>/{gsub(/<version>|<\/version>/,"",$1);print $1;exit;}' $POM`

PARAM=$1

AUTO_VERSION=false

PROJECT_ID=

PROJECT=

TOKEN=

TARGET_FILE=

URL_UPLOAD=

URL_RELEASE=


function usage() {
    echo "Yegoo Co.ltd"
    echo "Deploy version $VERSION"
    echo "Usage: deploy [version(x.x.x.x)]"
    if [ "$1" != "" ]; then
        echo -e $1
    fi
    exit 1
}

function newVersionFromPom() {
    LEFT_VERSION=$1

    OV=${LEFT_VERSION%%.*}
    LEFT_VERSION=${LEFT_VERSION#*$OV.}

    TV=${LEFT_VERSION%%.*}
    LEFT_VERSION=${LEFT_VERSION#*$TV.}

    SV=${LEFT_VERSION%%.*}
    LEFT_VERSION=${LEFT_VERSION#*$SV.}

    FVT=${LEFT_VERSION%%.*}
    FV=${FVT%-*}
    echo $OV.$TV.$SV.$(($FV+1))-SNAPSHOT
}

BANNER='
 _____             _             
|  __ \           | |            
| |  | | ___ _ __ | | ___  _   _ 
| |  | |/ _ \  _ \| |/ _ \| | | |
| |__| |  __/ |_) | | (_) | |_| |
|_____/ \___| .__/|_|\___/ \__, |
            | |             __/ |
            |_|            |___/ 
'

echo -e "$BANNER"


if [ "$PARAM" == "rollback" ]; then
    echo "Rollback "
    mvn versions:revert -f $POM
    exit 0
fi

if [ "$PARAM" == "" ]; then
    PARAM=$POM_VERSION
    AUTO_VERSION=true
fi

if [[ "$PARAM" =~ ^[0-9]+.[0-9]+.[0-9]+.[0-9]+(-SNAPSHOT)?$ ]]; then
    OLD_VERSION=${PARAM%-*}
    NEW_VERSION=`newVersionFromPom $OLD_VERSION`
    read -p "Are you sure to continue (release version $OLD_VERSION, new version $NEW_VERSION)? [Y/N]" yesOrNo
    case $yesOrNo in
        [yY]*)
            echo "Update release version $OLD_VERSION"
            mvn versions:set -DnewVersion=$OLD_VERSION -f $POM
            mvn package -DskipTests -f $POM
            if [[ $? -eq '0' ]]; then
                ret=$(curl -s --request POST --header "PRIVATE-TOKEN: $TOKEN" --form "file=@$TARGET_FILE" $URL_UPLOAD)
                markdown1=${ret#*markdown\":\"}
                msg=${markdown1:0:-2}
                git tag -a v$OLD_VERSION -m "$OLD_VERSION"
                git push origin v$OLD_VERSION
                if [[ $? -eq '0' ]]; then
                    git tag -d v$OLD_VERSION
                    echo "Update next version $NEW_VERSION"
                    mvn versions:set -DnewVersion=$NEW_VERSION -f $POM
                    mvn versions:commit -f $POM
                else
                    mvn versions:revert -f $POM
                fi
                data="# Release v$OLD_VERSION
$msg"
                ret=$(curl -s --request POST --header "PRIVATE-TOKEN: $TOKEN" --data "description=$data" $URL_RELEASE)
            else
                 mvn versions:revert -f $POM
            fi
            ;;
        [nN]*)
            echo "exit"
            exit
            ;;
        *)
            echo "Just enter Y or N, please."
            exit
            ;;
    esac
else
    if $AUTO_VERSION; then
        usage "pom version error, you must init pom version x.x.x.x\nex: deploy.sh 1.0.0.1"
    else
        usage "input version error"
    fi
fi
