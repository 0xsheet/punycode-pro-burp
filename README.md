# Punycode Pro Tool for Burp Suite

A lightweight Burp Suite extension for exploring Unicode homoglyphs, inspecting IDNA/Punycode encodings, and copying lookalike characters into your manual testing workflow.

Written in Python for **Jython**, with a native Java Swing interface and Burp's legacy Extender API.

## Features

- **Generator:** enter a letter from `a` to `z` to display its configured Unicode alternatives and encoding results.
- **Quick Copy List:** browse all 26 letter groups and click a character button to copy its exact text to the system clipboard.
- **421 configured entries:** a manually maintained collection of accented letters, mixed-script lookalikes, mathematical characters, and other visual variants.
- **Uppercase input support:** ASCII uppercase letters are converted to lowercase before lookup.
- **Local operation:** the extension contains no network requests, telemetry, or file-writing logic. Copy buttons update the system clipboard.
- **No pip dependencies:** the extension uses Jython's standard library, Java Swing/AWT, and Burp's supplied interfaces.

## Requirements

| Component | Requirement |
| --- | --- |
| Burp Suite | A desktop installation that supports Python extensions through the legacy Extender API |
| Python runtime | A Jython standalone JAR compatible with your Burp/Java environment |
| Desktop | A graphical environment for Swing and system clipboard access |

This is a **Burp extension**, not a standalone Python 3 application. Running `python3 punycode_tool.py` will not provide the required `burp`, `javax`, and `java` modules.

Download Jython from the [official Jython downloads page](https://www.jython.org/download.html). Use the **standalone JAR**, rather than the installer JAR.

## Installation

1. Clone this repository or download its ZIP and extract it:

   ```bash
   git clone https://github.com/0xsheet/punycode-pro-burp.git
   cd punycode-pro-burp
   ```

2. In Burp, open **Settings → Extensions** and find **Python environment**. Set **Location of the Jython standalone JAR file** to your downloaded JAR.
3. Go to **Extensions → Installed → Add**. Select **Python** as the extension type and choose `punycode_tool.py`.
4. Complete the loading dialog and inspect its **Output** and **Errors** tabs. Successful initialization prints:

   ```text
   Punycode Pro Tool loaded successfully.
   ```

5. Open the new **Punycode Tool** suite tab. The entry in the extension manager is named **Punycode Pro Tool**.

Older Burp versions may use **Extender** for the extension-management menu. See PortSwigger's [extension settings](https://portswigger.net/burp/documentation/desktop/settings/extensions) and [manual installation guide](https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/installing/manual-install) for the current interface.

## Usage

### Generate character variants

1. Open **Punycode Tool → Generator**.
2. Enter one ASCII letter, such as `a`.
3. Click **Generate & Encode**.
4. Inspect the **Glyph** and **Punycode Result** columns.

Representative results for entries in the `a` group:

| Character | Unicode | Encoding result |
| --- | --- | --- |
| `à` | U+00E0, Latin small letter a with grave | `xn--0ca` |
| `а` | U+0430, Cyrillic small letter a | `xn--80a` |
| `Ａ` | U+FF21, fullwidth Latin capital letter A | `a` |
| `𝔞` | U+1D51E, mathematical Fraktur small a | `a` |

The last two examples illustrate normalization: a Unicode input does not always produce an `xn--` label.

### Copy a character

Open **Quick Copy List**, scroll to a letter group, and click a character button. Paste the copied text into a suitable Burp editor or another application. Copying does not display a confirmation dialog and replaces the current clipboard text.

### Use results in manual testing

Use the gallery to prepare controlled Unicode inputs for applications you are authorized to assess. Compare how the application displays, normalizes, stores, or validates the text. Keep the exact code points alongside your observations, since similar-looking characters can have different identities.

The extension does not send the input, modify intercepted traffic, or interpret a response. You control where and how copied characters are used.

## How encoding works

For each configured entry, `encode_punycode()`:

1. Attempts the runtime's `idna` codec and decodes its output as ASCII.
2. If that fails, attempts raw `punycode` encoding and prepends `xn--`.
3. Returns `None` if both attempts fail; the Generator omits that entry from its result table.

The displayed result does not identify which encoding path was used. **A raw Punycode fallback is not proof of a valid IDNA label.** IDNA includes processing and validity rules beyond the underlying Punycode algorithm. Output also depends on the codec implementation in the selected Jython runtime.

## Scope and limitations

- **Single-letter lookup:** the Generator retrieves a predefined group. It does not accept a complete domain, URL, or word, and does not generate combinations of whole-domain variants.
- **Encoding only:** there is no decoding interface, DNS lookup, domain availability check, registration check, or browser-rendering test.
- **Manual collection:** the map is not the Unicode confusables database and is not exhaustive. It includes 421 entries and 419 distinct entry strings; some strings appear in more than one group.
- **Map quality:** the supplied map includes a replacement character (`U+FFFD`) in the `d` group and a multi-character string (`вів`) in the `v` group. Visual similarity varies by font and context. Review entries before relying on them.
- **Validation behavior:** empty input, multiple characters, and digits are rejected. An unsupported alphabetic character can instead produce “No variants found for this letter.” Use ASCII `a`–`z` for predictable lookup.
- **Font coverage:** some glyphs may appear as boxes or look different across operating systems.
- **Two visible tabs:** the source builds a Web Symbols panel, but its `addTab` call is commented out. The shipped interface exposes **Generator** and **Quick Copy List** only.
- **Manual workflow:** no scanner checks, Intruder payload generator, context-menu integration, bulk export, or automatic traffic processing is implemented.

The supplied `punycode_tool.py` is published without functional changes.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `No module named burp`, `javax`, or `java` | Load the file through Burp with Jython, rather than CPython. |
| Extension fails to load | Check Burp's extension Errors tab and confirm the configured file is a Jython standalone JAR. |
| No suite tab appears | Check that the extension is enabled and initialized successfully. |
| Input has no variants | Enter one ASCII letter from `a` to `z`. |
| Some results are plain ASCII | IDNA normalization can map compatibility characters to ASCII. |
| A result is rejected as a domain label | Raw Punycode fallback does not enforce full IDNA or registry rules. |
| Characters appear as empty boxes | Check the desktop's font coverage for those Unicode ranges. |
| Clipboard copy fails | Use a graphical desktop with an accessible system clipboard; inspect the extension Errors tab. |

## Validation

A headless smoke test exercises real Swing components with minimal substitutes for the two Burp interfaces and callback methods. Run it from the repository directory with your own Jython JAR:

```bash
java -Djava.awt.headless=true -jar /path/to/jython-standalone.jar tests/smoke_test.py
```

The included test passed with Jython 2.7.5b1 on OpenJDK 21. It checks initialization, both visible tabs, all letter groups, all 421 generated rows, representative encodings, and input handling. It does **not** validate a live Burp installation, visual layout, clipboard access, or domain validity. See the test source for the exact assertions.

## Project structure

```text
punycode-pro-burp/
├── punycode_tool.py      # Burp extension and character map
├── README.md            # Setup, usage, encoding behavior, and limitations
├── CONTRIBUTING.md      # Contribution and issue-report guidance
├── .gitignore           # Local caches, IDE files, and runtime artifacts
└── tests/
    └── smoke_test.py     # Headless Jython/Swing smoke test
```

## Contributing

Issues and pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes to the map or encoding behavior. Include the relevant Unicode code points and your Burp, Jython, and Java versions when reporting a problem.

Use this tool only in environments you own or are authorized to test.

Maintained by [0xsheet](https://github.com/0xsheet).
