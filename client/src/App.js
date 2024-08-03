import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  // State to hold the code input by the user
  const [code, setCode] = useState("");
  // State to hold the output received from the server
  const [output, setOutput] = useState("");
  // State to track if the form has been submitted
  const [submitted, setSubmitted] = useState(false);
  // State for the checkboxes
  const [checkboxes, setCheckboxes] = useState({
    fsoql: false,
    fdml: false,
    fshr: false,
    fcmt: false,
    esoql: false,
  });
  // State for the selected picklist option
  const [selectedPicklist, setSelectedPicklist] = useState("");

  // useEffect hook to fetch the output file when the form is submitted
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
    if (submitted) {
      fetchOutput();
    }
  }, [submitted]);

  // Handle changes to checkboxes
  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setCheckboxes((prevState) => ({
      ...prevState,
      [name]: checked,
    }));
  };

  // Handle changes to the picklist
  const handlePicklistChange = (e) => {
    setSelectedPicklist(e.target.value);
    console.log("Picklist selected:", e.target.value);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/submit-code", {
        code,
        checkboxes,
        selectedPicklist,
      });
      console.log("checkboxes", checkboxes);
      console.log("Code submitted successfully:", response.data);
      setSubmitted(!submitted); // Toggle the submitted state to trigger useEffect
    } catch (error) {
      console.error("There was an error submitting the code:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Salesforce Security Fixer</h1>
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
              style={{ height: "70vh", width: "35vw", marginRight: "10px" }}
            ></textarea>
            <div style={{ margin: "20px" }}>
              <input
                type="checkbox"
                id="fsoql"
                name="fsoql"
                checked={checkboxes.fsoql}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="fsoql">Fix SOQL FLS</label>
              <br />
              <input
                type="checkbox"
                id="fdml"
                name="fdml"
                checked={checkboxes.fdml}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="fdml">Fix DML FLS</label>
              <br />
              <input
                type="checkbox"
                id="fshr"
                name="fshr"
                checked={checkboxes.fshr}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="fshr">Enforce Sharing Rule</label>
              <br />
              <div>
                <select
                  htmlFor="picklist"
                  id="picklist"
                  value={selectedPicklist}
                  onChange={handlePicklistChange}
                >
                  <option value="">Select Sharing</option>
                  <option value="with">With Sharing</option>
                  <option value="without">Without Sharing</option>
                  <option value="inherited">Inherited Sharing</option>
                </select>
              </div>
              <br />
              <input
                type="checkbox"
                id="fcmt"
                name="fcmt"
                checked={checkboxes.fcmt}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="fcmt">Comment Debugs</label>
              <br />
              <input
                type="checkbox"
                id="esoql"
                name="esoql"
                checked={checkboxes.esoql}
                onChange={handleCheckboxChange}
              />
              <label htmlFor="esoql">Extract SOQL Queries</label>
            </div>
            <textarea
              value={output}
              readOnly
              placeholder="Output will be displayed here"
              style={{ height: "70vh", width: "35vw" }}
            ></textarea>
            <br />
          </div>
          <div style={{ alignSelf: "center" }}>
            App Development still Inprogress
            <br />
            <button type="submit">Submit Code</button>
          </div>
        </form>
      </header>
    </div>
  );
}

export default App;
