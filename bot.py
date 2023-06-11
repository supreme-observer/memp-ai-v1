from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import GPT4All, LlamaCpp
import os
import argparse
from langchain import PromptTemplate

load_dotenv()

embeddings_model_name = os.environ.get("EMBEDDINGS_MODEL_NAME")
persist_directory = os.environ.get('PERSIST_DIRECTORY')

model_type = os.environ.get('MODEL_TYPE')
model_path = os.environ.get('MODEL_PATH')
model_n_ctx = os.environ.get('MODEL_N_CTX')
target_source_chunks = int(os.environ.get('TARGET_SOURCE_CHUNKS', 4))

from constants import CHROMA_SETTINGS


class Bot:
    def __init__(self):
        # Parse the command line arguments
        args = self.parse_arguments()
        embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
        db = Chroma(persist_directory=persist_directory, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
        retriever = db.as_retriever(search_kwargs={"k": target_source_chunks})
        # activate/deactivate the streaming StdOut callback for LLMs
        callbacks = [] if args.mute_stream else [StreamingStdOutCallbackHandler()]
        # Prepare the LLM
        match model_type:
            case "LlamaCpp":
                llm = LlamaCpp(model_path=model_path, n_ctx=model_n_ctx, callbacks=callbacks, verbose=False)
            case "GPT4All":
                llm = GPT4All(model=model_path, n_ctx=model_n_ctx, backend='gptj', callbacks=callbacks, verbose=False)
            case _default:
                print(f"Model {model_type} not supported!")
                exit;

        prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Answer:"""
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        chain_type_kwargs = {"prompt": PROMPT}
        self.qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever,
                                              chain_type_kwargs=chain_type_kwargs)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Bot: Ask questions to your documents without an internet connection, '
                                                     'using the power of LLMs.')
        parser.add_argument("--hide-source", "-S", action='store_true',
                            help='Use this flag to disable printing of source documents used for answers.')

        parser.add_argument("--mute-stream", "-M",
                            action='store_true',
                            help='Use this flag to disable the streaming StdOut callback for LLMs.')

        return parser.parse_args()

    def answer(self, query):
        # Get the answer from the chain
        res = self.qa.run(query)
        return res
