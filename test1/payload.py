payload_menu={
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "direction": "ltr",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "ようこそ！",
              "align": "center",
              "weight": "bold"
            },
            {
              "type": "text",
              "text": "名無しさん！",
              "align": "center",
              "weight": "bold"
            },
            {
              "type": "spacer",
              "size": "xxl"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "button",
              "action": {
                "type": "postback",
                "label": "部屋を一覧",
                "data": "部屋リスト"
              },
              "color": "#177FF9"
            },
            {
              "type": "button",
              "action": {
                "type": "postback",
                "label": "部屋を作る",
                "data": "部屋作成"
              },
              "color": "#F61818"
            },
            {
              "type": "button",
              "action": {
                "type": "postback",
                "label": "ニックネームを変える",
                "data": "ニックネーム変更"
              },
              "color": "#16F43B"
            }
          ]
        }
      ]
    }
  }
}

payload_group ={
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "header": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "text",
          "text": "匿名チャット",
          "size": "sm",
          "weight": "bold",
          "color": "#AAAAAA"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://2.bp.blogspot.com/-ZWJKvLxGRCo/V4SA6jTHXqI/AAAAAAAA8OA/MlXUUJgevi0doVonmtfKBt5Dw6v-8rZwACLcB/s400/circle_figure2.png",
      "size": "full",
      "aspectRatio": "1:1",
      "aspectMode": "cover",
      "action": {
        "type": "uri",
        "label": "Action",
        "uri": "https://linecorp.com/"
      }
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "postback",
            "label": "参加する",
            "data": "参加"
          }
        }
      ]
    }
  }
}

payload_room_list={
    "type": "flex",
    "altText": "Flex Message",
    "contents": {
        "type": "bubble",
        "direction": "ltr",
        "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "部屋の一覧！",
                "align": "center",
                "weight": "bold"
                }
            ]
            }
        ]
        }
    }
}

payload_make_room={
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "部屋を作成する",
          "align": "center",
          "weight": "bold"
        }
      ]
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "「部屋名：(部屋名)、定員：(半角数字)」のように記入してください",
              "align": "center",
              "color": "#1E4DE1",
              "wrap": True
            },
            {
              "type": "spacer",
              "size": "xxl"
            }
          ]
        },
        {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": "例：部屋名：雑談部屋、定員：10"
            }
          ]
        }
      ]
    }
  }
}