from langchain.memory import ConversationBufferMemory

def BufferMemory(memory_key="chat_history", return_messages=True):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return memory

