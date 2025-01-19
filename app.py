import streamlit as st
from article_rag import ArticleRAG, load_vector_store




# Provide the URLs for the articles you want to scrap
# Initialize the ArticleRAG system (do this only once)
def initialize_rag_system():
    if "rag_system" not in st.session_state:
        try :
            urls = [
                "https://womenshealth.gov/pregnancy/youre-pregnant-now-what/stages-pregnancy",
                "https://my.clevelandclinic.org/health/articles/7247-fetal-development-stages-of-growth",
                "https://www.mentalhealthjournal.org/articles/an-overview-of-maternal-anxiety-during-pregnancy-and-the-post-partum-period.html",
                "https://www.parents.com/pregnancy/complications/health-and-safety-issues/top-pregnancy-fears/",
                "https://my.clevelandclinic.org/health/articles/pregnancy-pains",
                "https://www.medicalnewstoday.com/articles/327385#prevention",
                "https://my.clevelandclinic.org/health/diseases/12230-birth-defects",
                "https://health.clevelandclinic.org/dyeing-your-hair-while-pregnant",
                "https://www.webmd.com/baby/dyeing-your-hair-while-pregnant-what-to-know",
                "https://utswmed.org/medblog/alcohol-during-pregnancy/",
                "https://www.nhs.uk/pregnancy/keeping-well/travelling/",
                "https://www.medicalnewstoday.com/articles/sleeping-on-the-stomach-pregnant#changing-positions",
                "https://pmc.ncbi.nlm.nih.gov/articles/PMC11018210/",
                "https://americanpregnancy.org/healthy-pregnancy/pregnancy-health-wellness/second-hand-smoke-and-pregnancy/",
                "https://americanpregnancy.org/healthy-pregnancy/pregnancy-health-wellness/how-air-pollution-impacts-pregnancy/",
                "https://www.cdc.gov/heat-health/hcp/clinical-overview/heat-and-pregnant-women.html",
                "https://www.pregnancybirthbaby.org.au/injuries-during-pregnancy",
                "https://pmc.ncbi.nlm.nih.gov/articles/PMC3865835/",
                "https://kjkhospital.com/breast-pain-during-pregnancy-causes-and-remedies/#:~:text=Breast%20pain%20during%20pregnancy%20is,ways%20to%20relieve%20the%20pain.",
                "https://unmhealth.org/stories/2023/05/how-pregnancy-affects-heart-symptoms-when-to-call-doctor.html#:~:text=Pregnancy%20puts%20additional%20stress%20on,minute%20to%20pump%20more%20blood.",
                "https://epozytywnaopinia.pl/en/Should-household-chemicals-be-avoided-during-pregnancy%3F#:~:text=Domestos%20in%20pregnancy%3A%20the%20harm%20of%20household%20chemicals&text=Household%20chemicals%20such%20as%20Domestos,and%20skin%2C%20penetrates%20the%20body.",
                "https://www.pregnancybirthbaby.org.au/religious-fasting-pregnancy-and-breastfeeding#:~:text=you%20to%20fast.-,Can%20fasting%20harm%20my%20baby%3F,chance%20of%20a%20preterm%20birth.",
                "https://www.medicalnewstoday.com/articles/322316#management",
                "https://obgyn.onlinelibrary.wiley.com/doi/full/10.1002/uog.6328",
                "https://www.babycenter.com/pregnancy/health-and-safety/is-it-safe-to-get-an-x-ray-while-im-pregnant_9214",
                "https://www.ncbi.nlm.nih.gov/books/NBK279575/#:~:text=Women%20who%20gain%20a%20lot,to%20need%20a%20Cesarean%20section.",
                "https://americanpregnancy.org/healthy-pregnancy/is-it-safe/saunas-and-pregnancy/",
                "https://www.medicalnewstoday.com/articles/324941#medications",
                "https://www.parents.com/pregnancy/my-body/is-it-safe/how-to-avoid-hidden-toxins-during-pregnancy/#:~:text=When%20fragrance%20oils%20are%20incorporated,burn%20without%20emitting%20harmful%20chemicals.",
                "https://www.nestdesigns.com/blogs/maternity/when-to-start-wearing-maternity-clothes-the-ultimate-guide",
            ]
            st.session_state.rag_system = ArticleRAG(urls)
            st.session_state.rag_system.initialize()
        except Exception as e:
            st.write(f"Error initializing RAG system: {e}")


initialize_rag_system()
# Streamlit UI
st.title("Pregnancy Q&A Chatbot")
st.write("Ask me questions related to pregnancy, and I will answer using my articles and sources.")
st.write("Please note that it is just a recommendation system. For emergencies, please seek medical help")
pregnancy_weeks = st.selectbox(
    "How many weeks pregnant are you?",
    options=[f"{i} weeks" for i in range(1, 41)],
    index=0
)


# Initialize or continue the conversation
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Text input for user's question
question_key = f"question_input_{len(st.session_state.conversation)}"
question = st.text_area("Ask a question:", key=question_key)

if question and question.lower() != 'exit':
    try:
        rag_system = st.session_state.rag_system
        personalized_question = f"Pregnancy Week {pregnancy_weeks}: {question}"

        with st.spinner('Fetching answer, please wait...'):
            response = rag_system.query(personalized_question)

        # Display the summarized answer
        st.subheader("Answer:")
        st.write(response["answer"])

        # Display the sources used to generate the answer
        st.subheader("Sources:")
        for i, source in enumerate(response['sources'], 1):
            st.write(f"**Source {i}:**")
            st.write(f"URL: {source['url']}")
            st.write(f"Summary: {source['summary']}")
    except KeyError:
        st.write("Error: RAG system not initialized correctly. Please try again.")
    except Exception as e:
        st.write(f"Error while querying: {e}")



    # Save the question and answer in the conversation history
    st.session_state.conversation.append({"question": question, "answer": response["answer"]})

# Display the conversation history so far
if st.session_state.conversation:
    st.subheader("Conversation History:")
    for entry in st.session_state.conversation:
        st.write(f"Q: {entry['question']}")
        st.write(f"A: {entry['answer']}")