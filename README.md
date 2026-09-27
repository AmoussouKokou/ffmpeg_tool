# FFmpeg Tool

Bibliothèque Python modulaire pour manipuler des fichiers audio et vidéo
avec FFmpeg.

## Fonctionnalités

- Conversion audio
- Conversion vidéo
- Extraction audio
- Découpage audio
- Découpage vidéo
- Modification du volume
- Normalisation audio
- Fade audio
- Modification de vitesse
- Resize vidéo
- Extraction d'une image
- Overlay d'image
- Image + audio -> vidéo
- Analyse média avec FFprobe
- Pipelines
- Exécution parallèle d'opérations indépendantes

---

# Installation

## FFmpeg

FFmpeg doit être installé sur le système.

Vérifier :

```bash
ffmpeg -version
```
et
```bash
ffprobe -version
```

## Installation du projet

Depuis la racine du projet :

```bash
pip install -e .
```

Pour installer les outils de développement :


```bash
pip install -e ".[dev]"
```

# Utilisation
## Convertir WAV vers MP3

```python
from ffmpeg_tool import ConvertAudio

operation = ConvertAudio(
    input="audio.wav",
    output_path="audio.mp3",
    codec="libmp3lame",
    quality=0,
)

operation.execute()
```

## Extraire l'audio d'une vidéo

```python
from ffmpeg_tool import ExtractAudio

operation = ExtractAudio(
    input="video.mp4",
    output_path="audio.mp3",
    codec="libmp3lame",
    bitrate="320k",
)

operation.execute()
```

## Découper un audio

Les temps peuvent être fournis sous plusieurs formes.

```python
from ffmpeg_tool import CutAudio

operation = CutAudio(
    input="audio.mp3",
    output_path="extrait.mp3",
    start="00:05:00",
    end="00:10:00",
)

operation.execute()
```

On peut également utiliser des secondes :

```python
operation = CutAudio(
    input="audio.mp3",
    output_path="extrait.mp3",
    start=300,
    end=600,
)

operation.execute()
```

## Découper une vidéo

```python
from ffmpeg_tool import CutVideo

operation = CutVideo(
    input="video.mp4",
    output_path="extrait.mp4",
    start="00:01:30",
    end="00:03:45",
)

operation.execute()
```

## Découpage rapide sans réencodage

```python
operation = CutVideo(
    input="video.mp4",
    output_path="extrait.mp4",
    start="00:05:00",
    end="00:10:00",
    copy=True,
)

operation.execute()
```

`copy=True` est beaucoup plus rapide mais la découpe peut ne pas être
exacte à l'image près à cause des keyframes.

Pour une découpe précise, utiliser `copy=False`.

## Image + audio -> MP4

```python
from ffmpeg_tool import ImageAudioToVideo

operation = ImageAudioToVideo(
    image="cover.jpg",
    audio="audio.mp3",
    output_path="video.mp4",
)

operation.execute()
```

L'image est répétée pendant toute la durée de l'audio.

Cela permet également de créer une vidéo de plusieurs heures.

## Redimensionner une vidéo

```python
from ffmpeg_tool import ResizeVideo

operation = ResizeVideo(
    input="video.mp4",
    output_path="video_1080p.mp4",
    width=1920,
    height=1080,
)

operation.execute()
```

## Extraire une image

```python
from ffmpeg_tool import ExtractFrame

operation = ExtractFrame(
    input="video.mp4",
    output_path="frame.jpg",
    timestamp="00:01:30",
)

operation.execute()
```

## Modifier le volume

```python
from ffmpeg_tool import Volume

operation = Volume(
    input="audio.mp3",
    output_path="louder.mp3",
    volume=2.0,
)

operation.execute()
```

## Normaliser un audio

```python
from ffmpeg_tool import NormalizeAudio

operation = NormalizeAudio(
    input="audio.mp3",
    output_path="normalized.mp3",
)

operation.execute()
```

## Modifier la vitesse

```python
from ffmpeg_tool import SpeedAudio

operation = SpeedAudio(
    input="audio.mp3",
    output_path="fast.mp3",
    speed=1.5,
)

operation.execute()
```

## Analyser un fichier

```python
from ffmpeg_tool import FFprobe

probe = FFprobe()

info = probe.probe("video.mp4")

print(info.duration)
print(info.format_name)

print(info.has_video)
print(info.has_audio)

if info.video:
    print(info.video.width)
    print(info.video.height)
    print(info.video.fps)

if info.audio:
    print(info.audio.sample_rate)
    print(info.audio.channels)
```

## Pipeline

Les opérations peuvent être organisées en graphe.

```python
from ffmpeg_tool import (
    CutAudio,
    NormalizeAudio,
    Pipeline,
    PipelineExecutor,
)

pipeline = Pipeline()

cut = pipeline.add(
    CutAudio(
        input="audio.mp3",
        output_path="cut.mp3",
        start="00:05:00",
        end="00:10:00",
    )
)

normalize = pipeline.add(
    NormalizeAudio(
        input="cut.mp3",
        output_path="normalized.mp3",
    ),
    depends_on=[cut],
)

executor = PipelineExecutor(
    max_workers=2
)

results = executor.run(pipeline)
```

