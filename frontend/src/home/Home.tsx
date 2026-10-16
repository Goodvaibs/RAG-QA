import { useState } from "react";
import "./Home.css";
import { useNavigate } from "react-router-dom";

function Home() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState("");
  const [showSpinner, setShowSpinner] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setShowSpinner(true);
      const res = await fetch("http://127.0.0.1:8000/api/v1/ask-question", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: question }),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`${res.status} ${res.statusText}: ${text}`);
      }
      const data = await res.json();
      console.log("returned data:", data);
      setResult(data.result);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setShowSpinner(false);
    }
  };
  return (
    <div className="askme-page">
      <div className="askme-header">
        <h2>RAG Q&A system</h2>
        <p>Have medical queries? Ask away!</p>
      </div>
      <div className="askme-card">
        <form onSubmit={handleSubmit}>
          <label htmlFor="question">Your question</label>
          <input
            type="text"
            placeholder="Type your question"
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button type="submit">Get Answer</button>
        </form>
      </div>
      {showSpinner && (
        <div className="askme-spinner">
          <div className="spinner"></div>
        </div>
      )}
      <div className="askme-answer">
        <h2>Answer</h2>
        <div className="askme-answer-box">
          <p>{result}</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
