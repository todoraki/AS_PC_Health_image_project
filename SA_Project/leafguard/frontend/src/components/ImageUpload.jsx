import React, { useRef, useState } from "react";

function ImageUpload({ onImageSelect, selectedFile }) {
  const inputRef = useRef();
  const [dragOver, setDragOver] = useState(false);

  function handleFile(file) {
    if (file && file.type.startsWith("image/")) {
      onImageSelect(file);
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    handleFile(file);
  }

  return (
    <div className="card">
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
        <div className="icon">📷</div>
        <p>
          {selectedFile
            ? selectedFile.name
            : "Click or drag & drop a leaf image here"}
        </p>
      </div>

      {selectedFile && (
        <div className="image-preview">
          <img
            src={URL.createObjectURL(selectedFile)}
            alt="Leaf preview"
          />
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
