import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [code, setCode] = useState("");
  const [output, setOutput] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [checkboxes, setCheckboxes] = useState({
    fsoql: false,
    fdml: false,
    fshr: false,
    fcmt: false,
    esoql: false,
  });
  const [selectedPicklist, setSelectedPicklist] = useState("");
  const [error, setError] = useState(null);

  // Fetch output when form is submitted
  useEffect(() => {
    const fetchOutput = async () => {
      try {
        const response = await axios.get("http://localhost:5000/output-file");
        setOutput(response.data);
      } catch (error) {
        console.error("Error fetching output file:", error);
        setError("Failed to fetch output. Please try again later.");
      }
    };

    if (submitted) {
      fetchOutput();
      setSubmitted(false);
    }
  }, [submitted]);

  // Handle checkbox changes
  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckboxes((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  // Handle picklist changes
  const handlePicklistChange = (e) => {
    setSelectedPicklist(e.target.value);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/submit-code", {
        code,
        checkboxes,
        selectedPicklist,
      });
      setSubmitted(true);
      setError(null);
    } catch (error) {
      console.error("Error submitting code:", error);
      setError("Failed to submit code. Please try again.");
    }
  };

  // Handle file download
  const handleDownload = () => {
    if (!output) return;

    const element = document.createElement("a");
    const file = new Blob([output], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = "output.txt";
    document.body.appendChild(element);
    element.click();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Salesforce Security Fixer</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-container">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="Enter your code here"
              className="textarea-code"
            ></textarea>
            <div className="options-container">
              <div className="checkbox-container">
                <label>
                  <input
                    type="checkbox"
                    name="fsoql"
                    checked={checkboxes.fsoql}
                    onChange={handleCheckboxChange}
                  />
                  Fix SOQL FLS
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="fdml"
                    checked={checkboxes.fdml}
                    onChange={handleCheckboxChange}
                  />
                  Fix DML FLS
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="fshr"
                    checked={checkboxes.fshr}
                    onChange={handleCheckboxChange}
                  />
                  Enforce Sharing Rule
                </label>
              </div>
              <div className="picklist-container">
                <select
                  value={selectedPicklist}
                  onChange={handlePicklistChange}
                >
                  <option value="">Select Sharing</option>
                  <option value="with">With Sharing</option>
                  <option value="without">Without Sharing</option>
                  <option value="inherited">Inherited Sharing</option>
                </select>
              </div>
              <div className="checkbox-container">
                <label>
                  <input
                    type="checkbox"
                    name="fcmt"
                    checked={checkboxes.fcmt}
                    onChange={handleCheckboxChange}
                  />
                  Comment Debugs
                </label>
                <label>
                  <input
                    type="checkbox"
                    name="esoql"
                    checked={checkboxes.esoql}
                    onChange={handleCheckboxChange}
                  />
                  Extract SOQL Queries
                </label>
              </div>
            </div>
            <textarea
              value={output}
              readOnly
              placeholder="Output will be displayed here"
              className="textarea-output"
            ></textarea>
          </div>
          <div className="submit-container">
            <p>App Development still In progress</p>
            {error && <p className="error-message">{error}</p>}
            <button type="submit" className="submit-button">
              Submit
            </button>
            <button
              type="button"
              onClick={handleDownload}
              className={`download-button ${!output ? "disabled" : ""}`}
              disabled={!output}
            >
              Download
            </button>
          </div>
        </form>
      </header>
    </div>
  );
}

export default App;
