# インポートするライブラリ
from flask import Flask, request, abort
from linebot import (
   LineBotApi, WebhookHandler
)
from linebot.exceptions import (
   InvalidSignatureError
)
from linebot.models import (
   FollowEvent, JoinEvent, PostbackEvent, FlexSendMessage, MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
   RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, RichMenuResponse, MessageAction, PostbackTemplateAction, PostbackAction, URIAction,
)
import os
import psycopg2
import payload
import requests,json,re
# 軽量なウェブアプリケーションフレームワーク:Flask
app = Flask(__name__) #環境変数からLINE Access Tokenを設定
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"] #環境変数からLINE Channel Secretを設定
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def createRichmenu():
    result = False
    try:
        # define a new richmenu
        print("alive")
        rich_menu_to_create = RichMenu(
            size = RichMenuSize(width=1200, height=405),
            selected = True,
            name = 'richmenu for randomchat',
            chat_bar_text = 'メニューを開く',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=0, y=0, width=800, height=405),
                    action=PostbackAction(
                        label='メニュー',
                        display_text='',
                        data="メニュー",
                    )
                ),
                RichMenuArea(
                    bounds=RichMenuBounds(x=800, y=0, width=400, height=405),
                    action=MessageAction(text='退出')
                ),
            ]
        )
        print("ok?")
        richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
        print(richMenuId)
        # upload an image for rich menu
        path = 'menu.png'

        with open(path, 'rb') as f:
            print("path!!")
            print(f)
            line_bot_api.set_rich_menu_image(richMenuId, 'image/png', f)
            print("comp")
        
        print("madaka!")

        # set the default rich menu
        line_bot_api.set_default_rich_menu(richMenuId)

        result = True

    except Exception as e:
        print(e)
        result = False

    return result

#dbとの接続関係
#--------------------------dbを操作する主な機能--------------------------#
def get_connection():
    dsn = "host=ec2-18-233-32-61.compute-1.amazonaws.com port=5432 dbname=dbi32vi74s6bfo user=tajtnyyaunazcn password=d6786b0e47252911f8cb6c62ed8a2fb2869bec15382f9a28cb879dab64a06bb9"
    return psycopg2.connect(dsn)

def select_from_app_user(user_id,type):
    res=""
    with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT * FROM app_user WHERE id = %s",(user_id,))
                    result=cur.fetchall()
                    print(result[0])
                    if type==1:
                        res=result[0][1]
                    elif type==3:
                        res=result[0][3]
                except Exception as e:
                    print("error: ",e)
            conn.commit()
    return res

def select_from_room_with_owner_id(user_id):
    room_id=""
    with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT * FROM room WHERE owner_id=%s",(user_id,))
                    result=cur.fetchall()
                    room_id=result[0][0]
                except Exception as e:
                    print("error: ",e)
            conn.commit()
    return room_id
    
def update_app_user_with_room_id(user_id,room_id):
    result=True
    with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("update app_user set room_id=%s where id=%s",(room_id,user_id))
                except Exception as e:
                    result=False
                    print("error: ",e)
            conn.commit()
    return result


def insert_room(name,num,user_id,event):
    virtual_group_id=select_from_app_user(user_id,3)
    with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("INSERT INTO room (name,virtual_group_id,owner_id,capacity) VALUES (%s,%s,%s,%s)",(name,virtual_group_id,user_id,num))
                except Exception as e:
                    print("error: ",e)
            conn.commit()
    room_id=select_from_room_with_owner_id(user_id)
    if update_app_user_with_room_id(user_id,room_id):
        user_name=select_from_app_user(user_id,1)
        return "通知：　"+user_name+"さんが入室しました"

def get_response_message(mes_from,event):
    # "日付"が入力された時だけDBアクセス
    if mes_from=="日付":
        with get_connection() as conn:
            with conn.cursor(name="cs") as cur:
                try:
                    sqlStr = "SELECT TO_CHAR(CURRENT_DATE, 'yyyy/mm/dd');"
                    cur.execute(sqlStr)
                    (mes,) = cur.fetchone()
                    return mes
                except:
                    mes = "exception"
                    return mes
    elif mes_from=="menu":
        result=createRichmenu()
        print(result)
    elif re.match(r'部屋名：.+、定員：[0-9]',mes_from):
        name_obj=re.search(r'部屋名：',mes_from)
        sep_obj=re.search(r'、',mes_from)
        num_obj=re.search(r'定員：',mes_from)
        size=len(mes_from)
        len_name=sep_obj.end()-name_obj.end()-1
        len_num=num_obj.end()-sep_obj.end()-1
        name=mes_from[name_obj.end():sep_obj.start()]
        num=mes_from[num_obj.end():size]
        print(name,num)
        return insert_room(name,num,event.source.user_id,event)
    # それ以外はオウム返し
    return mes_from

