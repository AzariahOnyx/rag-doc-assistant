import os
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import gradio as gr

# ── Docs ──────────────────────────────────────────────────────────────────────
docs_text = [
    "Contentstack Personalize Management API manages Attributes, Audiences, Events, and Experiences. Base URL: https://personalize-api.contentstack.com. Authentication: OAuth Bearer token against authorization header, Project UID against x-project-uid header.",
    "Personalize Attributes are user properties used to build Audience rules. Types: STRING, NUMBER, BOOLEAN. Create: POST /attributes. Presets: COUNTRY, DEVICE_TYPE, SESSION_COUNT, PAGE_VIEW_COUNT.",
    "Personalize Audiences are groups of users. Create: POST /audiences with RuleCombination definition. Operators: EQUALS, GREATER_THAN, LESS_THAN, CONTAINS. Example: US visitors with order value over 1000.",
    "Personalize Experiences create content variations. Types: SEGMENTED and AB_TEST. Create: POST /experiences. Variants have shortUid used with CDA. AB_TEST randomly splits users.",
    "Personalize Events: Impressions and Conversions. Track via Edge API: POST https://personalize-edge.contentstack.com/events. Headers: x-project-uid, x-cs-personalize-user-uid. Impression: type IMPRESSION. Conversion: eventKey + type EVENT.",
    "Personalize Edge API Base URL: https://personalize-edge.contentstack.com. Get Manifest: GET /manifest. Set User Attributes: PUT /user-attributes. Drives audience matching in real time.",
    "JavaScript Personalize Edge SDK: npm i @contentstack/personalize-edge-sdk. Init: await Personalize.init(projectUid). Set attrs: personalizeSdk.set({age:20}). getExperiences(). getVariantAliases() for CDA. triggerImpression(). triggerEvent().",
    "Personalize integration flow: 1.Init SDK 2.Set user attributes 3.getVariantAliases() 4.Pass to CDA as cs-personalize-variant-aliases header 5.CDA returns personalized entry 6.Track impressions 7.Track conversions. User persisted via cs-personalize-user-uid cookie.",
]

# ── Build vector store ─────────────────────────────────────────────────────────
chroma_client = chromadb.Client()
default_ef = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.create_collection(
    name="personalize-docs",
    embedding_function=default_ef
)

chunks = []
for i, doc in enumerate(docs_text):
    words = doc.split(". ")
    chunk = ""
    chunk_id = 0
    for w in words:
        if len(chunk) + len(w) < 200:
            chunk += w + ". "
        else:
            if chunk:
                chunks.append({"id": f"{i}_{chunk_id}", "text": chunk.strip()})
                chunk_id += 1
            chunk = w + ". "
    if chunk:
        chunks.append({"id": f"{i}_{chunk_id}", "text": chunk.strip()})

collection.add(
    documents=[c["text"] for c in chunks],
    ids=[c["id"] for c in chunks]
)

# ── Groq client ───────────────────────────────────────────────────────────────
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def rag_answer(question, history):
    results = collection.query(query_texts=[question], n_results=3)
    context = "\n".join(results["documents"][0])

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for Contentstack Personalize documentation. Answer only using the context provided. If you cannot find the answer in the context, say so clearly."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ],
        max_tokens=300
    )

    answer = response.choices[0].message.content
    sources = list(set([d[:80] + "..." for d in results["documents"][0]]))
    source_text = "\n".join(f"- {s}" for s in sources)
    return f"{answer}\n\n---\n**Sources:**\n{source_text}"

# ── Gradio UI ─────────────────────────────────────────────────────────────────
demo = gr.ChatInterface(
    fn=rag_answer,
    title="Contentstack Personalize RAG Assistant",
    description="Ask anything about Contentstack Personalize. Answers grounded in real docs.",
    examples=[
        "How do I create an Audience?",
        "What is the difference between SEGMENTED and AB_TEST?",
        "How do I track a conversion event?",
        "How do I authenticate with the Management API?",
        "What does getVariantAliases() return?",
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    demo.launch()
