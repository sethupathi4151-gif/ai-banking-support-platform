# 🏦 AI Banking Support & Resolution Platform

An AI-powered banking customer support and resolution platform that combines **LLM-based classification, RAG, risk detection, customer 360° information, response validation, MCP tools, Human-in-the-Loop approval, LangGraph orchestration, FastAPI, PostgreSQL/Neon, and n8n automation**.

The platform is designed to automatically understand customer requests, retrieve relevant banking knowledge, assess risk and priority, generate safe responses, and perform actions for high-risk cases only after human approval.

---

## 🚀 Key Features

### 1. Customer 360° View

Provides a unified view of a banking customer, including:

- Customer profile
- Account information
- Account balance
- Account status
- Transaction history
- Support ticket history
- Customer risk level

Example:

```text
Customer
   │
   ├── Profile
   │
   ├── Accounts
   │
   ├── Transactions
   │
   └── Support Tickets
```

Customer 360° data is retrieved from PostgreSQL/Neon.

---

### 2. Automatic Priority & Risk Detection

The platform automatically evaluates banking requests using deterministic risk rules.

Risk factors include:

- High-value transactions
- Duplicate transactions
- Fraud-related requests
- Unauthorized transactions
- Transaction disputes
- Existing customer risk level

The system determines:

```text
Priority → LOW / MEDIUM / HIGH

Risk → LOW / MEDIUM / HIGH
```

Example:

```text
Duplicate Transaction
        ↓
Risk Detection
        ↓
HIGH RISK
        ↓
Human Approval Required
```

---

### 3. Router / Classification Agent

The Router Agent uses Gemini to classify customer requests into banking categories.

Supported categories:

- `TRANSACTION_DISPUTE`
- `FRAUD`
- `ACCOUNT`
- `CARD`
- `LOAN`
- `PAYMENT`
- `GENERAL`

The agent also determines the initial request priority.

---

### 4. Banking Knowledge RAG

The platform uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from the banking knowledge base.

Technology:

- ChromaDB
- Gemini Embeddings
- LangChain
- Document chunking and similarity search

Knowledge sources include:

```text
data/knowledge_base/
├── banking_faq.txt
├── company_policies.txt
└── refund_policy.txt
```

This helps the AI generate responses based on known banking policies instead of relying only on the LLM's general knowledge.

---

### 5. Response Generation Agent

The Response Agent uses Gemini to generate professional customer responses.

The response is based on:

- Customer request
- Detected category
- Priority
- Retrieved banking knowledge
- Customer context where applicable

The agent is instructed not to invent banking policies or falsely claim that an action has been completed.

---

### 6. Validation / Quality Agent

Every generated response is validated before an action is performed.

The Validation Agent checks whether the response is:

- Relevant
- Safe
- Accurate
- Supported by the banking knowledge
- Consistent with banking policies

Example:

```text
Generated Response
        ↓
Validation Agent
        ↓
VALID = YES
        ↓
Continue Workflow
```

---

### 7. Human-in-the-Loop

High-risk banking cases require human approval before an action is performed.

Example:

```text
Customer Request
       ↓
Risk Detection
       ↓
HIGH RISK
       ↓
Human Approval
       ↓
MCP Action
```

This prevents sensitive banking actions from being performed automatically without human oversight.

---

### 8. MCP Action / Tool Integration

The platform uses MCP tools to perform banking support actions.

Current MCP capabilities include:

- Customer lookup
- Support ticket creation
- Support ticket status update

Example:

```text
Validated High-Risk Request
          ↓
     Human Approval
          ↓
      MCP Action
          ↓
   Support Ticket Created
```

---

### 9. n8n Workflow Automation

n8n is used to automate communication with the banking support API.

Current workflow:

```text
Customer Request
       ↓
n8n Webhook
       ↓
HTTP Request
       ↓
FastAPI Support API
       ↓
LangGraph AI Workflow
       ↓
Response / Human Approval
       ↓
n8n Response
```

This allows external systems to trigger the AI banking support workflow through a webhook.

---

## 🧠 AI Workflow Architecture

The main LangGraph workflow is:

```text
Customer Request
       ↓
Customer 360
       ↓
Router / Classification Agent
       ↓
Risk & Priority Detection
       ↓
Banking Knowledge RAG
       ↓
Response Agent
       ↓
Validation Agent
       ↓
     ┌───────────────┐
     │ High Risk?    │
     └───────┬───────┘
          YES│       │NO
             ↓       ↓
      Human Approval  MCP / Action
             ↓       ↓
          MCP Action
             ↓
       Support Ticket
```

---

## 🏗️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| LangGraph | AI workflow orchestration |
| LangChain | LLM and RAG integration |
| Gemini | Large Language Model |
| ChromaDB | Vector database |
| PostgreSQL | Relational database |
| Neon | Cloud PostgreSQL |
| MCP | Tool/action integration |
| n8n | Workflow automation |
| Docker | Containerization |
| SQLAlchemy | Database connectivity |
| Pydantic | Request validation |
| Git / GitHub | Version control |

---

## 📁 Project Structure

```text
ai-banking-support-platform/
│
├── app/
│   ├── agents/
│   │   ├── router_agent.py
│   │   ├── risk_agent.py
│   │   ├── rag_agent.py
│   │   ├── response_agent.py
│   │   ├── validation_agent.py
│   │   └── banking_workflow.py
│   │
│   ├── api/
│   │   ├── customer.py
│   │   ├── risk.py
│   │   └── support.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── customer_service.py
│   │   ├── models.py
│   │   └── seed.py
│   │
│   ├── mcp/
│   │   └── server.py
│   │
│   ├── rag/
│   │
│   ├── config/
│   │
│   └── main.py
│
├── data/
│   └── knowledge_base/
│       ├── banking_faq.txt
│       ├── company_policies.txt
│       └── refund_policy.txt
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .env
├── requirements.txt
└── README.md
```

