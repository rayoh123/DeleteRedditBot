import praw
import psaw
import details
import sys

###  LOGGING INTO REDDIT  ###
reddit_instance = praw.Reddit(user_agent=        'your custom user agent name here',
                              client_id=         details.client_id,
                              client_secret=     details.secret,
                              password=          details.password,
                              username=          details.username)

###  GETTING KEYWORD  ###
keyword = ''
sure = 'no'
while sure != 'yes':
    if sure not in ('yes', 'no'):
        print('\n\nYour input was incomprehensible. Please follow the instructions.')
    keyword = input('\nEnter in a keyword. I will delete all Reddit comments and posts on your account that'
                    ' contain this keyword. This purge will be case sensitive. Enter "quit" to quit ')
    if keyword == 'quit':
        sys.exit()
    else:
        sure = input(f'\n\nAre you sure you want {keyword} to be your keyword? All your posts and comments '
                      'that contain this keyword will be overwritten and deleted. There is no going back. (yes/no) ')
        
    
    
###  DELETING ALL RELEVANT POSTS AND COMMENTS ###
print('Now finding and deleting all your relevant posts and comments. I process one post/comment a second, so this might take '
      'a while depending on the amount of content on your account...')
s=0
c=0
api = psaw.PushshiftAPI()

# Dealing with comments
for comment in [comment for comment in list(api.search_comments(author=details.username, q=keyword)) \
                if reddit_instance.comment(comment.id).body!='[deleted]']:
    reddit_instance.comment(comment.id).delete()
    c+=1
    print(f'{c} comments have been deleted')

# Dealing with submissions
for submission in [submission for submission in list(api.search_submissions(author=details.username, q=keyword)) \
                   if reddit_instance.submission(submission.id).selftext!='[deleted]']:
    reddit_instance.submission(submission.id).delete()
    s+=1
    print(f'{s} posts have been deleted')

print(f'Purge complete. Deleted {s} posts and {c} comments.')



