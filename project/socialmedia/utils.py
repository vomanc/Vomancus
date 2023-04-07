""" Twitter API request script """
import tweepy


def tweet_parse(api, count, since_id=None):
    """ Get Twitter API parse """
    try:
        public_tweets = api.home_timeline(
            count=count, since_id=since_id,
            tweet_mode="extended",
            # media=True,
            include_entities=True)
    except tweepy.errors.TooManyRequests:
        return None, 'Rate limit exceeded'
    except tweepy.errors.Unauthorized:
        return None, 'Invalid API key'

    all_tweets = []
    media_list = []

    for tweet in public_tweets:
        user_class = tweet.user
        user = str(user_class._json['name'])
        screen_name = str(user_class._json['screen_name'])
        tweet_text = tweet.full_text.split('https')

        try:
            preview_url = tweet._json['entities']['urls'][0]['expanded_url']
            if preview_url.count('https:') > 1 or preview_url.count('http') > 1 \
                    or '<script' in preview_url:
                preview_url = None
        except IndexError:
            preview_url = None

        try:
            media_url = tweet.extended_entities['media'][0]['video_info']['variants'][0]['url']
            if '/pl/' in media_url:
                media_url = tweet.extended_entities['media'][0]['video_info']['variants'][1]['url']
            if '/pl/' in media_url:
                media_url = tweet.extended_entities['media'][0]['video_info']['variants'][2]['url']
            if media_url.count('https:') > 1 or media_url.count('http') > 1 \
                    or '<script' in media_url:
                media_url = None
            else:
                media_list.append({str(tweet.id): media_url})
        except (AttributeError, KeyError):
            try:
                for i in range(4):
                    try:
                        img = tweet.extended_entities['media'][i]['media_url_https']
                        media_list.append({str(tweet.id): img})
                    except IndexError:
                        break
            except AttributeError:
                pass

        all_tweets.append({
            'tweet_id': str(tweet.id),
            'screen_name': '@' + screen_name.replace('"', "'"),
            'user': user.replace('"', "'"),
            'tweet_text': tweet_text[0].strip().replace('"', "'"),
            'media_url': [],
            'preview_url': preview_url
            })

    all_tweets.reverse()
    return all_tweets, media_list


def twitter_api(api_keys, count):
    """ Main function for get to Twitter API """
    auth = tweepy.OAuthHandler(api_keys.consumer_key, api_keys.consumer_secret)
    auth.set_access_token(api_keys.access_token, api_keys.access_token_secret)
    api = tweepy.API(auth)
    return tweet_parse(api, count)
