from src.chatbot import Chatbot
from src.memory import ConversationMemory
from src.config import validate_config


def main():
    validate_config()
    bot = Chatbot()
    memory = ConversationMemory()
    print("Chatbot AI siap. Ketik '/reset' untuk hapus percakapan, atau '/exit' untuk keluar.")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "/exit":
            print("Sampai jumpa!")
            break
        if user_input.lower() == "/reset":
            memory.clear()
            print("Bot: 🧹 Riwayat percakapan telah di-reset.\n")
            continue

        print("Bot: Thinking...")
        memory.add_message('user', user_input)
        response = bot.send_message(memory.get_history())
        memory.add_message('assistant', response)
        print(f"Bot: {response}\n")

    
if __name__ == "__main__":
    main()