import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { extractFromText, saveComplaint } from '../api/complaintApi';

const initialFormState = {
  complaint_source: '',
  customer_name: '',
  product_name: '',
  product_strength: '',
  batch_number: '',
  manufacturing_date: '',
  expiry_date: '',
  quantity_affected: '',
  complaint_type: '',
  complaint_date: '',
  complaint_description: '',
  initial_severity: '',
  priority: '',
  ai_confidence_notes: '',
};

export const extractComplaintFromText = createAsyncThunk(
  'complaint/extractFromText',
  async (text, { rejectWithValue }) => {
    try {
      const response = await extractFromText(text);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Extraction failed');
    }
  }
);

export const submitComplaint = createAsyncThunk(
  'complaint/submit',
  async (formData, { rejectWithValue }) => {
    try {
      const response = await saveComplaint(formData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data?.detail || 'Save failed');
    }
  }
);

const complaintSlice = createSlice({
  name: 'complaint',
  initialState: {
    formData: initialFormState,
    extractionStatus: 'idle',
    saveStatus: 'idle',
    error: null,
  },
  reducers: {
    updateField: (state, action) => {
      const { field, value } = action.payload;
      state.formData[field] = value;
    },
    resetForm: (state) => {
      state.formData = initialFormState;
      state.extractionStatus = 'idle';
      state.saveStatus = 'idle';
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(extractComplaintFromText.pending, (state) => {
        state.extractionStatus = 'loading';
        state.error = null;
      })
      .addCase(extractComplaintFromText.fulfilled, (state, action) => {
        state.extractionStatus = 'succeeded';
        state.formData = { ...state.formData, ...action.payload };
      })
      .addCase(extractComplaintFromText.rejected, (state, action) => {
        state.extractionStatus = 'failed';
        state.error = action.payload;
      })
      .addCase(submitComplaint.pending, (state) => {
        state.saveStatus = 'loading';
      })
      .addCase(submitComplaint.fulfilled, (state) => {
        state.saveStatus = 'succeeded';
      })
      .addCase(submitComplaint.rejected, (state, action) => {
        state.saveStatus = 'failed';
        state.error = action.payload;
      });
  },
});

export const { updateField, resetForm } = complaintSlice.actions;
export default complaintSlice.reducer;