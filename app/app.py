import numpy as np
import pandas as pd
import streamlit as st
from pipeline.stages.translate.translate import TranslateStage
from pipeline.stages.llm.llm_translate import LLMTranslateStage
from pipeline.stages.llm.llm_tagger import LLMTaggerStage
from pipeline.stages.api.rest_api import ApiController
from pipeline.stages.api.model.search_result import SearchResult
from pipeline.stages.crawler.crawler import CrawlerStage
from pipeline.stages.nlp.nlp import NLP_Lemmatizer
from pipeline.stages.nlp.ontology.nltk_wordnet import NLTKWordNet
from settings import settings
from result_model import ResultItem


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
nlp_lemmatizer = NLP_Lemmatizer()
nltk_word_net = NLTKWordNet()

# Set RTL direction
st.markdown("""<style>body {direction: rtl;}</style>""", unsafe_allow_html=True)

# Initialize query submitted state
st.session_state.setdefault("query_submitted", False)

# Sidebar content
st.sidebar.image("docs/team.png", use_column_width=True)

st.sidebar.header("المعاملات:")
words_num = st.sidebar.number_input("عدد الكلمات المستخلصة:", min_value=1, value=10, step=1, format="%d")

option1 = Option("ترجمة آلية", 1)
option2 = Option("نموذج اللغة الضخم LLM", 2)
options = [option1, option2]
translation_option = st.sidebar.radio("اختر طريقة الترجمة:", options, format_func=lambda option: option.name)

api_option1 = Option("إيقاف", 1)
api_option2 = Option("تفعيل", 2)
api_options = [api_option1, api_option2]
api_option = st.sidebar.radio("الارتباط مع المعجم:", api_options, format_func=lambda option: option.name)

st.header("الإثراء الرقمي")
st.divider()
st.markdown("#### ضع رابط مقالة من الويكيبيديا الانكليزية:")
query = st.text_input("", "https://en.wikipedia.org/wiki/Banlic_station", key="txt_area_query")
def submit_query():
    st.session_state["query_submitted"] = True

submit_btn = st.button("عالج المحتوى", on_click=submit_query, key="submit")

@st.cache_data
def fetch_data(query):
    title, crawled_texts = crawler_stage.crawl_page(query)
    ar_text = []
    for crawled_text in crawled_texts:
        translated_text = translate_stage.translate_ar(crawled_text)
        ar_text.append(translated_text)

    words = nlp_lemmatizer.lemmatize(ar_text)
    words_items = nlp_lemmatizer.lookup_ontology(words[:words_num])

    word_count_list = []
    for word_item in words_items:
        if api_option.id == 2:
            found_status = apiController.api_search(word_item.word)
            if found_status == SearchResult.FOUND:
                found_status = True
            else:
                found_status = False
        else:
            found_status = False
        word_count_list.append(
            ResultItem(
                word=word_item,
                enrichment=0,
                translation= translate_stage.translate_en(word_item.word),
                nltk= list(nltk_word_net.get_synonyms_antonyms(word_item.word).get('synonyms', set())),
                ner= llm_tagger_stage.tag([word_item.word]),
                # pause lookup to reserve quota
                found = found_status
            )
        )

    word_count_list_sorted = sorted(word_count_list, key=lambda item: len(item.word.senses), reverse=True)

    table_dicts = [
        {
            'word': item.word.word,
            'translate': item.translation,
            'nltk': item.nltk,
            'ner': item.ner,
            'type': item.word.type,
            'senses': item.word.senses,
            'meaning': item.word.meaning,
            'found': item.found
        } for item in word_count_list_sorted
    ]

    table_df = pd.DataFrame(table_dicts)
    return table_df

clear_cache_button = st.sidebar.button("Clear Cache")
if clear_cache_button:
    fetch_data.clear()
    st.session_state["query_submitted"] = False

def perform_action(word):
    if api_option.id == 2:
        apiController.api_create(apiController.create_obj(word))
    st.write("تم إضافة الكلمات المحددة:", word)

if st.session_state.get("query_submitted"):
    st.markdown("#### النتائج:")
    st.divider()
    table_df = fetch_data(query)

    s0 = dict(selector='tr', props=[('width', '100%')])
    s1 = dict(selector='th', props=[('text-align', 'center')])
    s2 = dict(selector='td', props=[('text-align', 'center')])
    
    selected_indices = []
    data_dict = {}
    for index, row in table_df.iterrows():
        data_dict.update({index: row})
        col1, col2, col3, col4, col5, col6 = st.columns((1, 2, 2, 1, 1, 1))
        checkbox_value = col1.checkbox(label=f"{index}", key=f"checkbox_{index}", label_visibility="hidden")
        if checkbox_value:
            selected_indices.append(index)
        col2.write(row['word'])
        col3.write(row['type'])
        col4.write(row['translate'])

        button_phold = col5.empty()
        if row['found'] == False:
            button_type = "إضافة"
            do_action = button_phold.button(button_type, key=f"button_{index}")
            if do_action:
                perform_action(row['word'])
        else:
            button_type = "موجودة"
            button_phold.button(button_type, key=f"button_{index}", disabled=True)
        placeholder = col6.empty()
        show_more = placeholder.button("المزيد", key=index, type="primary")
        if show_more:
            placeholder.button("إغلاق", key=str(index)+"_")
            st.markdown('<b><span style="color: braun; text-decoration: underline;">الإثراء الدلالي للكلمة:</span></b>', unsafe_allow_html=True)
            if len(row['nltk']) > 0:
                st.markdown('<b><span style="color: blue; text-decoration: underline;">الإثراء الأنطولوجي:</span></b>', unsafe_allow_html=True)
                st.write("  - " + "\n- ".join([f"**{row['nltk']}**"]))
            st.markdown('<span style="color: red; text-decoration: underline;">النوع:</span>', unsafe_allow_html=True)
            st.write("  - " + "\n- ".join([f"**{row['type']}**"]))
            if row['meaning']:
                st.markdown('<span style="color: red; text-decoration: underline;">المعنى:</span>', unsafe_allow_html=True)
                translated_meaning = translate_stage.translate_ar(row['meaning'])
                translated_meaning_array = translated_meaning.split("؛")
                st.write("  - " + "\n- ".join([f"{meaning}" for meaning in translated_meaning_array]))
            if len(row['senses']) > 0:
                st.markdown('<span style="color: red; text-decoration: underline;">العلاقات:</span>', unsafe_allow_html=True)
                st.write("  - " + "\n- ".join([f"**{key}:** {value}" for key, value in row['senses']]))
            st.write("---")

    if st.button("أضف الكلمات المحددة"):
        for selected_key in selected_indices:
            selected_item = data_dict.get(selected_key)
            if api_option.id == 2:
                apiController.api_create(apiController.create_obj(selected_item['word']))
            st.write("تم إضافة الكلمات المحددة:", selected_item['word'])
