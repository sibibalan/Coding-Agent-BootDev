````markdown
# Coding Agent CLI

A command-line tool that helps you **fix and modify code automatically** by delegating tasks to a set of predefined functions.  
Just describe the issue in natural language, and the agent will attempt to scan, read, modify, and run your files until the problem is solved (or it fails miserably 😅).

---

## 🚀 What Does the Agent Do?

The agent works in a loop of:

1. **Accepting a coding task**  
   Example:  
   ```bash
   uv run main.py "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽"
````

2. **Choosing from a set of predefined functions** such as:

   * `get_files_info` → Scan the files in a directory
   * `get_file_content` → Read a file's contents
   * `write_file` → Overwrite a file's contents
   * `run_python_file` → Execute the Python interpreter on a file

3. **Repeating step 2** until:

   * The task is complete ✅
   * Or it fails miserably ❌

---

## 🧑‍💻 Example

I had a buggy calculator app that wasn’t starting correctly. Using the agent:

```bash
uv run main.py "fix my calculator app, its not starting correctly"
```

The agent worked like this:

```
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. 
# The output shows the expression and the result in a formatted way.
```

---

## 📦 Prerequisites

Make sure you have the following installed:

* **Python 3.10+**
  (See the [bookbot project](#) if you need help setting it up)

* **[uv](https://github.com/astral-sh/uv)** project and package manager
  (used to manage dependencies and run the CLI)

* **Unix-like shell**
  (e.g., `zsh`, `bash`, or WSL on Windows)

---

## 🏃 Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/sibibalan/Coding-Agent-BootDev.git
   cd coding-agent
   ```

2. Initialize the project:

   ```bash
   uv init
   ```

3. Run the agent with a natural language task:

   ```bash
   uv run main.py "describe your bug here"
   ```

---

## ⚠️ Disclaimer

This tool is experimental and may not always succeed. Sometimes it fixes your code beautifully, other times it fails spectacularly. Use it at your own risk (and keep backups of your files 😉).

---

## 📜 License

MIT License – feel free to use, modify, and share!

```

---

