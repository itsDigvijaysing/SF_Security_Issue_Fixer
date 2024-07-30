import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [submitted, setSubmitted] = useState(false);

  // State for the checkboxes
  const [checkboxes, setCheckboxes] = useState({
    checkbox1: false,
    checkbox2: false,
    checkbox3: false,
    checkbox4: false,
    checkbox5: false,
  });

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
  }, [submitted]);

  // Handle changes to checkboxes
  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckboxes((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/submit-code", {
        code,
      });
      console.log("Code submitted successfully:", response.data);
      setSubmitted(!submitted); // Toggle the submitted state to trigger useEffect
    } catch (error) {
      console.error("There was an error submitting the code:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Code Submitter</h1>
        <form onSubmit={handleSubmit}>
          <div
            style={{
              display: "flex",
            }}
          >
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Enter your code here"
              style={{ height: "45vh", width: "15vw", marginRight: "10px" }}
            ></textarea>
            <div style={{ margin: "20px" }}>
              <input
                type="checkbox"
                id="checkbox1"
                name="checkbox1"
                checked={checkboxes.checkbox1}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="checkbox1">Fix SOQL FLS</label>
              <br />
              <input
                type="checkbox"
                id="checkbox2"
                name="checkbox2"
                checked={checkboxes.checkbox2}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="checkbox2">Fix DML FLS</label>
              <br />
              <input
                type="checkbox"
                id="checkbox3"
                name="checkbox3"
                checked={checkboxes.checkbox3}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="checkbox3">Enforce Sharing Rule</label>
              <br />
              <input
                type="checkbox"
                id="checkbox4"
                name="checkbox4"
                checked={checkboxes.checkbox4}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="checkbox4">Comment Debugs</label>
              <br />
              <input
                type="checkbox"
                id="checkbox5"
                name="checkbox5"
                checked={checkboxes.checkbox5}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="checkbox5">Extract SOQL Queries</label>
            </div>
            <textarea
              value={output}
              readOnly
              placeholder="Output will be displayed here"
              style={{ height: "45vh", width: "15vw" }}
            ></textarea>
            <br />
          </div>
          <div style={{ alignSelf: "center" }}>
            <button type="submit">Submit Code</button>
          </div>
        </form>
      </header>
    </div>
  );
}

export default App;
