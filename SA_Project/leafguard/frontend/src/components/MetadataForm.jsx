import React from "react";

/**
 * Binary fields — rendered as Yes / No dropdowns.
 * "Heat_Drought" displays as "Heat + Drought" but the key sent to the
 * backend uses the underscore form.
 */
const BINARY_FIELDS = [
  { key: "Artefacts",      label: "Artefacts" },
  { key: "Control",        label: "Control" },
  { key: "Heat",           label: "Heat" },
  { key: "Drought",        label: "Drought" },
  { key: "Heat_Drought",   label: "Heat + Drought" },
  { key: "Decolourization",label: "Decolourization" },
  { key: "Spots",          label: "Spots" },
];

/**
 * All field keys sent to the backend (10 total).
 * Damage_missing is computed automatically by the form, not shown directly.
 */
export const ALL_FIELDS = [
  ...BINARY_FIELDS.map((f) => f.key),
  "Damage",
  "Damage_missing",
  "Week",
];

/** Returns a blank metadata state. */
export function emptyMetadata() {
  const m = {};
  ALL_FIELDS.forEach((k) => (m[k] = ""));
  return m;
}

// Fields the user actually fills in (Damage_missing is auto-derived)
const USER_FIELDS = ALL_FIELDS.filter((k) => k !== "Damage_missing");

/** True only when every user-facing field has a value. */
export function isMetadataComplete(metadata) {
  return USER_FIELDS.every(
    (k) => metadata[k] !== "" && metadata[k] !== undefined && metadata[k] !== null
  );
}

/**
 * Build the final numeric metadata object to send to the backend.
 * Computes Damage_missing from the Damage selection.
 */
export function buildSubmittableMetadata(metadata) {
  const out = {};

  // Binary fields
  BINARY_FIELDS.forEach(({ key }) => {
    out[key] = metadata[key] === "yes" ? 1 : 0;
  });

  // Damage + Damage_missing
  if (metadata["Damage"] === "unknown") {
    out["Damage"] = 0;
    out["Damage_missing"] = 1;
  } else {
    out["Damage"] = metadata["Damage"] === "yes" ? 1 : 0;
    out["Damage_missing"] = 0;
  }

  // Week
  out["Week"] = parseInt(metadata["Week"], 10);
  return out;
}

// ── Component ────────────────────────────────────────────────────
function MetadataForm({ metadata, onChange }) {
  function set(key, value) {
    onChange({ ...metadata, [key]: value });
  }

  return (
    <div className="card">
      <h2>2. Enter Leaf Metadata</h2>

      <p className="meta-hint">
        Select <strong>Yes</strong> or <strong>No</strong> for each stress
        condition observed on the leaf.
      </p>

      <div className="meta-grid">
        {/* ── 7 binary Yes/No dropdowns ─────────────────── */}
        {BINARY_FIELDS.map(({ key, label }) => (
          <div key={key} className="meta-field">
            <label htmlFor={key}>{label}</label>
            <select
              id={key}
              value={metadata[key] ?? ""}
              onChange={(e) => set(key, e.target.value)}
              className={metadata[key] === "" ? "select-placeholder" : ""}
            >
              <option value="" disabled>Select…</option>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
        ))}

        {/* ── Damage (optional / unknown allowed) ───────── */}
        <div className="meta-field">
          <label htmlFor="Damage">Damage</label>
          <select
            id="Damage"
            value={metadata["Damage"] ?? ""}
            onChange={(e) => set("Damage", e.target.value)}
            className={metadata["Damage"] === "" ? "select-placeholder" : ""}
          >
            <option value="" disabled>Select…</option>
            <option value="yes">Yes</option>
            <option value="no">No</option>
            <option value="unknown">Unknown / Not observed</option>
          </select>
        </div>

        {/* ── Week ──────────────────────────────────────── */}
        <div className="meta-field">
          <label htmlFor="Week">Week (1 – 52)</label>
          <input
            id="Week"
            type="number"
            min={1}
            max={52}
            step={1}
            placeholder="e.g. 14"
            value={metadata["Week"] ?? ""}
            onChange={(e) => set("Week", e.target.value)}
          />
        </div>
      </div>

      {/* Damage_missing info line */}
      {metadata["Damage"] === "unknown" && (
        <p className="meta-hint warn">
          Damage marked as Unknown → <code>Damage_missing = 1</code> will be
          sent to the model automatically.
        </p>
      )}
    </div>
  );
}

export default MetadataForm;

