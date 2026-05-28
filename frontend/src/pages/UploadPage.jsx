import { useState, useRef } from "react";
import { uploadReceipt } from "../services/api";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null); // null | 'uploading' | 'success' | 'error'
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef();

  const handleFile = (f) => {
    if (f && (f.type.startsWith("image/") || f.type === "application/pdf")) {
      setFile(f);
      setStatus(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    try {
      await uploadReceipt(file);
      setStatus("success");
      setFile(null);
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">
        Upload a Receipt
      </h1>
      <p className="text-gray-500 mb-6">
        Upload a receipt image or PDF to get started.
      </p>

      {/* Drop zone */}
      <div
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
          dragOver
            ? "border-emerald-500 bg-emerald-50"
            : "border-gray-300 hover:border-emerald-400 hover:bg-gray-50"
        }`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragOver(false);
          handleFile(e.dataTransfer.files[0]);
        }}
      >
        <div className="text-5xl mb-3">📄</div>
        {file ? (
          <p className="text-gray-700 font-medium">{file.name}</p>
        ) : (
          <>
            <p className="text-gray-600 font-medium">
              Drag & drop or click to select
            </p>
            <p className="text-gray-400 text-sm mt-1">Supports JPG, PNG, PDF</p>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/*,application/pdf"
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={!file || status === "uploading"}
        className="mt-4 w-full bg-emerald-600 text-white py-2.5 rounded-lg font-medium hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {status === "uploading" ? "Uploading..." : "Upload Receipt"}
      </button>

      {status === "success" && (
        <p className="mt-3 text-emerald-600 text-center font-medium">
          ✅ Receipt uploaded successfully!
        </p>
      )}
      {status === "error" && (
        <p className="mt-3 text-red-500 text-center font-medium">
          ❌ Upload failed — is the backend running?
        </p>
      )}
    </div>
  );
}
