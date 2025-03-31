import React, { useState } from "react";

const predefinedSkills = [
  "Python course work",
  "Software Engineering course work",
  "Agile course",
  "3 years Python development",
  "1 year data development",
  "Experience in Agile projects",
  "Used Git",
  "3 years managing software projects",
  "2 years in Agile projects",
  "3 years using Python to develop Expert Systems",
  "2 years data architecture and development"
];

const predefinedQualifications = [
  "Bachelor in CS",
  "PMI Lean Project Management Certification",
  "Masters in CS"
];

const App = () => {
  const [skills, setSkills] = useState("");
  const [qualifications, setQualifications] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);
    
    const formattedSkills = skills.split(",").map(skill => skill.trim());
    
    try {
      const response = await fetch("https://expert-system-801f.onrender.com/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills: formattedSkills, qualifications }),
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Error connecting to the server. Please try again.");
    }
  };

  return (
    <div style={{ backgroundColor: "#ffb6c1", minHeight: "100vh", display: "flex", justifyContent: "center", alignItems: "center" }}>
      <div style={{ background: "white", padding: "20px", borderRadius: "10px", boxShadow: "0 0 10px rgba(0,0,0,0.1)", width: "400px", textAlign: "center" }}>
        <h2 style={{ color: "#d63384" }}>Job Qualification Check</h2>
        <div style={{ textAlign: "left", marginBottom: "10px" }}>
          <h4>Available Skills:</h4>
          <p>{predefinedSkills.join(", ")}</p>
          <h4>Available Qualifications:</h4>
          <p>{predefinedQualifications.join(", ")}</p>
        </div>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "10px" }}>
            <label>Skills (comma-separated):</label>
            <input 
              type="text" 
              value={skills} 
              onChange={(e) => setSkills(e.target.value)} 
              required 
              style={{ width: "100%", padding: "5px", border: "1px solid #d63384", borderRadius: "5px" }}
            />
          </div>
          <div style={{ marginBottom: "10px" }}>
            <label>Qualifications:</label>
            <input 
              type="text" 
              value={qualifications} 
              onChange={(e) => setQualifications(e.target.value)} 
              required 
              style={{ width: "100%", padding: "5px", border: "1px solid #d63384", borderRadius: "5px" }}
            />
          </div>
          <button type="submit" style={{ backgroundColor: "#d63384", color: "white", padding: "10px", border: "none", borderRadius: "5px", cursor: "pointer" }}>Submit</button>
        </form>
        {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
        {result && (
          <div style={{ marginTop: "20px" }}>
            <h3>Result:</h3>
            {result.status === "Accepted" ? (
              <p style={{ color: "green" }}>Accepted for: {result.positions.join(", ")}</p>
            ) : (
              <p style={{ color: "red" }}>Rejected - {result.reason}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;