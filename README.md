# YouTube2AnalyticsPipeline

## Overview

This repository provides a pipeline for extracting, processing, and analyzing YouTube video transcripts to study the representation of named entities and other linguistic features. The pipeline is divided into five main stages, each contained within a numbered folder.

---

## Installation

### 1. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 2. Install FFmpeg

Before installing the required Python libraries, you must install FFmpeg:

#### Ubuntu / Debian:
```bash
sudo apt update && sudo apt install ffmpeg
```

#### macOS (using Homebrew):
```bash
brew install ffmpeg
```

#### Windows (using Chocolatey):
```powershell
choco install ffmpeg
```

#### Windows (manual installation):
1. Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract it and add its `bin` directory to your system's PATH.

### 3. Install Dependencies

After installing FFmpeg, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Install OpenAI Whisper

Whisper is required for automatic speech recognition:

```bash
pip install -U openai-whisper
```

---

## Pipeline Overview

### Folder 1: Downloading and Transcribing Audio

1. **Downloading Audio Streams**  
   - Uses `PyTube` to download audio streams from YouTube.
   - An example CSV file is provided to guide input formatting.
   - Replace the example file with your own YouTube playlists and channels.
   - This will create a directory structure:
     ```
     /channels
        /playlist1
           /video1.mp3
           /video2.mp3
     ```

2. **Generating SRT Subtitles**  
   - Uses OpenAI Whisper to generate subtitle `.srt` files from downloaded audio files.
   - SRT files are stored in the same directories as their respective videos.

---

### Folder 2: Extracting Terms and Metadata

1. **WordNet Synonyms Extraction**  
   - Finds synonyms for key terms using WordNet.
   - Example: Extracting synonyms for people-related terms.

2. **Identifying Head Nouns**  
   - Analyzes subtitle files to extract common noun phrases.

3. **Calculating Total Video Time per Channel**  
   - Computes total video duration per channel.

4. **Saving Proper Nouns to CSV**  
   - Extracts proper nouns from transcripts and saves them to a CSV categorized by channel.

---

### Folder 3: Text Normalization and Coreference Resolution

1. **Convert SRT to Text**  
   - Converts subtitle files into plain text format.

2. **Expand Contractions**  
   - Uses a contraction-mapping library to replace contracted words (e.g., "can't" → "cannot").

3. **Handle Possessives and Apostrophes**  
   - Uses `spaCy` to differentiate possessive vs. contraction cases.

4. **Detect Duplicate Files**  
   - Identifies duplicate videos appearing in multiple playlists to prevent double counting.

5. **Coreference Resolution (Optional, Uses ChatGPT API)**  
   - Replaces pronouns with their referenced entities.
   - Requires an OpenAI API key.
   - API calls may incur costs.

---

### Folder 4: Named Entity Recognition (NER) and Name Standardization

1. **Standardizing Names with Wikidata**  
   - Uses Named Entity Recognition (NER) to find famous names.
   - Queries Wikidata for their standardized names.
   - Replaces mentions of full names and last names for consistency.
   - Example: "Roosevelt" → "Theodore Roosevelt".

2. **Counting Named Entities per Channel**  
   - Analyzes each channel's videos and counts the occurrences of recognized famous names.
   - Outputs a CSV file containing name counts per channel.

3. **Fetching Gender and Race Data from Wikidata**  
   - Queries Wikidata using previously extracted names.
   - Outputs a CSV file with demographic attributes.

---

### Folder 5: Keyword and Term Frequency Analysis

1. **Counting Custom Terms per Channel**  
   - Uses an input CSV of terms to count occurrences per channel.
   - Handles multi-word terms without overcounting.
   - Ensures words inside other words are not mistakenly counted multiple times.
   - Example: "American" and "African-American" are counted distinctly.

---

## Additional Directories

### `csv/`
- Stores various CSV output files generated throughout the pipeline.

### `miscellaneous/`
- Contains additional scripts:
  - **WordNet Term Extraction**: Generates a CSV of related terms using WordNet.
  - **Single Video Audio Download**: Uses `PyTube` to download audio from a single YouTube video.

---

## Usage Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube2analyticspipeline.git
   cd youtube2analyticspipeline
   ```

2. Follow the installation steps above.

3. Prepare your input CSV (replace example files with your own).

4. Execute scripts in order, starting with **Folder 1** and progressing sequentially.

---

## Notes

- The coreference resolution step (Folder 3, second subfolder) requires an OpenAI API key.
- The pipeline assumes audio files are organized into a structured directory format.
- Ensure FFmpeg is installed before running the pipeline.
- Outputs include CSV reports of word frequencies, named entity occurrences, and standardized name mappings.

---

## Contributions

Contributions are welcome! If you have any improvements or suggestions, feel free to submit a pull request.

---

## Contact

For issues or questions, open an issue on GitHub or reach out via email at hbhidya@vols.utk.edu
