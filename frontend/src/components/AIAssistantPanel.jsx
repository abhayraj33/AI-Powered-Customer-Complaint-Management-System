import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { extractComplaintFromText } from '../redux/complaintSlice';

function AIAssistantPanel() {
  const [inputText, setInputText] = useState('');
  const dispatch = useDispatch();

  const extractionStatus = useSelector((state) => state.complaint.extractionStatus);
  const error = useSelector((state) => state.complaint.error);

  const isLoading = extractionStatus === 'loading';

  const handleExtract = () => {
    if (inputText.trim().length < 10) {
      alert('Please paste a complaint text (email, description, etc.)');
      return;
    }
    dispatch(extractComplaintFromText(inputText));
  };

  return (
    <div className="ai-panel">
      <div className="ai-panel-header">
        <span className="ai-icon">✨</span>
        <h2>AI Complaint Intake Assistant</h2>
        <span className="beta-badge">BETA</span>
      </div>

      <textarea
        className="ai-textarea"
        placeholder="Paste complaint text or email here..."
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        rows={8}
      />

      <button
        className="extract-btn"
        onClick={handleExtract}
        disabled={isLoading}
      >
        {isLoading ? 'Analyzing...' : 'Extract Complaint Details'}
      </button>

      {isLoading && (
        <div className="ai-status">
          <div className="progress-bar">
            <div className="progress-fill" />
          </div>
          <p>Analyzing document content and extracting key details...</p>
        </div>
      )}

      {extractionStatus === 'succeeded' && (
        <div className="ai-message success">
          ✅ Extraction complete! Form has been auto-filled — please review the details.
        </div>
      )}

      {extractionStatus === 'failed' && (
        <div className="ai-message error">
          ⚠️ {error || 'Something went wrong during extraction.'}
        </div>
      )}

      {extractionStatus === 'idle' && (
        <div className="ai-message idle">
          💬 Paste a complaint text above and I'll automatically extract the details
          and populate the form for you.
        </div>
      )}
    </div>
  );
}

export default AIAssistantPanel;