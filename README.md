#Pregnancy Question-Answering System with RAG

-Note that when running the project, it might take few seconds-up to a minute to scrape the articles and create a vector store

-This project is a Retrieval-Augmented Generation (RAG)-based system designed to help pregnant women find tailored answers to their questions. By combining cutting-edge AI technology with curated resources, the system delivers accurate, personalized, and easy-to-understand information related to pregnancy.

##Key Features

###1. Personalized Answers

The system tailors responses based on the user's pregnancy week, ensuring that the information provided is relevant to their specific stage.

###2. Accurate Information Retrieval

Articles and resources are scraped from trusted sources, processed, and stored in a FAISS vector store for efficient retrieval.

###3. Summarized Responses

Instead of lengthy explanations, the system condenses information into concise, user-friendly answers.

###4. Source Transparency

Provides summaries and URLs of the original sources used to answer questions, so users can verify the information.

##How It Works

###1. Scraping Trusted Articles

-The system fetches articles from specified URLs, which contain information about pregnancy topics.

###2. Processing and Storing Data

-The articles are split into smaller chunks using text splitting techniques.

-These chunks are converted into vector embeddings using HuggingFace embeddings and stored in a FAISS vector store for efficient search.

###3. Question Understanding

-When a user asks a question, the system uses a language model (OpenAI GPT) to understand the intent and context of the query.

###4. Retrieving Relevant Information

-The system retrieves the most relevant chunks of text from the FAISS vector store using similarity search.

###5. Answer Generation

-The language model combines the retrieved chunks to generate a clear and concise response.

-A summarization chain is also included to condense long or complex answers further.

###6. Personalization by Pregnancy Week

-The system adjusts its answers based on the pregnancy week selected by the user, providing stage-appropriate advice and insights.

##Technologies Used

-LangChain: Framework for building retrieval-augmented applications.

-HuggingFace Embeddings: Converts text into embeddings for similarity search.

-FAISS: A fast similarity search tool used as the vector store.

-OpenAI GPT: Generates responses and summaries from retrieved information.

-Python: Core programming language for development.

-Streamlit: Frontend for user interaction.

#Installation and Setup

-Clone the Repository

`git clone [<https://github.com/aruaycodes/PreggoAI.git>]`

-Install Dependencies

`pip install -r requirements.txt`

-Add API Keys

Ensure you have access to OpenAI and other necessary API keys.

Create a .env file in the root directory and add your keys:

OPENAI_API_KEY=your_openai_key

Run the Application

`streamlit run app.py`

##Usage

-Select your pregnancy week from the dropdown.

-Enter your question in the text box.

-View the tailored response and summaries of source articles.

-To get a new question answered, please press `Command+Enter` , then type in your question

#Example Questions

"What foods should I eat in my first trimester?"

"How can I manage back pain during pregnancy?"

"What are common symptoms at 20 weeks pregnant?"

Future Improvements

Add more trusted pregnancy resources.

Enable multilingual support for more inclusivity.

Incorporate visual guides for key pregnancy topics.

Expand personalization to include specific health conditions or preferences.

Contributing

We welcome contributions! Please open an issue or submit a pull request with your suggestions and improvements.
