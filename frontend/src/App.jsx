import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [patentId, setPatentId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [result, setResult] = useState([]);
  const check_url = "http://localhost:8000/check_patent"

  const checkPatent = async () => {
    try {
      const response = await axios.get(`${check_url}?patentId=${patentId}&companyName=${companyName}`);
      setResult(response.data);
    } catch (error) {
      console.error("Error when fetch api: ", error.message);
    }
  }

  return (
    <>
      <h1 style={{color: "green"}}>Mini patent infringement check system</h1>
      <div className='input-form'>
        <label>Patent ID: </label>
        <input style={{marginRight: 15}} value={patentId} onChange={(e) => setPatentId(e.target.value)} />
        <label>Company name: </label>
        <input style={{marginRight: 15}} value={companyName} onChange={(e) => setCompanyName(e.target.value)} />
        <button onClick={checkPatent}>Check</button>
      </div>
      <div style={{maxWidth:'960px', alignItems: "center", margin:'0 auto'}}>
        <h2>Result</h2>
        {result && <p>Analysis Id: {result.analysis_id}</p>}
        {result && result.status === "failed" && <p> {result.error} </p>}
        {
          result && result.status === "success" && (
            <div>
              {result.top_infringing_products &&
                result.top_infringing_products.map((item, index) => (
                  <div key={index} style={{ border: '1px solid skyblue', padding: '5px', margin: '10px',  borderRadius: '5px' }}>
                    <h4>Product Name: {item.product_name}</h4>
                    <p><strong>Infringement Likelihood:</strong> {item.infringement_likelihood}</p>
                    <p><strong>Relevant Claims:</strong> {item.relevant_claims.join(', ')}</p>
                    <p style={{textAlign: 'left', margin:'10px'}}><strong>Explanation:</strong> {item.explanation}</p>
                    <p style={{textAlign: 'left', margin:'10px'}}><strong>Specific features:</strong></p>
                    <div>
                      {item.specific_features && item.specific_features.map((feature, idx) => (
                        <p style={{textAlign: 'left', margin: '5px 30px'}} key={idx}>{feature}</p>
                      ))}
                    </div>
                      
                  </div>
                ))}
              <p style={{paddingBottom: '100px', textAlign: 'left'}}><strong>Overall Risk Assessment:</strong> {result.overall_risk_assessment}</p>
            </div>
          )
        }
      </div>
    </>
  )
}

export default App
