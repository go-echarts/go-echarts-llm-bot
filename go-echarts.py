import os
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import GitLoader
from langchain.chains import RetrievalQA

load_dotenv(verbose=True)

go_echarts = 'https://github.com/go-echarts/go-echarts'
go_echarts_examples = 'https://github.com/go-echarts/examples'
victories_db = 'victories_db'


def load_go_echarts(fetch_hard=False):
    if not fetch_hard:
        if os.path.exists(victories_db):
            print('Loading go-echarts from local index')
            return FAISS.load_local(victories_db, AzureOpenAIEmbeddings())

    print('Loading go-echarts and embedding')
    loader = GitLoader(repo_path="repo/go-echarts", clone_url=go_echarts, branch="master")
    loader_examples = GitLoader(repo_path="repo/examples", clone_url=go_echarts_examples, branch="master")
    pages_go_echarts = loader.load_and_split()
    pages_go_echarts_examples = loader_examples.load_and_split()
    pages_go_echarts.extend(pages_go_echarts_examples)

    db = FAISS.from_documents(pages_go_echarts, AzureOpenAIEmbeddings())
    db.save_local(victories_db)
    return db


def bot(question, history):
    # Mention scope hardcode with prefix as workaround
    question = "In go-echarts, " + question

    answer = qa_client.run(question)
    if not answer:
        return "Could you provide more details on it? I can not answer it right now."
    return answer


def gui():
    bot_ui = gr.ChatInterface(
        fn=bot,
        title="Hello go-echarts",
        chatbot=gr.Chatbot(height=600),
    )

    print("Bot setup: ")
    bot_ui.launch(server_name="localhost", server_port=12345)


if __name__ == "__main__":
    openai_client = AzureChatOpenAI(deployment_name="gpt-35-turbo", temperature=0.2)

    go_echarts_db = load_go_echarts()
    qa_client = RetrievalQA.from_chain_type(openai_client,
                                            retriever=go_echarts_db.as_retriever(
                                                search_type="similarity_score_threshold",
                                                search_kwargs={"score_threshold": 0.5})
                                            )
    gui()
