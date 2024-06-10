#!/bin/bash
pip install pytest os sqlite3
bash pipeline.sh
pytest pipelinetest.py