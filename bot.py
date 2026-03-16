import telebot
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# ذاكرة المحادثات
chat_memory = {}

def ask_ai(chat_id, question):
    url = "https://openrouter.ai/api/v1/chat/completions"

    if chat_id not in chat_memory:
        chat_memory[chat_id] = []

    chat_memory[chat_id].append({"role": "user", "content": question})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": chat_memory[chat_id]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    chat_memory[chat_id].append({"role": "assistant", "content": answer})

    return answer


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "اهلا بك 👋\nاسألني أي سؤال وسأجيبك بالذكاء الاصطناعي.")


@bot.message_handler(func=lambda message: True)
def chat(message):
    bot.send_chat_action(message.chat.id, "typing")

    answer = ask_ai(message.chat.id, message.text)

    bot.reply_to(message, answer)


bot.infinity_polling()
