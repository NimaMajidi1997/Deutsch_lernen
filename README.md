# Deutsch_lernen
Ich würde hier Deutsch lernen :)

# &#128161; Idea behind this Project
This project aims to build a database for the vocabulary we learn over time. We add new words and corresponding sentences into two files: L#_Word.txt and L#_Sentences.txt. By converting these sentences into audio files, we can review new vocabularies more easily just by listening.

I split the L#_Sentences.txt file into clusters, where each cluster contains e.g. 20 sentences. Then I use the [TTS library](https://github.com/coqui-ai/TTS), an open-source tool for advanced Text-to-Speech generation, to generate audio files for each cluster. Each audio file contains the 20 sentences from the corresponding cluster.

# &#129668; How?
First, install the TTS library using:

```bash
pip install TTS
```
Then, you can run the [audio_generator.py](https://github.com/NimaMajidi1997/Deutsch_lernen/blob/main/audio_generator.py). This script will cluster your sentences and generate the corresponding audio files.

# &#129409; And?
Now you can easily listen to these audio files to review and recap new words while you're sleeping, exercising, or doing other activities.