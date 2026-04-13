const API_BASE = "/api";

/**
 * Send an image + metadata to the backend and return the prediction.
 *
 * @param {File}   imageFile  – Leaf image (JPEG/PNG/WebP)
 * @param {Object} metadata   – Object with 10 metadata fields
 * @returns {Promise<Object>}   { status, data: { species, health, summary } }
 */
export async function predictDisease(imageFile, metadata) {
  const formData = new FormData();
  formData.append("image", imageFile);
  formData.append("metadata", JSON.stringify(metadata));

  const response = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Server error (${response.status})`);
  }

  return response.json();
}
