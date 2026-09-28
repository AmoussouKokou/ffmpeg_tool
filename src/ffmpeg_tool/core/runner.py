from __future__ import annotations

import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from ffmpeg_tool.core.config import FFmpegConfig
from ffmpeg_tool.core.exceptions import (
    FFmpegExecutionError,
    FFmpegNotFoundError,
)

from ffmpeg_tool.models.progress import ProgressEvent
from ffmpeg_tool.progress.parser import FFmpegProgressParser


if TYPE_CHECKING:
    from collections.abc import Callable


@dataclass(slots=True)
class CommandResult:
    """
    Résultat de l'exécution d'une commande système.
    """

    command: list[str]

    return_code: int

    stdout: str

    stderr: str

    duration: float


class FFmpegRunner:
    """
    Exécute FFmpeg et FFprobe.
    """

    def __init__(
        self,
        config: FFmpegConfig | None = None,
    ) -> None:

        self.config = config or FFmpegConfig()

    # ==================================================================
    # Exécution générique
    # ==================================================================

    def run(
        self,
        command: list[str],
        progress_callback: Callable[
            [ProgressEvent],
            None
        ] | None = None,
        progress_duration: float | None = None,
        operation_name: str | None = None,
        operation_id: int | None = None,
    ) -> CommandResult:

        start_time = time.monotonic()

        # --------------------------------------------------------------
        # Vérification de FFmpeg
        # --------------------------------------------------------------

        self._check_executable(command[0])

        # --------------------------------------------------------------
        # Mode classique
        # --------------------------------------------------------------

        if progress_callback is None:

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdin=subprocess.DEVNULL,
            )

            stdout, stderr = process.communicate()

            duration = (
                time.monotonic()
                - start_time
            )

            return CommandResult(
                command=command,
                return_code=process.returncode,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
            )

        # --------------------------------------------------------------
        # Mode avec progression
        # --------------------------------------------------------------

        command = list(command)

        command.extend(
            [
                "-progress",
                "pipe:1",
                "-nostats",
            ]
        )

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            stdin=subprocess.DEVNULL,
        )

        parser = FFmpegProgressParser(
            duration=progress_duration,
            operation_name=operation_name,
            operation_id=operation_id,
        )

        stderr_lines: list[str] = []

        # --------------------------------------------------------------
        # Lecture de stderr dans un thread séparé
        #
        # Cela évite un blocage si stderr se remplit.
        # --------------------------------------------------------------

        def read_stderr() -> None:

            if process.stderr is None:
                return

            for line in process.stderr:
                stderr_lines.append(line)

        stderr_thread = threading.Thread(
            target=read_stderr,
            daemon=True,
        )

        stderr_thread.start()

        # --------------------------------------------------------------
        # Lecture de stdout = progression FFmpeg
        # --------------------------------------------------------------

        if process.stdout is not None:

            for line in process.stdout:

                event = parser.feed(line)

                if event is not None:
                    progress_callback(event)

        # --------------------------------------------------------------
        # Attendre FFmpeg
        # --------------------------------------------------------------

        process.wait()

        stderr_thread.join()

        duration = (
            time.monotonic()
            - start_time
        )

        stderr = "".join(stderr_lines)

        result = CommandResult(
            command=command,
            return_code=process.returncode,
            stdout="",
            stderr=stderr,
            duration=duration,
        )

        # --------------------------------------------------------------
        # Erreur FFmpeg
        # --------------------------------------------------------------

        if result.return_code != 0:

            raise FFmpegExecutionError(
                stderr or
                f"FFmpeg a retourné le code "
                f"{result.return_code}."
            )

        return result

    # ==================================================================
    # FFmpeg
    # ==================================================================

    def ffmpeg(
        self,
        args: list[str],
        progress_callback: Callable[
            [ProgressEvent],
            None
        ] | None = None,
        progress_duration: float | None = None,
        operation_name: str | None = None,
        operation_id: int | None = None,
    ) -> CommandResult:

        command = [
            self.config.ffmpeg_path,
            "-hide_banner",
            "-loglevel",
            self.config.loglevel,
        ]

        if self.config.overwrite:
            command.append("-y")

        if self.config.threads is not None:
            command.extend(
                [
                    "-threads",
                    str(self.config.threads),
                ]
            )

        command.extend(args)

        return self.run(
            command,
            progress_callback=progress_callback,
            progress_duration=progress_duration,
            operation_name=operation_name,
            operation_id=operation_id,
        )

    # ==================================================================
    # FFprobe
    # ==================================================================

    def ffprobe(
        self,
        args: list[str],
    ) -> CommandResult:

        command = [
            self.config.ffprobe_path,
            "-hide_banner",
            "-loglevel",
            self.config.loglevel,
        ]

        command.extend(args)

        return self.run(command)

    # ==================================================================
    # Vérification de l'exécutable
    # ==================================================================

    @staticmethod
    def _check_executable(
        executable: str,
    ) -> None:

        try:

            subprocess.run(
                [
                    executable,
                    "-version",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                check=True,
            )

        except FileNotFoundError as exc:

            raise FFmpegNotFoundError(
                f"Exécutable introuvable : {executable}"
            ) from exc

        except subprocess.CalledProcessError:
            # L'exécutable existe mais la commande
            # de vérification a échoué.
            pass

    # ==================================================================
    # Création du dossier de sortie
    # ==================================================================

    @staticmethod
    def ensure_output_directory(
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        parent = output_path.parent

        if parent != Path("."):
            parent.mkdir(
                parents=True,
                exist_ok=True,
            )