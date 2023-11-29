git commit -a -m "$1"
git pull --rebase
git push origin main
cp results/lt/dict.txt results/lt/dict.old
#cd morfologik-lt
#./extrau-novetats.sh