from dataclasses import dataclass, field


@dataclass(slots=True)
class ProgressEvent:
    """
    Représente l'état de progression d'une opération FFmpeg.

    Cet objet est transmis aux différents systèmes d'affichage
    ou de suivi de progression.
    """

    # ------------------------------------------------------------------
    # Identification de l'opération
    # ------------------------------------------------------------------

    operation_id: int | None = None

    operation_name: str | None = None

    # ------------------------------------------------------------------
    # État de l'opération
    # ------------------------------------------------------------------

    # queued
    # running
    # completed
    # failed
    status: str = "running"

    # ------------------------------------------------------------------
    # Informations FFmpeg
    # ------------------------------------------------------------------

    frame: int | None = None

    fps: float | None = None

    bitrate: float | None = None

    bitrate_text: str | None = None

    total_size: int | None = None

    # Temps de média déjà traité, en secondes
    out_time: float | None = None

    # Durée totale de référence, en secondes
    duration: float | None = None

    # Vitesse FFmpeg, par exemple 1.82 pour 1.82x
    speed: float | None = None

    # ------------------------------------------------------------------
    # Progression
    # ------------------------------------------------------------------

    percentage: float | None = None

    # ------------------------------------------------------------------
    # Temps d'exécution
    # ------------------------------------------------------------------

    elapsed: float = 0.0

    eta: float | None = None

    # ------------------------------------------------------------------
    # Informations de contrôle FFmpeg
    # ------------------------------------------------------------------

    # continue / end
    progress: str | None = None

    message: str | None = None

    # ------------------------------------------------------------------
    # Toutes les informations brutes envoyées par FFmpeg
    # ------------------------------------------------------------------

    raw: dict[str, str] = field(default_factory=dict)