from secrets import *
import tweepy
import time
import datetime
import requests
import os
    
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)
tweet_id = []
howwto = 'bot teti18 edisi twitter lur\ncara pakenya sebutkan keywordnya trus tanya aja mau jadwal hari ini, besok atau jadwal lengkao\nselain itu kalo kamu follow, bakal dikasih daily reminder h-1 dan hari h uas lho!\nayo yg kesepian gak ada yg ngingetin uas, dari pada lupa mending follow'

def get_mention():
    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        try:
            if(tweet.id not in tweet_id):
                api.update_status('@%s bro kalo mau nanyak pake "teti2018"' % (tweet.user.screen_name), tweet.id)
                tweet_id.append(tweet.id)
        except Exception as identifier:
            print(identifier)
            tweet_id.append(tweet.id)
    waiting(300) 

def get_tweet_keyword():
    tweets = api.search(q="teti2018")
    for tweet in tweets:
        try:
            if('besok' in tweet.text.split() and tweet.id not in tweet_id):
                tweet_schedule('besok', tweet.user.screen_name, tweet.id)
                tweet_id.append(tweet.id)
            elif('lusa' in tweet.text.split() and tweet.id not in tweet_id):
                tweet_schedule('lusa', tweet.user.screen_name, tweet.id)
                tweet_id.append(tweet.id)
            elif('ini' in tweet.text.split() and tweet.id not in tweet_id):
                tweet_schedule('hari ini', tweet.user.screen_name, tweet.id)
                tweet_id.append(tweet.id)
            elif('lengkap' in tweet.text.split() and tweet.id not in tweet_id):
                tweet_schedule_daily(tweet.user.screen_name, tweet.id) 
                tweet_id.append(tweet.id)
            elif(tweet.id not in tweet_id):
                api.update_status('@%s %s' % (tweet.user.screen_name, howwto), tweet.id)
                tweet_id.append(tweet.id)
        except Exception as identifier:
            print(identifier)
            tweet_id.append(tweet.id)    

def tweet_schedule(question, username, reply_id):
    if(question == 'besok'):    
        try:
            tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
            tomorrow = str(tomorrow).split()[0]
            tomorrow = datetime.datetime.strptime(tomorrow, '%Y-%m-%d')
            print('Besok uasnya ' + str(jadwalUas[tomorrow]) + ' Bro')
            api.update_status('@%s Besok uasnya ' + str(jadwalUas[tomorrow]) + ' Bro' % username, reply_id)
        except Exception as identifier:
            api.update_status('@%s Wah besok gak ada UAS bro' % username, reply_id)
            print(identifier)

    elif(question == 'lusa'):
        try:
            tomorrow = datetime.datetime.today() + datetime.timedelta(days=2)
            tomorrow = str(tomorrow).split()[0]
            tomorrow = datetime.datetime.strptime(tomorrow, '%Y-%m-%d')
            api.update_status('@%s Lusa uasnya %s Bro' % (username, jadwalUas[tomorrow]), reply_id)
            print('@%s Lusa uasnya %s Bro' % (username, jadwalUas[tomorrow]), reply_id)
        except Exception as identifier:
            api.update_status('@%s Wah lusa gak ada UAS bro' % username, reply_id)
            print(identifier)
    
    elif(question == 'hari ini'):
        try:
            tomorrow = datetime.datetime.today()
            tomorrow = str(tomorrow).split()[0]
            tomorrow = datetime.datetime.strptime(tomorrow, '%Y-%m-%d')
            api.update_status('@%s Hari ini uasnya %s Bro' % (username, jadwalUas[tomorrow]), reply_id)
            print('@%s Hari ini uasnya %s Bro' % (username, jadwalUas[tomorrow]), reply_id)
        except Exception as identifier:
            api.update_status('@%s Wah hari ini gak ada UAS bro' % username, reply_id)
            print(identifier)

def tweet_schedule_daily(username, reply_id):
    message = 'Inget bro\nSenin tgl 9 Basdat jam 1 \nRabu tgl 11 SO / OS jam 10 \nJumat tgl 13 SG jam 7.30 \nSabtu tgl 15 KWN jam 11.30\nSenin tgl 16 Jarkomdat jam 1\nSelasa tgl 17 Matdislog jam 10\nRabu tgl 18 ISIS jam 7.30\nKamis tgl 19 Sismik jam 1\nJumat tgl 20 Pemsim jam 8.30'
    api.update_status('@%s %s' % (username, message), reply_id)

def daily_uas_reminder(date, day):
    ids = get_follower_lists()
    if(day == 'today'):
        for id in ids:
            username = api.get_user(id)
            api.update_status('@%s Jangan lupa hari ini UAS %s Bro' % (username.screen_name, jadwalUas[date]))
            print('Daily Reminder Sent!')
            #print('@%s Jangan lupa hari ini UAS %s Bro' % (username.screen_name, jadwalUas[date]))
            time.sleep(2)
    elif(day == 'tomorrow'):
        for id in ids:
            username = api.get_user(id)
            api.update_status('@%s Jangan lupa besok UAS %s Bro' % (username.screen_name, jadwalUas[date]))
            print('Tomorrow Reminder Sent!')
            #print('@%s Jangan lupa besok UAS %s Bro' % (username.screen_name, jadwalUas[date]))
            time.sleep(2)

def get_follower_lists():
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name='ReminderUas').pages():
        ids.extend(page)
        time.sleep(5)
    return ids
    
def img_howto(tweet):
    filename = 'howto.jpg'
    url = 'https://ton.twitter.com/1.1/ton/data/dm/1203493212544847876/1203493202734354433/WcHBwfar.jpg:medium'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    api.update_with_media(filename ,status='@%s %s' % (tweet.user.screen_name, howwto), in_reply_to_status_id=tweet.id)
    os.remove(filename)

def waiting(second):
    for i in range(second):
        print("waiting... %i seconds left" % int(second - i))
        time.sleep(1)

while True:
    print("Searching for tweet")
    get_tweet_keyword()
    waiting(15)
    date = str(datetime.datetime.today()).split()[0]
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    tomorrow = str(datetime.datetime.today() + datetime.timedelta(days=1)).split()[0]
    tomorrow = datetime.datetime.strptime(tomorrow, "%Y-%m-%d")
    if(date in jadwalUas.keys() and datetime.datetime.now().strftime("%H-%M-%S") == '05-00-00'):
        daily_uas_reminder(date, 'today')
    if(tomorrow in jadwalUas.keys() and datetime.datetime.now().strftime("%H-%M-%S") == '20-00-00'):
        daily_uas_reminder(tomorrow, 'tomorrow')