---

## 🗄️ Database

The application uses PostgreSQL hosted on Neon.

### Main Tables

```text
customers
    │
    ├── accounts
    │
    └── support_tickets


accounts
    │
    └── transactions
```

### Customers

Stores:

- Customer ID
- Customer code
- Name
- Email
- Phone
- Risk level

### Accounts

Stores:

- Account number
- Account type
- Balance
- Account status

### Transactions

Stores:

- Transaction reference
- Transaction type
- Amount
- Merchant
- Transaction status
- Location
- Transaction time

### Support Tickets

Stores:

- Ticket ID
- Customer
- Subject
- Description
- Category
- Priority
- Risk level
- Status
- AI confidence
- Created time

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=your_neon_postgresql_connection_string
GOOGLE_API_KEY=your_gemini_api_key
```

Do not commit the `.env` file to GitHub.

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/sethupathi4151-gif/ai-banking-support-platform.git
cd ai-banking-support-platform
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` and add:

```env
DATABASE_URL=your_neon_postgresql_connection_string
GOOGLE_API_KEY=your_gemini_api_key
```

### 5. Seed the database

```powershell
python -m app.database.seed
```

### 6. Start the FastAPI application

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker Setup

The application can also be started using Docker Compose.

```powershell
docker compose up --build
```

Check running containers:

```powershell
docker compose ps
```

Stop the application:

```powershell
docker compose down
```

View API logs:

```powershell
docker compose logs --tail 80 api
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /
```

Returns:

```json
{
  "message": "AI Banking Support & Resolution Platform is running"
}
```

---

### Customer 360

```http
GET /customers/{customer_code}
```

Example:

```text
GET /customers/CUST001
```

Returns customer information, accounts, transactions, and support tickets.

---

### Risk Assessment

```http
POST /risk/assess
```

Example request:

```json
{
  "customer_code": "CUST001",
  "category": "TRANSACTION_DISPUTE",
  "amount": 50000,
  "duplicate_transaction": true
}
```

---

### AI Banking Support

```http
POST /support/chat
```

Example:

```json
{
  "customer_code": "CUST001",
  "message": "I was charged Rs.5000 twice for the same Amazon purchase.",
  "amount": 5000,
  "duplicate_transaction": true,
  "thread_id": "demo-thread-001"
}
```

A high-risk case returns:

```json
{
  "status": "HUMAN_APPROVAL_REQUIRED"
}
```

---

### Human Approval

```http
POST /support/approve
```

Example:

```json
{
  "thread_id": "demo-thread-001",
  "approved": true
}
```

After approval, the workflow continues and the MCP action can create the support ticket.

---

## 🔄 Example: Normal Banking Request

Customer:

```text
What is my account balance?
```

Workflow:

```text
Customer Request
       ↓
Customer 360
       ↓
ACCOUNT Classification
       ↓
LOW Risk
       ↓
RAG
       ↓
Response Agent
       ↓
Validation
       ↓
Completed
```

---

## 🚨 Example: High-Risk Transaction Dispute

Customer:

```text
I was charged Rs.5000 twice for the same Amazon purchase.
```

Workflow:

```text
Customer Request
       ↓
TRANSACTION_DISPUTE
       ↓
Risk Detection
       ↓
HIGH Priority
       ↓
HIGH Risk
       ↓
RAG
       ↓
Response Agent
       ↓
Validation
       ↓
Human Approval Required
       ↓
Approved
       ↓
MCP Action
       ↓
Support Ticket Created
```

---

## 🧪 Testing

The platform has been tested for:

- Customer 360 retrieval
- Customer lookup
- Account information requests
- Transaction dispute classification
- Risk detection
- Duplicate transaction detection
- RAG retrieval
- AI response generation
- Response validation
- Human approval workflow
- MCP support ticket creation
- Ticket status updates
- FastAPI endpoints
- n8n webhook integration
- Docker API container

---

## 🔗 n8n Integration

The n8n workflow uses:

```text
Webhook
   ↓
HTTP Request
   ↓
Respond to Webhook
```

Example webhook endpoint during local testing:

```text
http://localhost:5678/webhook-test/banking-support
```

The webhook forwards customer requests to:

```text
POST /support/chat
```

The FastAPI backend then executes the LangGraph banking workflow.

---

## 🛡️ Safety & Validation

The platform follows several safety principles:

- Sensitive banking information requires verification.
- High-risk cases require human approval.
- Duplicate and unauthorized transactions require investigation.
- The AI does not claim that refunds have been completed without an actual action.
- Responses are validated against the banking knowledge base.
- Business rules are used for risk detection rather than relying entirely on LLM decisions.

---

## 🎯 Project Objective

The objective of this project is to demonstrate how modern AI technologies can be combined to build a reliable banking customer support platform.

The system combines:

```text
LLM
+
RAG
+
LangGraph
+
MCP
+
Human-in-the-Loop
+
FastAPI
+
PostgreSQL
+
n8n
+
Docker
```

to create an end-to-end AI banking support and resolution workflow.

---

## 👨‍💻 Author

**Sethupathi M.**

AI Banking Support & Resolution Platform
