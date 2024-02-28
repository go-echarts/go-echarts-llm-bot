import gradio as gr
from dotenv import load_dotenv
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.embeddings import AzureOpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import GitLoader
from langchain.chains import RetrievalQA

load_dotenv(verbose=True)

go_echarts = 'https://github.com/go-echarts/go-echarts'
go_echarts_examples = 'https://github.com/go-echarts/examples'

loader = GitLoader(repo_path="repo/go-echarts", clone_url=go_echarts, branch="master")
loader_examples = GitLoader(repo_path="repo/examples", clone_url=go_echarts_examples, branch="master")
pages_go_echarts = loader.load_and_split()
pages_go_echarts_examples = loader_examples.load_and_split()
pages_go_echarts.extend(pages_go_echarts_examples)

db = FAISS.from_documents(pages_go_echarts, AzureOpenAIEmbeddings())

openai_client = AzureChatOpenAI(deployment_name="gpt-35-turbo", temperature=0.5)

qa_client = RetrievalQA.from_chain_type(openai_client,
                                        retriever=db.as_retriever(search_type="similarity_score_threshold",
                                                                  search_kwargs={"score_threshold": 0.5})
                                        )


def bot(question, history):
    # Mention scope hardcode with prefix as workaround
    question = "In go-echarts, " + question

    answer = qa_client.run(question)
    if not answer:
        return "Could you provide more details on it? I can not answer it right now."
    return answer


bot_ui = gr.ChatInterface(
    fn=bot,
    title="Hello go-echarts",
    chatbot=gr.Chatbot(height=600),
)

bot_ui.launch(share=True, server_name="localhost", server_port=12345)
