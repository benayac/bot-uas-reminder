from secrets import *
import tweepy
import time
import datetime
    
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)
tweet_id = []

def get_mention():
    for tweet in tweepy.Cursor(api.mentions_timeline).items():
        if('besok' in tweet.text.split() and tweet.id not in tweet_id):
            tweet_schedule('besok', tweet.user.screen_name, tweet.id)
            tweet_id.append(tweet.id)
        elif('lusa' in tweet.text.split() and tweet.id not in tweet_id):
            tweet_schedule('lusa', tweet.user.screen_name, tweet.id)
            tweet_id.append(tweet.id)
        time.sleep(10)  

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

def tweet_schedule_daily():
    print('Ingat UAS!')
    print('Senin tgl 9 Basdat jam 1 \nRabu tgl 11 SO / OS jam 10 \nJumat tgl 13 SG jam 7.30 \nSabtu tgl 15 KWN jam 11.30\nSenin tgl 16 Jarkomdat jam 1\nSelasa tgl 17 Matdislog jam 10\nRabu tgl 18 ISIS jam 7.30\nKamis tgl 19 Sismik jam 1\nJumat tgl 20 Pemsim jam 8.30')

while True:
    get_mention()