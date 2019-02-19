#!/bin/bash

# Auto compile py file to pyc
# Author Harvey


# py File to pyc main work
function py2pyc_work(){
    local COMPILE_DIR=$1;

    # Compile File
    python3.6 -m compileall $COMPILE_DIR;

    # File Move
    mv $COMPILE_DIR/__pycache__/*.pyc $COMPILE_DIR;

    # File rename
    rename -v -f 's/.cpython-36//' $COMPILE_DIR/*.pyc;

    # Delete dir  __pycache__
    rm -r $COMPILE_DIR/__pycache__;

    # Delete source file
    rm $COMPILE_DIR/*.py;
}

function py2pyc(){
    local COMPILE_DIR=$1;
    echo "!!!!!!!"${COMPILE_DIR}

    # 是否存在py文件才去编译，但是加上这个判断就会报参数太多，还没想到办法解决
    #if [ -e $COMPILE_DIR/*.py -eq 0 ];
    #then
        py2pyc_work $COMPILE_DIR;
    #fi

    for ITEM in $(ls $COMPILE_DIR);
    do
        local NEW_DIR=${COMPILE_DIR}"/"$ITEM;
        echo $NEW_DIR;
        if isDir $NEW_DIR;
        then
            py2pyc $NEW_DIR;
        fi
    done
}

# Judge is Dir or not
function isDir(){
    if [ -d $1 ];
    then
        return 0;
    else
        return 1;
    fi
}

function isRootDir(){
    local IN_DIR=$1;
    local STR=${IN_DIR:0:1}
    if [ $STR == "/" ];
    then
        return 0;
    else
        return 1;
    fi
}


# Main
INIT_DIR=$( pwd -P )
if [ "$1" ];
then

    if [ $1 == "-h" ];
    then
        echo "参数为寻求帮助";
        exit;
    fi

    if isDir $1;
    then
        IN_DIR=$1;
        DIR_LEN=${#IN_DIR};
        STR=${IN_DIR:$DIR_LEN-1:$DIR_LEN};

        if isRootDir $1;
        then
            echo "root";
            if [ $STR == "/" ];
            then
                IN_DIR_NEW=${IN_DIR:0:$DIR_LEN-1};
            else
                IN_DIR_NEW=$1;
            fi
            py2pyc $IN_DIR_NEW;

        else
            echo "not root";
            if [ $STR == "/" ];
            then
            echo "/";
                IN_DIR_TMP=${IN_DIR:1:$DIR_LEN-2};
            else
                IN_DIR_TMP=${IN_DIR:1:$DIR_LEN-1};
            fi

            INIT_DIR_NEW=${INIT_DIR}${IN_DIR_TMP};
            py2pyc $INIT_DIR_NEW;
        fi

    else
        echo "传入参数不是文件夹";
    fi

# 没有传入参数，直接从本文件所在文件夹开始运行
else
    py2pyc $INIT_DIR;
fi


echo "COMPILE DONE !! ";