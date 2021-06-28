import random
from comment_dynamic import Comment

id = input('动态ID: ')
times = int(input('抽奖次数: '))
commentwh = Comment(id)
user_list = commentwh.get_comment_user_list()
print('此动态下评论的用户名、UID列表（主楼，不包含置顶，去重）:\n', user_list)

# Lottery Part
winners = {}
for i in range(times):
    print('开始抽取第', i + 1, '位中奖用户...')
    winner = random.choice(list(user_list.keys()))
    print('恭喜', user_list[winner], '(UID:', winner, '\b) 获得本次奖励！')
    winners.update({winner: user_list[winner]})
    user_list.pop(winner)
