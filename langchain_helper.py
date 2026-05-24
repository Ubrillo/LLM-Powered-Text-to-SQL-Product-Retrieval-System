import os
import re
from operator import itemgetter
from dotenv import  load_dotenv
from few_shots import few_shots
from langchain_chroma import Chroma
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.chains import create_sql_query_chain
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.agent_toolkits.sql.prompt import SQL_PREFIX, SQL_SUFFIX

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

from langchain_openai import OpenAI
api_key = os.getenv("OPENAI_KEY")
llm = OpenAI(api_key = api_key, temperature=0.2)


# ── SQL DATABASE ──────────────────────────────────────────────────
db_user     = "dev"
db_password = "dev123"
db_host     = "localhost"
db_name     = "afriq_tshirts"
port        = 3306

db = SQLDatabase.from_uri(
    f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
    sample_rows_in_table_info=3,
)
_execute = QuerySQLDataBaseTool(db=db)

# ── Answer prompt: converts SQL result → natural language ─────────
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Given the question, the SQL query used, and the SQL result, write a clear and concise natural language answer."),
    ("human", """Question : {question}
    SQL Query: {query}
    SQL Result: {result}

    Answer:""")
    ])

def get_llm_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    PROMPT_SUFFIX = """Only use the following tables:
        {table_info}

        Question: {input}"""

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=SQL_PREFIX,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"],
    )

    # Chain 1: question → SQL query
    sql_chain = create_sql_query_chain(llm, db, prompt=few_shot_prompt)

    # Chain 2: question + SQL + result → natural language answer
    full_chain = (
        RunnablePassthrough.assign(query=sql_chain)               # generate SQL
        | RunnablePassthrough.assign(result=itemgetter("query") | _execute)                  # execute SQL
        | answer_prompt                                            # format answer prompt
        | llm                                                      # interpret result
        | StrOutputParser()                                        # extract plain string
    )

    return full_chain

def ask(question: str, chain) -> str:
    """Run the full chain and return a plain natural language answer."""
    answer = chain.invoke({"question": question, "input": question})
    print(f"\nAnswer: {answer}\n")
    return answer


if __name__ == '__main__':
    chain = get_llm_chain()
    ask('how many total tshirts are left in total in stock?', chain)