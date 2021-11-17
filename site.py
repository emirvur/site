
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

import aiohttp
import asyncio
import requests as request
import pandas as pd
import speech_recognition as sr
from sumapi.api import SumAPI

stt_button = Button(label="Speak", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        r = sr.Recognizer()
        #message=r.recognize_google(result.get("GET_TEXT"), language='tr-tr')
        api = SumAPI(username='GSUINF443', password='wHxuqxdQ95cT')
        print("basladi")
        reply=api.sentiment_analysis(result.get("GET_TEXT"), domain='general')
        st.write(reply['evaluation']['label'])