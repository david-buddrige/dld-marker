# HTML Code Testing Program Documentation

## Overview

This Python program is designed to apply a series of tests on HTML files using regular expressions. It identifies common errors that would result in a student needing to fix and resubmit their code. The main focus of these tests is to ensure that files and directories are properly named and structured, that HTML follows best practices, and that images are appropriately formatted.

### Purpose
- The primary purpose of this program is to help evaluate HTML files by identifying potential issues such as:
  - Improper folder naming
  - Missing required files or directories
  - Improper HTML elements (`<span>`, `<img>` tags without `alt` attributes)
  - Files with improper naming conventions or file sizes
  - And much more.

### Inputs and Arguments
The program requires specific command-line arguments to function correctly. The arguments include:

1. **`-dir` (Required)**: The directory path to scan for HTML files and associated resources (CSS, JavaScript, images).
2. **`-pingDocs` (Optional)**: If specified, the program will avoid checking non-standard files (e.g., `.doc`, `.pdf`).
3. **`-webdev` (Optional)**: If specified, the program allows multiple `<div>` elements in HTML files.

### Constants
- **`IMAGE_TOO_BIG`**: Maximum file size (in bytes) for images. Images larger than this threshold will trigger an error.
- **`IMAGE_SIZE_WARNING`**: Maximum file size for images before a warning is issued.

## Functions

### `getRelativePathFromFullPath(fullPath)`
Converts a full path to a relative path by removing the base directory.

**Parameters**:
- `fullPath`: The full file path.

**Returns**:
- The relative path from the directory specified in the `-dir` argument.

---

### `printMessage(messageType, message)`
Prints a message to the console, prefixed with its message type (e.g., `INFO`, `ERROR`).

**Parameters**:
- `messageType`: The type of the message (e.g., `INFO`, `ERROR`).
- `message`: The message to be printed.

---

### `isAParam(theParam)`
Checks if a given parameter is a valid argument.

**Parameters**:
- `theParam`: The parameter to check.

**Returns**:
- `True` if the parameter is valid, `False` otherwise.

---

### `parseArgs()`
Parses the command-line arguments passed to the program and returns a dictionary of the argument values.

**Returns**:
- A dictionary where the keys are the argument names (e.g., `-dir`, `-pingDocs`) and the values are the argument values.

---

### `isValidDirOrFile(dirToCheck)`
Checks if a directory or file is valid, excluding known invalid files and directories.

**Parameters**:
- `dirToCheck`: The directory or file path to validate.

**Returns**:
- `True` if the directory/file is valid, `False` otherwise.

---

### `findAllDirectories(dirToFind)`
Recursively finds all directories within the given directory, excluding invalid ones.

**Parameters**:
- `dirToFind`: The directory to search.

**Returns**:
- A list of all valid directories.

---

### `findAllFiles(dirToCheck)`
Finds all files within a directory.

**Parameters**:
- `dirToCheck`: The directory to search.

**Returns**:
- A list of all valid files.

---

### `checkForUpper(folderName)`
Checks if a folder contains any uppercase characters, which is considered a violation of naming standards.

**Parameters**:
- `folderName`: The folder name to check.

---

### `hasRequiredDirsAndFiles(dirToCheck)`
Checks if the specified directory contains all the required directories (CSS, JS, Images) and the `index.html` file.

**Parameters**:
- `dirToCheck`: The directory to check.

---

### `testForSpan(htmlLine, lineNumber, htmlFile)`
Tests if a line in the HTML file contains a `<span>` tag, which is considered a violation of standards.

**Parameters**:
- `htmlLine`: The HTML line to check.
- `lineNumber`: The line number in the HTML file.
- `htmlFile`: The path to the HTML file.

---

### `directoryContainsAHtmlFile(dirToCheck)`
Checks if a directory contains at least one HTML file.

**Parameters**:
- `dirToCheck`: The directory to check.

**Returns**:
- `True` if the directory contains at least one HTML file, `False` otherwise.

---

### `testAHtmlFile(htmlFilePath, paramsDictionaryToUse)`
Tests an HTML file for various violations such as:
- Multiple `<div>` tags (if `-webdev` flag is not specified).
- Missing `alt` attribute in `<img>` tags.
- Improper file formatting (e.g., uppercase HTML tags).

**Parameters**:
- `htmlFilePath`: The path to the HTML file to test.
- `paramsDictionaryToUse`: The dictionary containing the parsed command-line arguments.

---

### `isOneOfTheAcceptableNonStandardFiles(filePath)`
Checks if a file is one of the accepted non-standard files (e.g., `.doc`, `.pdf`).

**Parameters**:
- `filePath`: The path to the file.

**Returns**:
- `True` if the file is acceptable, `False` otherwise.

---

### `checkFile(filePath)`
Checks a file for common issues such as:
- Uppercase letters in filenames.
- Spaces in filenames.

**Parameters**:
- `filePath`: The path to the file to check.

---

### `checkIfImage(imageFilename)`
Checks an image file for issues such as:
- File size (too large or warning level).
- Uppercase letters or spaces in the filename.

**Parameters**:
- `imageFilename`: The path to the image file.

---

## Example Usage

To run the program, use the following command format:

```bash
python html-tester.py -dir <path_to_directory> [-pingDocs] [-webdev]
```

### Example:

```bash
python html-tester.py -dir /path/to/project -pingDocs
```

This command will process the directory at `/path/to/project`, ignore non-standard files (like `.doc` or `.pdf`), and print the results to the console.

## Error and Warning Messages

The program generates messages to inform users of potential issues in their HTML code. These include:
- **INFO**: General information about the processing.
- **WARNING**: A potential issue that may need attention.
- **ERROR**: A critical issue that must be addressed immediately.
- **LABEL**: A separator used to demarcate sections in the output.

## Conclusion

This program is a helpful tool for evaluating HTML files and ensuring they adhere to best practices. By running it against your project directory, you can catch common errors and improve the quality of your HTML code before submitting.