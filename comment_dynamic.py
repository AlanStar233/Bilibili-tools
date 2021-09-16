import json
import requests
import time

with open('dynamic_types.json', 'r') as load_file:
    dynamic_types = json.load(load_file)


class Comment(object):
    def __init__(self, dynamic_id):
        super().__init__()
        self.session = requests.Session()
        self.dynamic_detail = self.get_dynamic_details(dynamic_id)

    def get_comment_uid_list(self, sort=2, ps=49, counter=1, refresh_interval=5, sleep=1, next_reply=0, remove_repeat=True):
        # 防止 412 错误
        if counter % refresh_interval == 0:
            time.sleep(sleep)
        # 检测回复的 type 和 oid
        dynamic_type = str(self.dynamic_detail['data']['card']['desc']['type'])
        if dynamic_type in dynamic_types['types']:
            type_data = dynamic_types['types'][dynamic_type]
            type_oid_path = type_data['path']
            oid = self.dynamic_detail
            for k in type_oid_path:
                oid = oid[k]
            type_value = type_data['value']

            # API - 只展示主楼回复
            # comment_url = 'https://api.bilibili.com/x/v2/reply?type={}&oid={}&sort={}&ps={}&pn={}'.format(type_value, oid, sort, ps, pn)
            # API - 展示主楼和楼中楼回复
            comment_url = 'https://api.bilibili.com/x/v2/reply/main?type={}&oid={}&mode={}&ps={}&next={}'.format(type_value, oid, sort, ps, next_reply)
            # 获取当前页的回复
            while True:
                try:
                    topic_info_response = self.session.get(comment_url)
                    break
                except:
                    time.sleep(1)
            comment_info = json.loads(topic_info_response.content.decode())
            if comment_info['code'] != 0:
                if comment_info['code'] == -404:
                    raise ValueError
                elif comment_info['code'] == -400:
                    raise ValueError
                else:
                    raise ValueError
            reply_list = comment_info['data']['replies']
            # API的总计数方法-仅显示主答复
            # 回复总数=评论信息['data']['page']['count']
            # API的总计数方法-包含部分子答复的答复
            # 回复总数=评论信息['data']['cursor']['all\u count']
            uid_list = []
            # 避免空回复导致错误
            if reply_list is None:
                return []
            # 给每个回复添加UID
            for reply in reply_list:
                uid_list.append(reply['mid'])
            # 检查是否有另一个API页面-仅显示主要回复
            # if total_replies - ps * counter > 0:
            #     uid_list.extend(self.get_comment_uid_list(sort, ps, counter + 1))
            next_reply = comment_info['data']['cursor']['next']
            if next_reply != 1:
                uid_list.extend(self.get_comment_uid_list(sort, ps, counter+1, next_reply=next_reply))
            if remove_repeat:
                uid_list = list(set(uid_list))
            return uid_list

    def get_dynamic_details(self, dynamic_id):
        dynamic_detail_url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'.format(dynamic_id)
        while True:
            try:
                dynamic_detail_response = self.session.get(dynamic_detail_url)
                break
            except:
                time.sleep(1)
        dynamic_detail = json.loads(dynamic_detail_response.content.decode())
        if dynamic_detail['code'] != 0:
            if dynamic_detail['code'] == -404:
                raise ValueError
            elif dynamic_detail['code'] == -400:
                raise ValueError
            else:
                raise ValueError
        else:
            return dynamic_detail

    def get_comment_uname_list(self, sort=2, ps=49, counter=1, refresh_interval=5, sleep=1, next_reply=0, remove_repeat=True):
        # 防止412错误
        if counter % refresh_interval == 0:
            time.sleep(sleep)
        # 检查回复的 type 和 oid
        dynamic_type = str(self.dynamic_detail['data']['card']['desc']['type'])
        if dynamic_type in dynamic_types['types']:
            type_data = dynamic_types['types'][dynamic_type]
            type_oid_path = type_data['path']
            oid = self.dynamic_detail
            for k in type_oid_path:
                oid = oid[k]
            type_value = type_data['value']

            # API - Only Display Main Replies
            # comment_url = 'https://api.bilibili.com/x/v2/reply?type={}&oid={}&sort={}&ps={}&pn={}'.format(type_value, oid, sort, ps, pn)
            # API - Replies with Part of Sub-replies
            comment_url = 'https://api.bilibili.com/x/v2/reply/main?type={}&oid={}&mode={}&ps={}&next={}'.format(type_value, oid, sort, ps, next_reply)
            # Obtain reply for current page
            while True:
                try:
                    topic_info_response = self.session.get(comment_url)
                    break
                except:
                    time.sleep(1)
            comment_info = json.loads(topic_info_response.content.decode())
            if comment_info['code'] != 0:
                if comment_info['code'] == -404:
                    raise ValueError
                elif comment_info['code'] == -400:
                    raise ValueError
                else:
                    raise ValueError
            reply_list = comment_info['data']['replies']
            # Total Count Approach for API - Only Display Main Replies
            # total_replies = comment_info['data']['page']['count']
            # Total Count Approach for API - Replies with Part of Sub-replies
            # total_replies = comment_info['data']['cursor']['all_count']
            uname_list = []
            # Avoid error caused by empty replies
            if reply_list is None:
                return []
            # Add UID for each reply
            for reply in reply_list:
                uname_list.append(reply['member']['uname'])
            # Check if there is another page for API - Only Display Main Replies
            # if total_replies - ps * counter > 0:
            #     uid_list.extend(self.get_comment_uid_list(sort, ps, counter + 1))
            next_reply = comment_info['data']['cursor']['next']
            if next_reply != 1:
                uname_list.extend(self.get_comment_uname_list(sort, ps, counter + 1, next_reply=next_reply))
            if remove_repeat:
                uname_list = list(set(uname_list))
            return uname_list

    def get_comment_user_list(self, sort=2, ps=49, counter=1, refresh_interval=5, sleep=1, next_reply=0,
                                   remove_repeat=True):
        # Technique to avoid 412
        if counter % refresh_interval == 0:
            time.sleep(sleep)
        # Detect reply type & oid
        dynamic_type = str(self.dynamic_detail['data']['card']['desc']['type'])
        if dynamic_type in dynamic_types['types']:
            type_data = dynamic_types['types'][dynamic_type]
            type_oid_path = type_data['path']
            oid = self.dynamic_detail
            for k in type_oid_path:
                oid = oid[k]
            type_value = type_data['value']

            # API - Only Display Main Replies
            # comment_url = 'https://api.bilibili.com/x/v2/reply?type={}&oid={}&sort={}&ps={}&pn={}'.format(type_value, oid, sort, ps, pn)
            # API - Replies with Part of Sub-replies
            comment_url = 'https://api.bilibili.com/x/v2/reply/main?type={}&oid={}&mode={}&ps={}&next={}'.format(
                type_value, oid, sort, ps, next_reply)
            # Obtain reply for current page
            while True:
                try:
                    topic_info_response = self.session.get(comment_url)
                    break
                except:
                    time.sleep(1)
            comment_info = json.loads(topic_info_response.content.decode())
            if comment_info['code'] != 0:
                if comment_info['code'] == -404:
                    raise ValueError
                elif comment_info['code'] == -400:
                    raise ValueError
                else:
                    raise ValueError
            reply_list = comment_info['data']['replies']
            # Total Count Approach for API - Only Display Main Replies
            # total_replies = comment_info['data']['page']['count']
            # Total Count Approach for API - Replies with Part of Sub-replies
            # total_replies = comment_info['data']['cursor']['all_count']
            user_list = ''
            # Avoid error caused by empty replies
            if reply_list is None:
                return ''
            # Add UID for each reply
            for reply in reply_list:
                # user_list += str.format('{{\"username\": \"{}\", \"uid\": {}}}, ', reply['member']['uname'], reply['mid'])
                user_list += str.format('\"{}\": \"{}\", ', reply['mid'], reply['member']['uname'])
            # Check if there is another page for API - Only Display Main Replies
            # if total_replies - ps * counter > 0:
            #     uid_list.extend(self.get_comment_uid_list(sort, ps, counter + 1))
            next_reply = comment_info['data']['cursor']['next']
            if next_reply != 1:
                user_list += (self.get_comment_user_list(sort, ps, counter + 1, next_reply=next_reply))
            if counter == 1:
                # user_list = '[' + user_list[:(len(user_list) - 2)] + ']'
                user_list = '{' + user_list[:(len(user_list) - 2)] + '}'
                user_list = json.loads(user_list)
            return user_list
