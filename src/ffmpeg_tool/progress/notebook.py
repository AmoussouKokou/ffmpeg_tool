from __future__ import annotations

from IPython.display import HTML, display

from ffmpeg_tool.models.progress import ProgressEvent


class NotebookProgress:
    """
    Affichage dynamique de la progression dans Jupyter Notebook.
    """

    def __init__(
        self,
        title: str | None = None,
    ) -> None:

        self.title = title

        self.handle = None

    # ==================================================================
    # Callback
    # ==================================================================

    def __call__(
        self,
        event: ProgressEvent,
    ) -> None:

        html = self._render(event)

        if self.handle is None:

            self.handle = display(
                HTML(html),
                display_id=True,
            )

        else:

            self.handle.update(
                HTML(html)
            )

    # ==================================================================
    # Affichage
    # ==================================================================

    def _render(
        self,
        event: ProgressEvent,
    ) -> str:

        name = (
            self.title
            or event.operation_name
            or "FFmpeg"
        )

        # --------------------------------------------------------------
        # Pourcentage
        # --------------------------------------------------------------

        if event.percentage is None:

            percentage_text = "—"
            percentage = 0

        else:

            percentage = event.percentage

            percentage_text = (
                f"{percentage:.1f}%"
            )

        # --------------------------------------------------------------
        # Temps
        # --------------------------------------------------------------

        out_time = self._format_time(
            event.out_time
        )

        duration = self._format_time(
            event.duration
        )

        elapsed = self._format_time(
            event.elapsed
        )

        eta = self._format_time(
            event.eta
        )

        # --------------------------------------------------------------
        # FPS
        # --------------------------------------------------------------

        fps = (
            f"{event.fps:.2f}"
            if event.fps is not None
            else "—"
        )

        # --------------------------------------------------------------
        # Speed
        # --------------------------------------------------------------

        speed = (
            f"{event.speed:.2f}x"
            if event.speed is not None
            else "—"
        )

        # --------------------------------------------------------------
        # Taille
        # --------------------------------------------------------------

        size = self._format_size(
            event.total_size
        )

        # --------------------------------------------------------------
        # Frame
        # --------------------------------------------------------------

        frame = (
            str(event.frame)
            if event.frame is not None
            else "—"
        )

        # --------------------------------------------------------------
        # Bitrate
        # --------------------------------------------------------------

        bitrate = (
            event.bitrate_text
            if event.bitrate_text
            else "—"
        )

        # --------------------------------------------------------------
        # Statut
        # --------------------------------------------------------------

        status = event.status

        if status == "completed":
            status_label = "Terminé"

        elif status == "running":
            status_label = "En cours"

        elif status == "failed":
            status_label = "Échec"

        elif status == "queued":
            status_label = "En attente"

        else:
            status_label = status

        # --------------------------------------------------------------
        # HTML
        # --------------------------------------------------------------

        return f"""
        <div style="
            border: 1px solid #d0d0d0;
            border-radius: 10px;
            padding: 16px;
            margin: 8px 0;
            font-family: Arial, sans-serif;
            max-width: 850px;
        ">

            <div style="
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 12px;
            ">
                {name}
            </div>

            <div style="
                width: 100%;
                height: 22px;
                background: #eeeeee;
                border-radius: 6px;
                overflow: hidden;
            ">

                <div style="
                    width: {percentage}%;
                    height: 100%;
                    background: #4caf50;
                    transition: width 0.2s;
                ">
                </div>

            </div>

            <div style="
                margin-top: 7px;
                font-size: 16px;
                font-weight: bold;
            ">
                {percentage_text}
            </div>

            <table style="
                width: 100%;
                margin-top: 14px;
                border-collapse: collapse;
            ">

                <tr>
                    <td><b>Statut</b></td>
                    <td>{status_label}</td>

                    <td><b>Frame</b></td>
                    <td>{frame}</td>
                </tr>

                <tr>
                    <td><b>Temps traité</b></td>
                    <td>{out_time}</td>

                    <td><b>Durée</b></td>
                    <td>{duration}</td>
                </tr>

                <tr>
                    <td><b>FPS</b></td>
                    <td>{fps}</td>

                    <td><b>Vitesse</b></td>
                    <td>{speed}</td>
                </tr>

                <tr>
                    <td><b>Bitrate</b></td>
                    <td>{bitrate}</td>

                    <td><b>Taille</b></td>
                    <td>{size}</td>
                </tr>

                <tr>
                    <td><b>Temps écoulé</b></td>
                    <td>{elapsed}</td>

                    <td><b>ETA</b></td>
                    <td>{eta}</td>
                </tr>

            </table>

        </div>
        """

    # ==================================================================
    # Utilitaires
    # ==================================================================

    @staticmethod
    def _format_time(
        seconds: float | None,
    ) -> str:

        if seconds is None:
            return "—"

        seconds = max(
            0,
            int(seconds),
        )

        hours, remainder = divmod(
            seconds,
            3600,
        )

        minutes, seconds = divmod(
            remainder,
            60,
        )

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    @staticmethod
    def _format_size(
        size: int | None,
    ) -> str:

        if size is None:
            return "—"

        value = float(size)

        units = [
            "B",
            "KB",
            "MB",
            "GB",
            "TB",
        ]

        for unit in units:

            if value < 1024:

                return (
                    f"{value:.1f} {unit}"
                )

            value /= 1024

        return f"{value:.1f} PB"