# 🚀 Quick Start Guide

Get your Local RAG Debate Generator running in **5 minutes**!

## ⚡ Super Fast Setup (Windows)

1. **Run Setup**: Double-click `windows_setup.bat`
2. **Add PDFs**: Put PDF files in the `data` folder
3. **Create Database**: Run `python create_database.py`
4. **Generate Debate**: Run `python query_debate.py "Should AI be used in education?"`

## 🎯 Alternative: Manual Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama & Model
- Download Ollama from [ollama.com](https://ollama.com)
- Run: `ollama pull mistral`

### 3. Create Database
```bash
python create_database.py
```

### 4. Generate Your First Debate
```bash
python query_debate.py "Climate change solutions"
```

## 🌐 Web Interface (Optional)

```bash
python app.py
# Open browser to http://localhost:5000
```

## ✅ Test It Works

Try these example debates:
- `"Should universities use AI for grading?"`
- `"Is remote work better than office work?"`
- `"Should genetic engineering be allowed?"`
- `"Are social media platforms harmful?"`

## 🆘 Need Help?

- **Ollama not found?** Download from ollama.com
- **No database?** Run `python create_database.py` first
- **No PDFs?** Add files to `data` folder
- **Errors?** Check `README.md` troubleshooting section

## 📊 What You'll Get

```
PERSPECTIVE A: [Supporting argument]
- Point with evidence [Source: doc.pdf, Page 1]

PERSPECTIVE B: [Counter-argument]  
- Point with evidence [Source: doc.pdf, Page 2]

NEUTRAL SUMMARY: [Balanced view]
```

**Ready to start?** Follow the steps above! 🎓