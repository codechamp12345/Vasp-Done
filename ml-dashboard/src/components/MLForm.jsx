import { useState } from 'react';
import axios from 'axios';

const MLForm = () => {
  const [formData, setFormData] = useState({
    tds: '',
    flow: ''
  });
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const endpoint = apiUrl === '/api' ? '/api/predict' : `${apiUrl}/predict`;
      
      const response = await axios.post(endpoint, {
        tds: parseFloat(formData.tds),
        flow: parseFloat(formData.flow)
      });
      
      setResult(response.data);
      setSubmitted(true);
    } catch (err) {
      if (err.code === 'ERR_NETWORK' || err.message.includes('ERR_CONNECTION_REFUSED')) {
        setError('Cannot connect to the server. Please make sure the Flask API is running on port 5000.');
      } else {
        setError(err.response?.data?.error || 'Failed to get prediction. Please check your inputs and try again.');
      }
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSubmitted(false);
    setFormData({ tds: '', flow: '' });
    setResult(null);
    setError('');
  };

  if (submitted && result) {
    return (
      <div className="ml-results-container">
        <div className="result-header">
          <h2>Hybrid Prediction Results</h2>
          <button className="reset-button" onClick={handleReset}>
            New Prediction
          </button>
        </div>
        
        <div className="result-card final-result">
          <h3>Final Hybrid Prediction</h3>
          <div className="result-item">
            <span className="result-label">PX Power Savings:</span>
            <span className="result-value">{result.final_prediction.px_power_savings.toFixed(2)}</span>
          </div>
          <div className="result-item">
            <span className="result-label">Power Cost Savings:</span>
            <span className="result-value">{result.final_prediction.power_cost_savings.toFixed(2)}</span>
          </div>
        </div>
        
        <div className="visualization-container">
          <div className="gauge-chart">
            <div className="gauge-value">
              <span className="gauge-number">{result.final_prediction.px_power_savings.toFixed(1)}</span>
              <span className="gauge-label">PX Power Savings</span>
            </div>
          </div>
          <div className="gauge-chart cost-savings">
            <div className="gauge-value">
              <span className="gauge-number">{result.final_prediction.power_cost_savings.toFixed(1)}</span>
              <span className="gauge-label">Cost Savings</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="ml-form-container">
      <form className="prediction-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="tds">Permeate TDS:</label>
          <input
            type="number"
            id="tds"
            name="tds"
            value={formData.tds}
            onChange={handleChange}
            placeholder="Enter TDS value"
            required
            step="any"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="flow">Permeate Flow:</label>
          <input
            type="number"
            id="flow"
            name="flow"
            value={formData.flow}
            onChange={handleChange}
            placeholder="Enter Flow value"
            required
            step="any"
          />
        </div>
        
        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? (
            <>
              <span className="loading-spinner"></span>
              Predicting...
            </>
          ) : 'Get Prediction'}
        </button>
      </form>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  );
};

export default MLForm;