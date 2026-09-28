from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path

from ffmpeg_tool.core.exceptions import FFmpegExecutionError
from ffmpeg_tool.core.runner import FFmpegRunner
from ffmpeg_tool.models.operation import OperationResult
from ffmpeg_tool.models.progress import ProgressEvent


class Operation(ABC):
    """
    Classe abstraite de base de toutes les opérations FFmpeg.
    """

    def __init__(
        self,
        output_path: str,
    ) -> None:

        self.output = output_path

    # ==================================================================
    # Validation de l'entrée
    # ==================================================================

    @staticmethod
    def check_input(
        input_path: str | Path,
    ) -> None:
        """
        Vérifie que le fichier d'entrée existe.
        """

        path = Path(input_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Fichier d'entrée introuvable : {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"L'entrée n'est pas un fichier : {path}"
            )

    # ==================================================================
    # Construction de la commande FFmpeg
    # ==================================================================

    @abstractmethod
    def build_args(self) -> list[str]:
        """
        Construit les arguments passés à FFmpeg.
        """

        raise NotImplementedError

    # ==================================================================
    # Durée utilisée pour la progression
    # ==================================================================

    def get_progress_duration(
        self,
        runner: FFmpegRunner,
    ) -> float | None:
        """
        Retourne la durée de référence utilisée pour calculer
        le pourcentage de progression.

        Par défaut, aucune durée n'est connue.

        Les opérations qui connaissent leur durée de sortie peuvent
        redéfinir cette méthode.
        """

        return None

    # ==================================================================
    # Exécution
    # ==================================================================

    def execute(
        self,
        runner: FFmpegRunner | None = None,
        progress_callback: Callable[
            [ProgressEvent],
            None
        ] | None = None,
        operation_id: int | None = None,
    ) -> OperationResult:

        if runner is None:
            runner = FFmpegRunner()

        # --------------------------------------------------------------
        # Création du dossier de sortie
        # --------------------------------------------------------------

        runner.ensure_output_directory(
            self.output
        )

        # --------------------------------------------------------------
        # Construction de la commande
        #
        # build_args() est responsable de vérifier l'entrée
        # via check_input(), comme le faisaient tes opérations
        # existantes.
        # --------------------------------------------------------------

        args = self.build_args()

        # --------------------------------------------------------------
        # Durée de référence pour la progression
        # --------------------------------------------------------------

        progress_duration = (
            self.get_progress_duration(runner)
        )

        # --------------------------------------------------------------
        # Exécution FFmpeg
        # --------------------------------------------------------------

        result = runner.ffmpeg(
            args=args,
            progress_callback=progress_callback,
            progress_duration=progress_duration,
            operation_name=self.__class__.__name__,
            operation_id=operation_id,
        )

        # --------------------------------------------------------------
        # Vérification du résultat
        # --------------------------------------------------------------

        if result.return_code != 0:
            raise FFmpegExecutionError(
                result.stderr
            )

        # --------------------------------------------------------------
        # Résultat de l'opération
        # --------------------------------------------------------------

        return OperationResult(
            operation_name=self.__class__.__name__,
            output=self.output,
            command=result.command,
            duration=result.duration,
            return_code=result.return_code,
        )