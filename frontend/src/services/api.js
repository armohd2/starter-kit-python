import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
});

export const uploadReceipt = (file) => {
  const formData = new FormData();
  formData.append("receipt", file);
  return api.post("/receipts", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getReceipts = () => api.get("/receipts");

export const getInsights = () => api.get("/insights");
