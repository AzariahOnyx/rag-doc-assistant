import os
from groq import Groq
import gradio as gr

docs_text = [
    "How to authenticate with Contentstack Personalize API: Use OAuth Bearer token in the Authorization header and your Project UID in the x-project-uid header. Base URL is https://personalize-api.contentstack.com. This applies to all Management API calls for Attributes, Audiences, Events, and Experiences.",
    "How to create and manage Attributes in Personalize: POST to /attributes to create a new attribute. Attributes are user properties used to build Audience rules. Supported types are STRING, NUMBER, and BOOLEAN. Built-in presets include COUNTRY, DEVICE_TYPE, SESSION_COUNT, and PAGE_VIEW_COUNT.",
    "How to create an Audience in Personalize: POST to /audiences with a RuleCombination definition. An Audience is a group of users matched by attribute rules. Supported operators are EQUALS, GREATER_THAN, LESS_THAN, and CONTAINS. Example: target US visitors with order value over 1000.",
    "How to create an Experience in Personalize: POST to /experiences. Experiences define content variations for matched audiences. Two types exist: SEGMENTED (targets a specific audience) and AB_TEST (randomly splits users). Each variant has a shortUid used when fetching content from the CDA.",
    "How to track Events like impressions and conversions in Personalize: POST to https://personalize-edge.contentstack.com/events. Include x-project-uid and x-cs-personalize-user-uid headers. For an impression send type IMPRESSION. For a conversion send the eventKey and type EVENT.",
    "How to use the Personalize Edge API: Base URL is https://personalize-edge.contentstack.com. Use GET /manifest to fetch the experience manifest. Use PUT /user-attributes to set user attributes in real time for audience matching.",
    "How to use the JavaScript Personalize Edge SDK: Install with npm i @contentstack/personalize-edge-sdk. Initialize with await Personalize.init(projectUid). Set user attributes with personalizeSdk.set({age:20}). Call getExperiences() and getVariantAliases() to get the right variant for CDA. Track events with triggerImpression() and triggerEvent().",
    "How the full Personalize integration flow works: 1. Init the SDK 2. Set user attributes 3. Call getVariantAliases() 4. Pass aliases to CDA as the cs-personalize-variant-aliases header 5. CDA returns the personalized entry 6. Track impressions 7. Track conversions. The user is persisted via the cs-personalize-user-uid cookie.",
]

def simple_search(query, docs, n=3):
    query_words = set(query.lower().split())
    scores = [len(query_words & set(doc.lower().split())) for doc in docs]
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [docs[i] for i in ranked[:n]]

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def rag_answer(question, history):
    results = simple_search(question, docs_text, n=3)
    context = "\n".join(results)
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Contentstack Personalize documentation. Answer only using the context provided. If you cannot find the answer in the context, say so clearly."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        max_tokens=300
    )
    answer = response.choices[0].message.content
    sources = list(set([d[:80] + "..." for d in results]))
    source_text = "\n".join(f"- {s}" for s in sources)
    return f"{answer}\n\n---\n**Sources:**\n{source_text}"

demo = gr.ChatInterface(
    fn=rag_answer,
    title="RAG Doc Assistant",
    description="A RAG pipeline built over API documentation. Shows how doc structure affects AI retrieval quality.",
    examples=[
        "How do I create an Audience?",
        "What is the difference between SEGMENTED and AB_TEST?",
        "How do I track a conversion event?",
        "How do I authenticate with the Management API?",
        "What does getVariantAliases() return?",
    ],
)

if __name__ == "__main__":
    demo.launch()
