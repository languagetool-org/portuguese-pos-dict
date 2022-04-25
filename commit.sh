git commit -a -m "$1"
git pull --rebase
git push origin main
cp results/lt/diccionari.txt results/lt/diccionari.old
#cd morfologik-lt
#./extrau-novetats.sh