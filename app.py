# -*- coding: utf-8 -*-

from open_ai import OpenAI
from flask import Flask, redirect, render_template, request, url_for
import common.config as config
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

app = Flask(__name__)
ai = OpenAI()


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        res_content = ai.process_with_session(request.form["msg"], 1)
        return redirect(url_for("index", result=res_content))
    result = request.args.get("result")
    return render_template("index.html", result=result)


# 定义微信公众平台接口验证路由
@app.route("/wechat", methods=["GET", "POST"])
def verify():
    # 获取 GET 请求参数
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    echostr = request.args.get("echostr", "")
    token = "weixin"

    # 验证请求签名
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        return "Invalid signature", 400
    # 处理 GET 请求
    if request.method == "GET":
        return echostr

    # 处理 POST 请求
    xml_str = request.data
    msg = parse_message(xml_str)
    if msg:
        # 处理业务逻辑并返回响应
        reply = None
        # 使用 OpenAI 库生成回复内容
        if msg.type == "text":
            res_content = ai.process_text(msg.content, 1)
            reply = create_reply(res_content, msg)
        else:
            reply = "暂不支持该类消息"
        # 返回回复消息
        if reply is None:
            reply = create_reply("抱歉，无法理解你在说什么！", msg)
        xml = reply.render()
        return xml
    else:
        # 收到超时消息，不进行处理
        return 'success'


@app.route("/chat", methods=["GET"])
def chat():
    msg = request.args.get("msg")
    res_content = ai.process_text(msg, 1)
    return res_content


if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=int(config.APP_PORT))
