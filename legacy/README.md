# Legacy Flask prototype

This is the original single-file Flask prototype of SpeedRead, kept for
history/reference. It has been fully superseded by the current MVP:

- Backend: [`backend/`](../backend/) — FastAPI (see `backend/app/routers/`,
  which ports this prototype's arithmetic-generation logic).
- Frontend: [`flutter_app/`](../flutter_app/) — Flutter app.

## Running it (if you ever need to)

This prototype needs its own dependencies — **do not** install them into
`backend/.venv`, which is for the FastAPI backend only.

```
cd legacy
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
