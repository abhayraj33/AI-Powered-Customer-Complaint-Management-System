import { useDispatch, useSelector } from 'react-redux';
import { updateField, resetForm, submitComplaint } from '../redux/complaintSlice';

const COMPLAINT_TYPES = ['Packaging Issue', 'Quality Defect', 'Delivery Issue', 'Contamination', 'Labeling Error', 'Other'];
const SEVERITY_LEVELS = ['Critical', 'Major', 'Minor'];
const PRIORITY_LEVELS = ['High', 'Medium', 'Low'];

function ComplaintForm() {
  const dispatch = useDispatch();
  const formData = useSelector((state) => state.complaint.formData);
  const saveStatus = useSelector((state) => state.complaint.saveStatus);

  const handleChange = (field, value) => {
    dispatch(updateField({ field, value }));
  };

  const handleSave = () => {
    dispatch(submitComplaint(formData));
  };

  const handleReset = () => {
    dispatch(resetForm());
  };

  return (
    <div className="complaint-form">
      <div className="form-header">
        <div>
          <h1>Log Customer Complaint</h1>
          <p className="subtitle">API &amp; FDF Quality Assurance Module</p>
        </div>
        <span className="status-badge">Pending Triage</span>
      </div>

      <fieldset>
        <legend>1. Origin &amp; Customer Details</legend>
        <div className="field-row">
          <Field label="Complaint Source" value={formData.complaint_source}
            onChange={(v) => handleChange('complaint_source', v)} />
          <Field label="Customer Name" value={formData.customer_name}
            onChange={(v) => handleChange('customer_name', v)} />
        </div>
      </fieldset>

      <fieldset>
        <legend>2. Product &amp; Batch Identification</legend>
        <div className="field-row">
          <Field label="Product Name" value={formData.product_name}
            onChange={(v) => handleChange('product_name', v)} />
          <Field label="Product Strength/Grade" value={formData.product_strength}
            onChange={(v) => handleChange('product_strength', v)} />
        </div>
        <div className="field-row">
          <Field label="Batch/Lot Number" value={formData.batch_number}
            onChange={(v) => handleChange('batch_number', v)} />
          <Field label="Manufacturing Date" value={formData.manufacturing_date}
            onChange={(v) => handleChange('manufacturing_date', v)} />
        </div>
        <div className="field-row">
          <Field label="Expiry Date" value={formData.expiry_date}
            onChange={(v) => handleChange('expiry_date', v)} />
          <Field label="Quantity Affected" value={formData.quantity_affected}
            onChange={(v) => handleChange('quantity_affected', v)} />
        </div>
      </fieldset>

      <fieldset>
        <legend>3. Complaint Details</legend>
        <div className="field-row">
          <SelectField label="Complaint Type" value={formData.complaint_type}
            options={COMPLAINT_TYPES}
            onChange={(v) => handleChange('complaint_type', v)} />
          <Field label="Complaint Date" value={formData.complaint_date}
            onChange={(v) => handleChange('complaint_date', v)} />
        </div>
        <div className="field-column">
          <label>Detailed Complaint Description</label>
          <textarea
            value={formData.complaint_description || ''}
            onChange={(e) => handleChange('complaint_description', e.target.value)}
            rows={4}
            placeholder="Awaiting AI extraction..."
          />
        </div>
      </fieldset>

      <fieldset>
        <legend>4. Initial Assessment &amp; Priority</legend>
        <div className="field-row">
          <SelectField label="Initial Severity" value={formData.initial_severity}
            options={SEVERITY_LEVELS}
            onChange={(v) => handleChange('initial_severity', v)} />
          <SelectField label="Priority" value={formData.priority}
            options={PRIORITY_LEVELS}
            onChange={(v) => handleChange('priority', v)} />
        </div>
      </fieldset>

      <div className="form-actions">
        <button className="btn-secondary" onClick={handleReset}>↺ Reset Form</button>
        <button className="btn-primary" onClick={handleSave} disabled={saveStatus === 'loading'}>
          💾 {saveStatus === 'loading' ? 'Saving...' : 'Save Complaint'}
        </button>
      </div>

      {saveStatus === 'succeeded' && (
        <p className="save-success">✅ Complaint saved successfully!</p>
      )}
    </div>
  );
}

function Field({ label, value, onChange }) {
  return (
    <div className="field">
      <label>{label}</label>
      <input
        type="text"
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Awaiting AI extraction..."
      />
    </div>
  );
}

function SelectField({ label, value, options, onChange }) {
  return (
    <div className="field">
      <label>{label}</label>
      <select value={value || ''} onChange={(e) => onChange(e.target.value)}>
        <option value="">Awaiting AI extraction...</option>
        {options.map((opt) => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
    </div>
  );
}

export default ComplaintForm;