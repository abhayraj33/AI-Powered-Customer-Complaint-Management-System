import axios from 'axios';

// Backend jaha chal raha hai
const API_BASE_URL = 'http://localhost:8000/api/complaints';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Text se extraction (jab user paste kare)
export const extractFromText = async (text) => {
  const response = await api.post('/extract-from-text', { text });
  return response.data;
};

// File se extraction (jab user PDF/DOCX upload kare)
export const extractFromFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post(`${API_BASE_URL}/extract-from-file`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

// Complaint save karna
export const saveComplaint = async (complaintData) => {
  const response = await api.post('/', complaintData);
  return response.data;
};

// Saari complaints list karna (dashboard ke liye)
export const listComplaints = async () => {
  const response = await api.get('/');
  return response.data;
};