def insert_virtual_group(line_group_id,line_group_name):
    result=True
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("INSERT INTO virtual_group (name,line_group_id) VALUES (%s,%s)",(line_group_name,line_group_id))
            except Exception as e:
                result=False
                print("error: ",e)
        conn.commit()
    print(result)

def select_form_room(event):
    with get_connection() as conn:
        with conn.cursor(name="cs") as cur:
            try:
                sqlStr = 'SELECT * FROM room'
                cur.execute(sqlStr)
                results=cur.fetchall()
                print(results)
                mes=[]
                for result in results:
                    mes.append((result[1],result[4]))
                print(mes)
                temporary_payload=payload.payload_room_list
                print(temporary_payload)
                for m in mes: 
                    Str=str(m[0])+" ("+str(m[1])+")"
                    temporary_payload['contents']['body']['contents'][0]['contents'].
                    append({"type": "text","text": Str,"align": "center","weight": "bold"})
                    print(temporary_payload)

                container_obj = FlexSendMessage.new_from_json_dict(temporary_payload)
                
                line_bot_api.reply_message(
                    event.reply_token,
                    messages=container_obj
                )
            except Exception as e:
                print("error: ",e)

def select_from_virtual_group(line_group_id):
    virtual_group_id=""
    print(line_group_id)
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT * FROM virtual_group WHERE line_group_id = %s",(line_group_id,))
                results=cur.fetchall()
                virtual_group_id=results[0][0]
                print(virtual_group_id)
            except Exception as e:
                print("error: ",e)
                virtual_group="error_id"
        conn.commit()
    return virtual_group_id

def insert_app_user(line_group_id,user_id):
    virtual_group_id=select_from_virtual_group(line_group_id)
    print(virtual_group_id)
    if virtual_group_id=="error_id":
        print("error: This virtual_group_id is invalid.")
    else:
        with get_connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("INSERT INTO app_user (id,name,virtual_group_id) VALUES (%s,%s,%s)",(user_id,"名無し",virtual_group_id))
                except Exception as e:
                    print("error: ",e)
            conn.commit()


#-------ここからアプリの基本処理--------#
@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
   signature = request.headers['X-Line-Signature']
   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)
   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'
# MessageEvent
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=get_response_message(event.message.text,event))
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    print("postback")
    print(event.postback.data)
    data=event.postback.data
    if data=="メニュー":
        print("menu")
        container_obj = FlexSendMessage.new_from_json_dict(payload.payload_menu)
        line_bot_api.reply_message(
            event.reply_token,
            messages=container_obj
        )
    elif data=="部屋リスト":
        select_form_room(event)
    elif data=="参加":
        insert_app_user(event.source.group_id,event.source.user_id)
    elif data=="部屋作成":
        container_obj = FlexSendMessage.new_from_json_dict(payload.payload_make_room)
        line_bot_api.reply_message(
            event.reply_token,
            messages=container_obj
        )


@handler.add(FollowEvent)
def handle_follow(event):
    
    container_obj = FlexSendMessage.new_from_json_dict(payload.payload_menu)
    line_bot_api.reply_message(
        event.reply_token,
        messages=container_obj
    )

@handler.add(JoinEvent)
def handle_join(event):
    print(event)
    if hasattr(event.source,"group_id"):
        group_id=event.source.group_id
        headers = {"content-type": "application/json; charset=UTF-8",'Authorization':'Bearer {}'.format(LINE_CHANNEL_ACCESS_TOKEN)}
        url = 'https://api.line.me/v2/bot/group/' + group_id + '/summary'
        response = requests.get(url, headers=headers)
        response=response.json()
        group_name=response['groupName']
        print(group_id,group_name)
        insert_virtual_group(group_id,group_name)
        container_obj = FlexSendMessage.new_from_json_dict(payload.payload_group)
        line_bot_api.reply_message(
            event.reply_token,
            messages=container_obj
        )

if __name__ == "__main__":
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)