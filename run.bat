git add .
git commit -m "first commit"
git push -u origin master
git push heroku master
heroku ps:scale web=1 --apps=kinozatvbot
heroku open
heroku logs --tail
