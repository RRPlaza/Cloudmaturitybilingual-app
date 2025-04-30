@echo off
echo Starting CloudMature Risk Solutions App...
call cloudmaturityenv\Scripts\activate
streamlit run app_local.py
pause