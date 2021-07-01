from comment_dynamic import Comment

id = input('动态ID: ')
commentwh = Comment(id)

uid_list = commentwh.get_comment_uid_list(remove_repeat=False)
print('此动态下评论的UID列表（主楼，不包含置顶，不去重）：\n', uid_list)
uid_list_filtered = commentwh.get_comment_uid_list()
print('此动态下评论的UID列表（主楼，不包含置顶，去重）：\n', uid_list_filtered)
