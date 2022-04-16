# git repo chain 
```
┌────────────────────┐         ┌─────────────────────┐         ┌────────────────────┐
│                    │         │                     │         │                    │
│ repo DIR_ORIGINAL  ◄─────────► repo DIR_LOCAL      ◄─────────► repo DIR_LOCAL_EXT │
│      bare          │         │                     │         │                    │
└────────────────────┘         └─────────────────────┘         └────────────────────┘
```

## repo-original: init
```sh
REPO_NAME=local-git
DIR_ORIGINAL=/home/projects/temp/$REPO_NAME
mkdir -p $DIR_ORIGINAL
cd $DIR_ORIGINAL
git init --bare 
```

## repo-local: clone
```sh
DIR_LOCAL=/home/projects/temp/repo-local
mkdir -p $DIR_LOCAL
cd $DIR_LOCAL
git clone file://$DIR_LOCAL/$REPO_NAME
cd $DIR_LOCAL/$REPO_NAME

# for avoiding error when someone push currently active branch
git config --local receive.denyCurrentBranch updateInstead

# 2. before push to original
cd $DIR_LOCAL/$REPO_NAME
git reset --soft origin/master; git add *; git commit --message 'commits from repo-local-extend'
```


# repo-local-extend: clone
```sh
DIR_LOCAL_EXT=/home/projects/temp/repo-local-extend
mkdir -p $DIR_LOCAL_EXT
cd  $DIR_LOCAL_EXT

git clone file://$DIR_LOCAL/$REPO_NAME

# 1. make a changes 
cd $DIR_LOCAL_EXT/$REPO_NAME
touch 1.txt
git add; git commit --message 'ext repo changes'; git push
# ask to change the branch in DIR_LOCAL in case of any errors
```