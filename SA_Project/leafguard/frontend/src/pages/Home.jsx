import React, { useState } from "react";
import ImageUpload from "../components/ImageUpload.jsx";
import MetadataForm, {
  emptyMetadata,
  isMetadataComplete,
  buildSubmittableMetadata,
} from "../components/MetadataForm.jsx";
import ResultDisplay from "../components/ResultDisplay.jsx";
import { predictDisease } from "../services/api.js";

function Home() {
  const [imageFile, setImageFile] = useState(null);
  const [metadata, setMetadata] = useState(emptyMetadata());
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function isFormValid() {
    return imageFile !== null && isMetadataComplete(metadata);
  }

  async function handleSubmit() {
    setError(null);
    setResult(null);

    if (!imageFile) {
      setError("Please upload a leaf image.");
      return;
    }
    if (!isMetadataComplete(metadata)) {
      setError("Please fill in all metadata fields before submitting.");
      return;
    }

    // Validate Week is a number
    const weekNum = parseInt(metadata["Week"], 10);
    if (isNaN(weekNum) || weekNum < 1 || weekNum > 52) {
      setError("Week must be an integer between 1 and 52.");
      return;
    }

    const numericMeta = buildSubmittableMetadata(metadata);

    setLoading(true);
    try {
      const resp = await predictDisease(imageFile, numericMeta);
      setResult(resp.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setImageFile(null);
    setMetadata(emptyMetadata());
    setResult(null);
    setError(null);
  }

  return (
    <section className="workflow-stack">
      {error && <div className="error-msg">{error}</div>}

      <ImageUpload
        onImageSelect={setImageFile}
        selectedFile={imageFile}
        isAnalyzing={loading}
      />

      <MetadataForm metadata={metadata} onChange={setMetadata} />

      <button
        className={`submit-btn ${loading ? "is-loading" : ""}`}
        onClick={handleSubmit}
        disabled={loading}
        aria-busy={loading}
      >
        {loading ? (
          <>
            <span className="spinner" /> Analyzing...
          </>
        ) : (
          "Analyze Leaf"
        )}
      </button>

      <ResultDisplay result={result} />

      {result && (
        <button
          className="submit-btn secondary-btn"
          onClick={handleReset}
        >
          Analyze Another Leaf
        </button>
      )}
    </section>
  );
}

export default Home;
