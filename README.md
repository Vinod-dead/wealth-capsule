# Wealth Capsule



**Privacy-preserving Personal AI for understanding personal finances.**



Wealth Capsule combines financial analysis, persistent memory, NVIDIA Nemotron reasoning, and Tavily-powered public research to help users understand spending patterns and explore budgeting strategies.



The project is designed around a simple principle: **private financial information should remain under the user's control and should not be exposed to external research services.**



## Features



- **Spending analysis:** Review monthly spending and category totals.

- **AI-powered explanations:** Use NVIDIA Nemotron to explain spending patterns and answer financial questions.

- **Current public research:** Use Tavily to discover external budgeting and personal-finance resources.

- **Privacy gateway:** Rewrite research requests into generic public queries and block queries containing detected sensitive information.

- **Persistent memory:** Store application memory locally using SQLite.

- **Research source filtering:** Remove duplicate and irrelevant sources before presenting research results.

- **Financial validation:** Validate financial calculations and responses.

- **Web interface:** Explore the application through a React frontend.



## Technology Stack



- Python and FastAPI

- NVIDIA Nemotron through Nebius Token Factory

- Tavily Search API

- SQLite

- React and Vite

- Pytest

- Docker



## Architecture



1\. The user submits a question through the web interface.

2\. The backend determines whether financial analysis or public research is needed.

3\. Financial calculations use the application's financial data and validation logic.

4\. Research queries pass through the privacy policy before Tavily is called.

5\. Retrieved external content is filtered and sanitized before being used by the AI.

6\. The application returns an answer with relevant research sources when available.



**Privacy boundary:** Tavily should receive only sanitized public research queries, not raw transactions or private financial amounts. The implemented filters and tests provide safeguards, but they are not a guarantee against every possible privacy leak.



## Requirements



- Python 3.11 or later

- Node.js and npm

- Nebius Token Factory API credentials

- Tavily API key



## Setup



### 1. Clone the repository



```bash

git clone <YOUR_PUBLIC_GITHUB_REPOSITORY_URL>

cd "wealth capsule"

```



Replace the placeholder with your repository URL.



### 2. Set up the Python environment



Windows PowerShell:



```powershell

py -3.11 -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

```



### 3. Configure environment variables



Create your local `.env` file using `.env.example` as a reference.



Configure the variable names required by your application, including:



- `TAVILY_API_KEY`

- Your Nebius Token Factory API key



Use the variable names expected by the application code. Never commit `.env` or share API keys publicly.



### 4. Start the backend



From the project root:



```powershell

python -m uvicorn app.main:app --reload

```



The API should be available at:



- Application: `http://127.0.0.1:8000`

- API documentation: `http://127.0.0.1:8000/docs`

- Dashboard endpoint: `http://127.0.0.1:8000/api/dashboard`

- Privacy audit: `http://127.0.0.1:8000/api/privacy-audit`



### 5. Start the frontend



Open a second terminal:



```powershell

cd frontend

npm install

npm run dev

```



Open the local URL printed by Vite, normally `http://localhost:5173`.



## Run Tests



From the project root:



```powershell

python -m pytest tests -v

```



Compile the Python application and tests:



```powershell

python -m compileall -q app tests

```



Build the frontend for production:



```powershell

cd frontend

npm run build

```



## Demo Data



The project uses synthetic demonstration financial data. Do not use real bank statements, account numbers, or personal financial records in a public demo without appropriate safeguards and authorization.



## Limitations and Responsible Use



- This is a demonstration project, not a banking service.

- AI-generated explanations may be incomplete or inaccurate.

- Public research results must be reviewed for relevance and reliability.

- Privacy filters are defense-in-depth safeguards and should be supplemented with testing of actual outbound requests.

- The application does not replace qualified financial advice.



## Hackathon Technology



Wealth Capsule uses NVIDIA Nemotron through Nebius Token Factory and integrates Tavily for external research. The project is intended for the Personal AI track, emphasizing useful assistance, persistent memory, selected tools, and user control over private information.



## License



Add your chosen open-source license before publishing. Ensure the license matches your intended reuse and distribution terms.
