from app.pipeline.base import BaseFilter

SPECIES_FULL_NAMES = {
    "AS": "Acacia Senegal",
    "PC": "Prosopis Cineraria",
}


class ResultFormatter(BaseFilter):
    """Filter 6 – Result Formatting.

    Assembles the structured JSON response returned to the client.

    Reads:  data["species"], data["species_confidence"],
            data["health_status"], data["health_confidence"],
            data["disease_model_used"]
    Writes: data["result"]
    """

    def process(self, data: dict) -> dict:
        species_code = data["species"]
        species_name = SPECIES_FULL_NAMES.get(species_code, species_code)
        health = data["health_status"]

        data["result"] = {
            "species": {
                "code": species_code,
                "name": species_name,
                "confidence": round(data["species_confidence"], 4),
            },
            "health": {
                "status": health,
                "confidence": round(data["health_confidence"], 4),
                "model_used": data["disease_model_used"],
            },
            "summary": (
                f"The leaf is identified as {species_name} ({species_code}) "
                f"and is predicted to be {health}."
            ),
        }
        return data
