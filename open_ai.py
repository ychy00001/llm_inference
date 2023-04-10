# -*- coding: utf-8 -*-

import time
import openai
from common.log import logger
from common.timer import get_time
import common.config as config
import traceback

user_session = dict()


class OpenAI:

    def __init__(self):
        openai.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL

    def process_with_session(self, msg, from_user_id):
        # acquire reply content
        if msg == '#清除记忆':
            Session.clear_session(from_user_id)
            return '记忆已清除'

        new_query = Session.build_session_query(msg, from_user_id)
        logger.debug("[OPEN_AI] session query={}".format(new_query))

        reply_content = self.process_text(new_query, from_user_id)
        if reply_content and msg:
            Session.save_session(msg, reply_content, from_user_id)
        return reply_content

    @get_time
    def process_text(self, msg, user_id, retry_count=1):
        logger.info("[OPEN_AI] process_text={}".format(msg))
        try:
            response = openai.Completion.create(
                model=self.model,
                prompt=msg,
                temperature=0.4,  # 值在[0,1]之间，越大表示回复越具有不确定性
                max_tokens=500,  # 回复最大的字符数
                top_p=1,
                frequency_penalty=0.8,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                presence_penalty=1.0,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                stop=["\n\n\n"]
            )
            res_content = response.choices[0]['text'].strip().replace('<|endoftext|>', '')
            logger.info("[OPEN_AI] reply={}".format(res_content))
            return res_content
        except openai.error.RateLimitError as e:
            # rate limit exception
            if retry_count < 1:
                time.sleep(2)
                logger.warn("[OPEN_AI] RateLimit exceed, 第{}次重试".format(retry_count + 1))
                return self.process_text(msg, user_id, retry_count + 1)
            else:
                logger.error(e.json_body)
                return "提问太快啦，请休息一下再问我吧"
        except Exception as e1:
            # unknown exception
            logger.error(traceback.print_exc())
            Session.clear_session(user_id)
            return "请再问我一次吧"


class Session(object):
    @staticmethod
    def build_session_query(query, user_id):
        '''
        build query with conversation history
        e.g.  Q: xxx
              A: xxx
              Q: xxx
        :param query: query content
        :param user_id: from user id
        :return: query content with conversaction
        '''
        prompt = config.OPENAI_CHARACTER_DESC
        if prompt:
            prompt += "<|endoftext|>\n\n\n"
        session = user_session.get(user_id, None)
        if session:
            for conversation in session:
                prompt += "Q: " + conversation["question"] + "\n\n\nA: " + conversation["answer"] + "<|endoftext|>\n"
            prompt += "Q: " + query + "\nA: "
            return prompt
        else:
            return prompt + "Q: " + query + "\nA: "

    @staticmethod
    def save_session(query, answer, user_id):
        max_tokens = int(config.OPENAI_SESSION_MAX_TOKENS)
        if not max_tokens:
            # default 3000
            max_tokens = 1000
        conversation = dict()
        conversation["question"] = query
        conversation["answer"] = answer
        session = user_session.get(user_id)
        if session:
            # append conversation
            session.append(conversation)
        else:
            # create session
            queue = list()
            queue.append(conversation)
            user_session[user_id] = queue

        # discard exceed limit conversation
        Session.discard_exceed_conversation(user_session[user_id], max_tokens)

    @staticmethod
    def discard_exceed_conversation(session, max_tokens):
        count = 0
        count_list = list()
        for i in range(len(session) - 1, -1, -1):
            # count tokens of conversation list
            history_conv = session[i]
            count += len(history_conv["question"]) + len(history_conv["answer"])
            count_list.append(count)

        for c in count_list:
            if c > max_tokens:
                # pop first conversation
                session.pop(0)

    @staticmethod
    def clear_session(user_id):
        user_session[user_id] = []
