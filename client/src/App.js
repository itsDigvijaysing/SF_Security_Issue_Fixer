import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");

  useEffect(() => {
    const fetchOutput = async () => {
      try {
        console.log("Fetching output file...");
        const response = await axios.get("http://localhost:5000/output-file");
        setOutput(response.data);
      } catch (error) {
        console.error("There was an error fetching the output file:", error);
      }
    };
    fetchOutput();
  }, [output]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/submit-code", {
        code,
      });
      console.log("Code submitted successfully:", response.data);
    } catch (error) {
      console.error("There was an error submitting the code:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Code Submitter</h1>
        <form onSubmit={handleSubmit} style={{ display: "flex" }}>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Enter your code here"
            style={{ height: "75vh", width: "40vw", marginRight: "10px" }}
          ></textarea>
          <textarea
            value={output}
            readOnly
            placeholder="Output will be displayed here"
            style={{ height: "75vh", width: "40vw" }}
          ></textarea>
          <br />
          <button type="submit">Submit Code</button>
        </form>
      </header>
    </div>
  );
}

export default App;