## Exécution parallèle

Les opérations indépendantes peuvent être exécutées
simultanément.

```python
pipeline = Pipeline()

audio = pipeline.add(
    ExtractAudio(
        input="video.mp4",
        output_path="audio.mp3",
    )
)

frame = pipeline.add(
    ExtractFrame(
        input="video.mp4",
        output_path="cover.jpg",
        timestamp="00:01:00",
    )
)

executor = PipelineExecutor(
    max_workers=2
)

results = executor.run(pipeline)
```

Les deux opérations n'ont aucune dépendance entre elles.
Elles peuvent donc être exécutées en parallèle.

## Configuration de FFmpeg

Si FFmpeg n'est pas dans le PATH :

```python
from ffmpeg_tool import (
    FFmpegConfig,
    FFmpegRunner,
)

config = FFmpegConfig(
    ffmpeg_path=r"C:\ffmpeg\bin\ffmpeg.exe",
    ffprobe_path=r"C:\ffmpeg\bin\ffprobe.exe",
)

runner = FFmpegRunner(config)
```

Puis :

```python
operation.execute(runner)
```

## Tests

```bash
pytest
```

---

# 40. Exemple concret : ton cas MP3 → MP4

Avec cette architecture, tu peux maintenant faire :

```python
from ffmpeg_tool import ImageAudioToVideo

operation = ImageAudioToVideo(
    image="cover.jpg",
    audio="musique.mp3",
    output_path="resultat.mp4",
    audio_bitrate="320k",
)

result = operation.execute()

print(result.output)
print(result.duration)
print(result.command)
```

# 41. Exemple concret : découper 5 minutes d'audio

```python
from ffmpeg_tool import CutAudio

operation = CutAudio(
    input="long_audio.mp3",
    output_path="extrait.mp3",
    start="00:05:00",
    end="00:10:00",
)

operation.execute()
```

Cela correspond conceptuellement à :

```bash
ffmpeg -i long_audio.mp3 -ss 00:05:00 -t 00:05:00 extrait.mp3
```

Et tu peux aussi écrire :

```python
operation = CutAudio(
    input="long_audio.mp3",
    output_path="extrait.mp3",
    start=300,
    end=600,
)
```

# 42. Exemple de pipeline plus intéressant

Par exemple :

vidéo → extraction audio → découpage → normalisation → MP3 final

```python
from ffmpeg_tool import (
    ExtractAudio,
    CutAudio,
    NormalizeAudio,
    Pipeline,
    PipelineExecutor,
)

pipeline = Pipeline()

extract = pipeline.add(
    ExtractAudio(
        input="video.mp4",
        output_path="audio.wav",
        codec="pcm_s16le",
    )
)

cut = pipeline.add(
    CutAudio(
        input="audio.wav",
        output_path="extrait.wav",
        start="00:05:00",
        end="00:10:00",
    ),
    depends_on=[extract],
)

normalize = pipeline.add(
    NormalizeAudio(
        input="extrait.wav",
        output_path="normalise.wav",
    ),
    depends_on=[cut],
)

executor = PipelineExecutor(
    max_workers=2
)

results = executor.run(pipeline)

for node_id, result in results.items():
    print(
        node_id,
        result.operation_name,
        result.output,
    )
```

Le graphe est :

```
video.mp4
    │
    ▼
ExtractAudio
    │
    ▼
CutAudio
    │
    ▼
NormalizeAudio
    │
    ▼
normalise.wav
```

Alors que celui-ci :

```python
pipeline = Pipeline()

audio = pipeline.add(
    ExtractAudio(
        input="video.mp4",
        output_path="audio.mp3",
    )
)

frame = pipeline.add(
    ExtractFrame(
        input="video.mp4",
        output_path="cover.jpg",
        timestamp="00:01:00",
    )
)

executor = PipelineExecutor(
    max_workers=2
)

executor.run(pipeline)
```

peut être exécuté :

```
                ┌── ExtractAudio ──► audio.mp3
video.mp4 ──────┤
                └── ExtractFrame ──► cover.jpg
```

avec les deux traitements en parallèle.

# 43. Installation du projet

Une fois les fichiers créés :

```bash
cd ffmpeg_tool
```

Puis :

```bash
python -m venv .venv
```

Windows :

```bash
.venv\Scripts\activate
```

Installation :

```bash
pip install -e ".[dev]"
```

Tests :

```bash
pytest
```

Et vérification de FFmpeg :

```bash
ffmpeg -version
ffprobe -version
```

Point important

Cette base est volontairement construite comme une vraie bibliothèque, et pas comme un simple script FFmpeg. La séparation core → models → operations → pipeline nous permettra ensuite d'ajouter proprement, sans refaire l'architecture, des fonctionnalités comme concaténation, sous-titres, watermark, GIF, changement de FPS, codecs avancés, métadonnées, génération de miniatures, batch processing, traitement par lots et pipelines plus complexes.
