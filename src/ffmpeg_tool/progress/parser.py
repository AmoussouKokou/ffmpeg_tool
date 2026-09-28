import time

from ffmpeg_tool.models.progress import ProgressEvent


class FFmpegProgressParser:
    """
    Parse la sortie produite par :

        ffmpeg -progress pipe:1

    FFmpeg produit des lignes de la forme :

        frame=1520
        fps=42.3
        bitrate=1245.3kbits/s
        total_size=64200000
        out_time_us=410000000
        out_time=00:06:50.000000
        speed=1.82x
        progress=continue

    """

    def __init__(
        self,
        duration: float | None = None,
        operation_name: str | None = None,
        operation_id: int | None = None,
    ) -> None:

        self.duration = duration
        self.operation_name = operation_name
        self.operation_id = operation_id

        self.data: dict[str, str] = {}

        self.start_time = time.monotonic()

    # ------------------------------------------------------------------
    # Lecture d'une ligne FFmpeg
    # ------------------------------------------------------------------

    def feed(self, line: str) -> ProgressEvent | None:

        line = line.strip()

        if not line:
            return None

        if "=" not in line:
            return None

        key, value = line.split("=", 1)

        self.data[key] = value

        # FFmpeg envoie normalement plusieurs informations,
        # puis termine un bloc avec progress=continue ou progress=end.
        if key != "progress":
            return None

        return self._build_event()

    # ------------------------------------------------------------------
    # Construction de l'événement
    # ------------------------------------------------------------------

    def _build_event(self) -> ProgressEvent:

        elapsed = time.monotonic() - self.start_time

        out_time = self._parse_out_time()

        percentage = self._calculate_percentage(out_time)

        speed = self._parse_speed()

        eta = self._calculate_eta(
            percentage=percentage,
            elapsed=elapsed,
        )

        progress_value = self.data.get("progress")

        status = "running"

        if progress_value == "end":
            status = "completed"

        return ProgressEvent(
            operation_id=self.operation_id,
            operation_name=self.operation_name,
            status=status,

            frame=self._parse_int("frame"),

            fps=self._parse_float("fps"),

            bitrate=self._parse_bitrate(),

            bitrate_text=self.data.get("bitrate"),

            total_size=self._parse_int("total_size"),

            out_time=out_time,

            duration=self.duration,

            speed=speed,

            percentage=percentage,

            elapsed=elapsed,

            eta=eta,

            progress=progress_value,

            raw=dict(self.data),
        )

    # ------------------------------------------------------------------
    # Pourcentage
    # ------------------------------------------------------------------

    def _calculate_percentage(
        self,
        out_time: float | None,
    ) -> float | None:

        if self.duration is None:
            return None

        if out_time is None:
            return None

        if self.duration <= 0:
            return None

        percentage = (
            out_time / self.duration
        ) * 100.0

        return min(
            100.0,
            max(0.0, percentage),
        )

    # ------------------------------------------------------------------
    # ETA
    # ------------------------------------------------------------------

    def _calculate_eta(
        self,
        percentage: float | None,
        elapsed: float,
    ) -> float | None:

        if percentage is None:
            return None

        if percentage <= 0:
            return None

        if elapsed <= 0:
            return None

        estimated_total_time = (
            elapsed / (percentage / 100.0)
        )

        eta = estimated_total_time - elapsed

        return max(0.0, eta)

    # ------------------------------------------------------------------
    # Conversion des valeurs
    # ------------------------------------------------------------------

    def _parse_int(
        self,
        key: str,
    ) -> int | None:

        value = self.data.get(key)

        if value is None:
            return None

        try:
            return int(value)

        except (TypeError, ValueError):
            return None

    def _parse_float(
        self,
        key: str,
    ) -> float | None:

        value = self.data.get(key)

        if value is None:
            return None

        try:
            return float(value)

        except (TypeError, ValueError):
            return None

    # ------------------------------------------------------------------
    # Speed
    # ------------------------------------------------------------------

    def _parse_speed(self) -> float | None:

        value = self.data.get("speed")

        if not value:
            return None

        value = value.strip().lower()

        value = value.replace("x", "")

        try:
            return float(value)

        except (TypeError, ValueError):
            return None

    # ------------------------------------------------------------------
    # Bitrate
    # ------------------------------------------------------------------

    def _parse_bitrate(self) -> float | None:

        value = self.data.get("bitrate")

        if not value:
            return None

        value = value.strip().lower()

        if value in {"n/a", "0", "0kbits/s"}:
            return None

        try:

            if "mbits/s" in value:

                number = float(
                    value
                    .replace("mbits/s", "")
                    .strip()
                )

                return number * 1000.0

            if "kbits/s" in value:

                return float(
                    value
                    .replace("kbits/s", "")
                    .strip()
                )

            return float(value)

        except (TypeError, ValueError):
            return None

    # ------------------------------------------------------------------
    # Temps traité
    # ------------------------------------------------------------------

    def _parse_out_time(self) -> float | None:

        # --------------------------------------------------------------
        # Méthode préférée : microsecondes
        # --------------------------------------------------------------

        value = self.data.get("out_time_us")

        if value is not None:

            try:

                return int(value) / 1_000_000.0

            except (TypeError, ValueError):
                pass

        # --------------------------------------------------------------
        # Fallback : HH:MM:SS.microseconds
        # --------------------------------------------------------------

        value = self.data.get("out_time")

        if not value:
            return None

        try:

            hours, minutes, seconds = value.split(":")

            return (
                int(hours) * 3600
                + int(minutes) * 60
                + float(seconds)
            )

        except (TypeError, ValueError):
            return None