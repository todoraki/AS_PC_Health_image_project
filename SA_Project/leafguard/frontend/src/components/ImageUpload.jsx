import React, { useRef, useState } from "react";

const SUPPORTED_FILENAME_PATTERN = /^(ASP|PCP)\d{5}\.JPG$/;

function ImageUpload({
  onImageSelect,
  onInvalidImage,
  selectedFile,
  isAnalyzing = false,
}) {
  const inputRef = useRef();
  const [dragOver, setDragOver] = useState(false);

  function handleFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      return;
    }

    if (!SUPPORTED_FILENAME_PATTERN.test(file.name)) {
      if (typeof onInvalidImage === "function") {
        onInvalidImage();
      }
      return;
    }

    onImageSelect(file);
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  }

  return (
    <div className="card ai-input-card">
      <h2>1. Upload Leaf Image</h2>

      <div
        className={`upload-zone ${dragOver ? "drag-over" : ""}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={(e) => handleFile(e.target.files[0])}
        />
        <div className="upload-glyph" aria-hidden="true">
          <svg viewBox="0 0 24 24" role="img" aria-hidden="true">
            <path d="M9 4h6l1 3h2a2 2 0 012 2v8a3 3 0 01-3 3H7a3 3 0 01-3-3V9a2 2 0 012-2h2l1-3zm3 4a5 5 0 100 10 5 5 0 000-10zm0 2.2a2.8 2.8 0 110 5.6 2.8 2.8 0 010-5.6z" />
          </svg>
        </div>
        <p>
          {selectedFile
            ? selectedFile.name
            : "Click or drag & drop a leaf image here"}
        </p>
        <small>Accepted: JPG, PNG, WEBP</small>
      </div>

      {selectedFile && (
        <div className="image-preview reveal-in">
          <img
            src={URL.createObjectURL(selectedFile)}
            alt="Leaf preview"
          />
        </div>
      )}

      {selectedFile && isAnalyzing && (
        <div className="analyze-placeholder" aria-live="polite">
          <div className="placeholder-top">
            <span className="pulse-dot" />
            <span>Model analyzing...</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" />
          </div>
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
