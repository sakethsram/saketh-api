#!/bin/bash
source /home/saketh/venv/ecom/bin/activate
uvicorn app.main:app --reload
