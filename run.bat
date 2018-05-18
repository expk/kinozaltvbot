git add .
git commit -m "first commit"
git push -u origin master
git push heroku master
heroku ps:scale web=1 --apps=shrouded-tor-71280
heroku open
heroku logs --tail
