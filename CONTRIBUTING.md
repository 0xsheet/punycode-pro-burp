# Contributing

Thank you for helping improve Punycode Pro Tool.

## Reporting a problem

Open a GitHub issue with:

- Burp Suite edition and version.
- Jython standalone JAR version, Java version, and operating system.
- The input letter and exact Unicode code points involved.
- Steps to reproduce, expected behavior, and actual behavior.
- Relevant extension error output with any private data removed.

Use synthetic examples or reserved example domains. Do not include credentials, private traffic, customer data, or details of systems you are not authorized to test.

## Proposing a change

1. Fork the repository and create a focused branch.
2. Keep `punycode_tool.py` compatible with Jython's Python 2.7 syntax and Burp's legacy Extender API.
3. Preserve UTF-8 encoding and explicit `u` prefixes on Unicode literals.
4. For character-map changes, include the code point, Unicode name, intended letter group, and a reason for inclusion or removal. Distinguish single characters from multi-character sequences.
5. For encoding changes, explain normalization and fallback behavior. Raw Punycode output must not be presented as proof of IDNA validity.
6. Update the README and smoke-test expectations if behavior or map counts change.
7. Run the headless smoke test described in the README, then load the extension in Burp and manually check both visible tabs and clipboard buttons.
8. Submit a pull request describing the change and the checks you actually completed.

Avoid unrelated formatting changes to the character map. Do not commit runtime JARs, generated class files, Burp project files, logs, or secrets.
