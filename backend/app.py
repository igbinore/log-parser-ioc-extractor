from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Optional
import io, re, pandas as pd, json

app = FastAPI(title="Log Parser & IOC Extractor", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Practical regexes for demo
PATTERNS = {
    "ipv4":   re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"),
    "domain": re.compile(r"\b(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+(?:[A-Za-z]{2,24})\b"),
    "url":    re.compile(r"\b(?:https?://|ftp://)[^\s\"'>)]+", re.IGNORECASE),
    "email":  re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,24}\b"),
    "md5":    re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "sha1":   re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "sha256": re.compile(r"\b[A-Fa-f0-9]{64}\b"),
}

def extract_text(text: str) -> pd.DataFrame:
    rows = []
    for ioc_type, rx in PATTERNS.items():
        for m in rx.findall(text or ""):
            rows.append({"type": ioc_type, "value": m})
    df = pd.DataFrame(rows, columns=["type","value"])
    if df.empty:
        return pd.DataFrame(columns=["type","value","count"])
    # Deduplicate and count occurrences per (type, value)
    df = (
        df.groupby(["type","value"])
          .size()
          .reset_index(name="count")
          .sort_values(["type","count","value"], ascending=[True, False, True])
          .reset_index(drop=True)
    )
    return df

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/extract")
async def extract_iocs(file: UploadFile | None = File(default=None),
                       text: Optional[str] = Form(default=None)):
    content = ""
    if file is not None:
        content = (await file.read()).decode("utf-8", errors="ignore")
    if text:
        content = (content + "\n" + text) if content else text

    df = extract_text(content)
    total = int(df["count"].sum()) if not df.empty else 0
    by_type = df.groupby("type")["count"].sum().to_dict() if not df.empty else {}

    return JSONResponse({
        "total": total,
        "by_type": by_type,
        "items": df.to_dict(orient="records")  # [{type, value, count}]
    })

@app.post("/export")
async def export(format: str = Form(...), items: str = Form(...)):
    """
    Accepts items (JSON list of {type,value,count}) and returns CSV or JSON file.
    """
    data = json.loads(items)
    df = pd.DataFrame(data)
    if format.lower() == "csv":
        buf = io.StringIO()
        cols = ["type","value","count"] if not df.empty else ["type","value","count"]
        df.to_csv(buf, index=False, columns=cols)
        buf.seek(0)
        return StreamingResponse(
            io.BytesIO(buf.getvalue().encode("utf-8")),
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="iocs.csv"'}
        )
    # JSON default
    blob = json.dumps(data, indent=2).encode("utf-8")
    return StreamingResponse(
        io.BytesIO(blob),
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="iocs.json"'}
    )
