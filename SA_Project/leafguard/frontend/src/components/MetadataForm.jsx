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

const GROUPS = [
  {
    title: "Environmental Stress",
    icon: "🧪",
    fields: [
      { key: "Heat", label: "Heat" },
      { key: "Drought", label: "Drought" },
      { key: "Heat_Drought", label: "Heat + Drought" },
    ],
  },
  {
    title: "Leaf Condition",
    icon: "🌿",
    fields: [
      { key: "Spots", label: "Spots" },
      { key: "Damage", label: "Damage", options: ["no", "yes"] },
      { key: "Decolourization", label: "Decolourization" },
    ],
  },
  {
    title: "Experiment Info",
    icon: "🧪",
    fields: [
      { key: "Artefacts", label: "Artefacts" },
      { key: "Control", label: "Control" },
      { key: "Week", label: "Week", type: "number" },
    ],
  },
];

// ── Component ────────────────────────────────────────────────────
function MetadataForm({ metadata, onChange }) {
  function set(key, value) {
    onChange({ ...metadata, [key]: value });
  }

  function renderBinaryControl(fieldKey, fieldLabel, options = ["no", "yes"]) {
    return (
      <div className="control-row" key={fieldKey}>
        <label className="control-label" htmlFor={`${fieldKey}-${options[0]}`}>
          {fieldLabel}
        </label>
        <div className="binary-toggle" role="group" aria-label={fieldLabel}>
          {options.map((opt) => (
            <button
              key={opt}
              id={`${fieldKey}-${opt}`}
              type="button"
              className={`toggle-pill ${metadata[fieldKey] === opt ? "active" : ""}`}
              onClick={() => set(fieldKey, opt)}
            >
              {opt === "yes"
                ? "Yes"
                : opt === "no"
                ? "No"
                : "Unknown"}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="card metadata-panel">
      <h2>2. Enter Leaf Metadata</h2>

      <div className="meta-group-grid">
        {GROUPS.map((group) => (
          <section key={group.title} className="meta-group-card">
            <div className="group-title">
              <span>{group.icon}</span>
              <h3>{group.title}</h3>
            </div>

            <div className="group-separator" />

            <div className="group-controls">
              {group.fields.map((field) => {
                if (field.type === "number") {
                  return (
                    <div className="control-row" key={field.key}>
                      <label className="control-label" htmlFor="Week">
                        Week (1-52)
                      </label>
                      <input
                        id="Week"
                        className="week-input"
                        type="number"
                        min={1}
                        max={52}
                        step={1}
                        placeholder="e.g. 14"
                        value={metadata["Week"] ?? ""}
                        onChange={(e) => set("Week", e.target.value)}
                      />
                    </div>
                  );
                }

                if (field.options) {
                  return renderBinaryControl(field.key, field.label, field.options);
                }

                return renderBinaryControl(field.key, field.label);
              })}
            </div>
          </section>
        ))}
      </div>

    </div>
  );
}

export default MetadataForm;

