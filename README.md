<p align="center">
	<img src="https://user-images.githubusercontent.com/19553554/52535979-c0d0e680-2d8f-11e9-85c8-2e9f659e7c6f.png" width=300 height=300 />
</p>

<h1 align="center">go-echarts-llm-bot</h1>
<p align="center">
    <em> The localized QA Chatbot for go-echarts.</em>
</p>


The `go-echarts-llm-bot` depends on the [`LangChain`](https://github.com/langchain-ai/langchain)
which help to develop LLM applications easily.  
The Chatbot GUI is powered by [Gradio](https://github.com/gradio-app/gradio).   
The underlying OpenAI service is `AzureOpenAI`, see more details
in [Azure AI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service).

---
Any issue in go-echarts? Call `12345` (the localized Chatbot GUI server port) for help! :telephone_receiver:

![go-echarts-bot-gif](https://github.com/go-echarts/go-echarts-llm-bot/assets/33706142/24221c4c-db6c-490b-a329-03f77cae4111)

## Install

> Python v3.11.8 is used, I recommend using the same version to avoid dependency issue.

**Install dependencies**

```shell
 pip install -r requirements.txt
```

## Configuration

Rename the `.env_sample` file to `.env` and put your own Azure Open AI configs in it.
> .env

```
AZURE_OPENAI_API_KEY=***your_api_key***
OPENAI_API_VERSION=2024-02-14
AZURE_OPENAI_ENDPOINT=https://my-openai.azure.com
OPENAI_API_TYPE=azure
```

Or change to other LLM providers and change the related api.

# LICENSE

MIT [@Koooooo-7](https://github.com/Koooooo-7)