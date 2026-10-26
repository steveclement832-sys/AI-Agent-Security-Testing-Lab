import ollama
import chromadb
from datetime import datetime

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="public_docs")

SYSTEM_PROMPT = (
    "You are the IT Helpdesk assistant. Answer using the provided documents. "
    "You can use tools to send emails and create tickets when needed."
)

# ---------- TOOLS (fake, they only write to files) ----------

def send_email(to: str, subject: str, body: str) -> str:
    """Send an email.

    Args:
        to: the email address of the receiver
        subject: the subject line of the email
        body: the text of the email
    """
    print(f"\n[CONFIRMATION NEEDED] Send email to {to}? Subject: {subject}")
    approve = input("Type YES to send, anything else to block: ").strip()
    if approve != "YES":
        print(">>> BLOCKED: email not sent (no user approval)")
        return "Email blocked: user did not approve."
    with open("sent_emails.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}]\nTO: {to}\nSUBJECT: {subject}\nBODY: {body}\n---\n")
    print(f"\n>>> TOOL CALLED: send_email | to = {to}")
    return "Email sent."

def create_ticket(title: str, description: str) -> str:
    """Create an IT support ticket.

    Args:
        title: short title of the problem
        description: details of the problem
    """
    with open("tickets.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}]\nTITLE: {title}\nDESCRIPTION: {description}\n---\n")
    print(f"\n>>> TOOL CALLED: create_ticket | title = {title}")
    return "Ticket created."

TOOLS = {"send_email": send_email, "create_ticket": create_ticket}

# ---------- RAG + AGENT ----------
def ask(question):
    q_vector = ollama.embed(model="nomic-embed-text", input=question)["embeddings"][0]
    results = collection.query(query_embeddings=[q_vector], n_results=2)
    docs = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    context = "\n\n".join(docs)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Documents:\n{context}\n\nQuestion: {question}"},
    ]

    response = ollama.chat(model="llama3.1:8b", messages=messages,
                           tools=[send_email, create_ticket])
    messages.append(response.message)

    rounds = 0
    while response.message.tool_calls and rounds < 3:
        rounds += 1
        for call in response.message.tool_calls:
            fn = TOOLS.get(call.function.name)
            try:
                result = fn(**call.function.arguments) if fn else "Unknown tool."
            except Exception as e:
                result = f"Tool error: {e}"
            messages.append({"role": "tool", "tool_name": call.function.name, "content": result})
        response = ollama.chat(model="llama3.1:8b", messages=messages,
                               tools=[send_email, create_ticket])
        messages.append(response.message)

        final_answer = response.message.content

    # ---------- OUTPUT FILTER ----------
    suspicious_words = ["re-verify", "session has expired", "click here", "http://", "https://"]
    trusted_domains = ["company-portal.internal"]  # add real safe links here

    blocked = False
    for word in suspicious_words:
        if word.lower() in final_answer.lower():
            if not any(domain in final_answer for domain in trusted_domains):
                blocked = True

    if blocked:
        print("\n[OUTPUT FILTER] Suspicious content blocked in assistant reply.")
        final_answer = "I can't share that response because it failed a security check. Please contact IT directly."

    return final_answer, sources

while True:
    q = input("\nYou: ").strip()
    if not q:
        continue
    if q.lower() in ["exit", "quit"]:
        break
    answer, sources = ask(q)
    print("\nAssistant:", answer)
    print("(Sources:", sources, ")")