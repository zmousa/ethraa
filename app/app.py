import numpy as np
import pandas as pd
import streamlit as st
from pipeline.stages.translate.translate import TranslateStage
from pipeline.stages.llm.llm_translate import LLMTranslateStage
from pipeline.stages.llm.llm_tagger import LLMTaggerStage
from pipeline.stages.api.rest_api import ApiController
from pipeline.stages.crawler.crawler import CrawlerStage
from settings import settings


st.set_page_config(
    page_title="الإثراء الرقمي",
    page_icon=":airplane:",
    layout="wide"
)

class Option:
    def __init__(self, name, option_id):
        self.name = name
        self.id = option_id

crawler_stage = CrawlerStage()
translate_stage = TranslateStage()
llm_translate_stage = LLMTranslateStage()
llm_tagger_stage = LLMTaggerStage()
apiController = ApiController(settings)

# Set RTL direction
st.markdown("""<style>body {direction: rtl;}</style>""", unsafe_allow_html=True)

# Initialize query submitted state
st.session_state.setdefault("query_submitted", False)

# Sidebar content
st.sidebar.header("المعاملات:")
words_num = st.sidebar.number_input("عدد الكلمات:", min_value=1, value=10, step=1, format="%d")

option1 = Option("ترجمة آلية", 1)
option2 = Option("نموذج اللغة الضخم LLM", 2)
options = [option1, option2]
translation_option = st.sidebar.radio("اختر طريقة الترجمة:", options, format_func=lambda option: option.name)

## MAIN
st.header("النص")
query = st.text_input("", "https://en.wikipedia.org/wiki/El_Dorado_Fire", key="txt_area_query")
def submit_query():
    st.session_state["query_submitted"] = True
    

submit_btn = st.button("حلل", on_click=submit_query, key="submit")

if st.session_state.get("query_submitted"):
    st.divider()
    st.header("النتائج")
    
    title, crawled_texts = crawler_stage.crawl_page(query)
    st.header(title.text if title else "")
    words = []
    for crawled_text in crawled_texts:
        translated_text = translate_stage.translate_ar(crawled_text)
        words.append(translated_text.split())
    words = [item for sublist in words for item in sublist]
    word_counts = pd.Series(words).value_counts().head(words_num)
    
    s0 = dict(selector='tr', props=[('width', '100%')])
    s1 = dict(selector='th', props=[('text-align', 'center')])
    s2 = dict(selector='td', props=[('text-align', 'center')])

    table_df = pd.DataFrame({"الكلمة": word_counts.index, "التكرار": word_counts.values})
    if translation_option.id == 1:
        table_df["Translation"] = table_df["الكلمة"].apply(translate_stage.translate_en)
    elif translation_option.id == 2:
        table_df["Translation"] = table_df["الكلمة"].apply(llm_translate_stage.translate)

    table = table_df.style.set_table_styles([s0,s1,s2]).to_html()
    st.write(f'{table}', unsafe_allow_html=True)
    
    # Test api call
    # search_result = apiController.api_search("كلمة")
    # print(search_result)
    
    # Test tagger
    # test_parts = ['هذا', 'علي خليل', 'محمد', 'يأكل', 'معجم', 'كلام', 'دمشق']
    # llm_tagger_stage.tag(test_parts)
