#!/bin/bash

HOME_PATH=`echo ~`
ROOT_PATH=$HOME_PATH/new_blog
CODING_PATH=$HOME_PATH/projects/coding/blog

upload_sitemap(){
    open -a 'Google Chrome' https://www.google.com/ping?sitemap=http://ganjiacheng.cn/sitemap.xml
}

deploy_github(){
    echo "start deploy github"
    cd $ROOT_PATH
    hexo clean
    hexo g
    hexo d
    git add .
    git commit -m "update blog"
    git push origin master
    echo "end deploy github"
    upload_sitemap
}

deploy_coding(){
    echo "start deploy coding"
    cd $ROOT_PATH
    hexo clean
    hexo g
    rm -rf $CODING_PATH/*
    cp -r $ROOT_PATH/public/* $CODING_PATH/
    cd $CODING_PATH
    git add .
    git commit -m "update blog"
    git push origin master
    echo "end deploy coding"
}

deploy_github

# case $1 in 
#     github)
#         deploy_github
#         ;;
#     coding)
#         deploy_coding
#         ;;
#     *)
#         echo "use args github/coding"
#         ;;
# esac