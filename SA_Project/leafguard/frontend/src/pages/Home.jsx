import React, { useEffect, useState } from "react";
import ImageUpload from "../components/ImageUpload.jsx";
import MetadataForm, {
  emptyMetadata,
  isMetadataComplete,
  buildSubmittableMetadata,
} from "../components/MetadataForm.jsx";
import ResultDisplay from "../components/ResultDisplay.jsx";
import { predictDisease } from "../services/api.js";

const SUPPORTED_FILENAME_PATTERN = /^(ASP|PCP)\d{5}\.JPG$/;
const ERROR_DISMISS_MS = 4000;

function Home() {
  const [imageFile, setImageFile] = useState(null);
  const [metadata, setMetadata] = useState(emptyMetadata());
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [metadataVisible, setMetadataVisible] = useState(true);

  useEffect(() => {
    if (!error) {
      return undefined;
    }

    const timeoutId = setTimeout(() => {
      setError(null);
    }, ERROR_DISMISS_MS);

    return () => clearTimeout(timeoutId);
  }, [error]);

  function isSupportedFilename(filename) {
    return SUPPORTED_FILENAME_PATTERN.test(filename);
  }

  function handleImageSelect(file) {
    setImageFile(file);
    if (file) {
      setError(null);
    }
  }

  function handleInvalidImage() {
    setImageFile(null);
    setError(
      "Uploaded species is out of model scope. Please upload either Acacia Senegal (AS) or Prosopis Cineraria (PC) plant images."
    );
  }

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
    if (!isSupportedFilename(imageFile.name)) {
      setError(
        "Uploaded species is out of model scope. Please upload either Acacia Senegal (AS) or Prosopis Cineraria (PC) plant images."
      );
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

    setMetadataVisible(false);
    setLoading(true);
    try {
      const resp = await predictDisease(imageFile, numericMeta);
      setResult(resp.data);
    } catch (err) {
      setError(err.message);
      setMetadataVisible(true);
    } finally {
      setLoading(false);
    }
  }

  function handleReset() {
    setImageFile(null);
    setMetadata(emptyMetadata());
    setResult(null);
    setError(null);
    setMetadataVisible(true);
  }

  return (
    <section className="workspace-split">
      <div className="input-column">
        {error && <div className="error-msg">{error}</div>}

        <ImageUpload
          onImageSelect={handleImageSelect}
          onInvalidImage={handleInvalidImage}
          selectedFile={imageFile}
          isAnalyzing={loading}
        />

        {metadataVisible ? (
          <MetadataForm metadata={metadata} onChange={setMetadata} />
        ) : (
          <div className="card meta-collapsed">
            <h2>2. Leaf Metadata</h2>
            <button
              type="button"
              className="link-btn"
              onClick={() => setMetadataVisible(true)}
            >
              Show metadata controls
            </button>
          </div>
        )}

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
      </div>

      <div className="result-column">
        {result ? (
          <ResultDisplay result={result} />
        ) : (
          <div className="card result-placeholder">
            <h2>AI Prediction Dashboard</h2>
            <p>
              Prediction cards appear here after you upload an image and run
              analysis.
            </p>
          </div>
        )}

        {result && (
          <button className="submit-btn secondary-btn" onClick={handleReset}>
            Analyze Another Leaf
          </button>
        )}
      </div>
    </section>
  );
}

export default Home;
