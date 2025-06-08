import streamlit as st

from document_processor import extract_text_from_pdf, chunk_text, build_vector_store
from QA import answer_question
from compliance import check_compliance, check_compliance_HTML
from pdf_utils import generate_pdf_from_html
from speech_recog import recognize_speech
from tts import TextToSpeech
import threading

tts = TextToSpeech()

def speak_text(text):
    thread = threading.Thread(target=tts.speak, args=(text,))
    thread.start()
    return thread

def stop_speech_now():
    tts.stop()

def process_document(pdf_doc):
    if 'raw_text' not in st.session_state or not st.session_state.raw_text:
        with st.spinner("Processing document..."):
            raw_text = extract_text_from_pdf(pdf_doc)
            chunks = chunk_text(raw_text)
            vector_store, stored_chunks = build_vector_store(chunks)

            st.session_state.raw_text = raw_text
            st.session_state.chunks = stored_chunks
            st.session_state.vector_store = vector_store

            # Summary generation
            from summarizer import generate_summary
            if 'summary' not in st.session_state or not st.session_state.summary:
                st.session_state.summary = generate_summary(raw_text)



def show_main_page():
    st.title("Contract Analysis & QA System 📄")
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("Upload Document")
        pdf_doc = st.file_uploader("Upload Contract (PDF)", type="pdf")
        
        if pdf_doc:
            process_document(pdf_doc)
            st.success("Document processed!")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📝 Document Summary", "❓ Question & Answer", "📊 Compliance Report"])
    
    # Summary Tab
    with tab1:
        if hasattr(st.session_state, 'summary') and st.session_state.summary:
            st.header("Document Summary")
            st.write(st.session_state.summary)
    
    # Q&A Tab
    with tab2:
        if hasattr(st.session_state, 'summary') and st.session_state.summary:
            st.header("Ask Questions")

            if 'question' not in st.session_state:
                st.session_state.question = None

            input_method = st.radio("Choose input method:", ("Text", "Speech"))

            if input_method == "Text":
                question = st.text_input("Enter your question about the document:")
                if question:
                    st.session_state.question = question
            else:
                if st.button("Click to Speak", key="speak_qa"):
                    spoken_text = recognize_speech()
                    if spoken_text:
                        st.session_state.question = spoken_text
                        st.write(f"You asked: {spoken_text}")

            if st.session_state.question:
                if st.session_state.vector_store is not None:
                    answer_key = f"answer_{st.session_state.question}"
                    if answer_key not in st.session_state:
                        with st.spinner("Finding answer..."):
                            st.session_state[answer_key] = answer_question(
                                st.session_state.question,
                                st.session_state.vector_store,
                                st.session_state.chunks
                            )

                    st.subheader("Answer")
                    st.write(st.session_state[answer_key])

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("Play Answer", key="play_answer"):
                            if 'speech_thread' not in st.session_state:
                                st.session_state.speech_thread = None
                            if st.session_state.speech_thread is not None:
                                stop_speech_now()
                            st.session_state.speech_thread = speak_text(st.session_state[answer_key])
                            st.success("Playing answer...")

                    with col2:
                        if st.button("Stop Audio", key="stop_audio"):
                            stop_speech_now()
                            if 'speech_thread' in st.session_state:
                                st.session_state.speech_thread = None
                            st.info("Audio stopped")

                    with col3:
                        if st.button("Clear Question", key="clear_qa"):
                            stop_speech_now()
                            if 'speech_thread' in st.session_state:
                                st.session_state.speech_thread = None
                            st.session_state.question = None
                            st.rerun()
                else:
                    st.error("Please upload a document first.")
        else:
            st.info("Please upload a contract document to start asking questions.")

    # Compliance Report Tab
    with tab3:
        st.header("Compliance Report")
        if hasattr(st.session_state, 'raw_text') and st.session_state.raw_text:
            if 'compliance_report' not in st.session_state:
                st.session_state.compliance_report = None

            if st.button("Generate Compliance Report", key="gen_compliance"):
                with st.spinner("Analyzing compliance..."):
                    st.session_state.compliance_report = check_compliance(st.session_state.raw_text)

            if st.session_state.compliance_report:
                st.markdown(st.session_state.compliance_report)
                compliance_report_HTML_format = check_compliance_HTML(st.session_state.compliance_report)

                col1, col2 = st.columns(2)
                with col1:
                    if st.download_button(
                        label="Download PDF Report",
                        data=generate_pdf_from_html(compliance_report_HTML_format),
                        file_name="Compliance_report.pdf",
                        mime="application/pdf"
                    ):
                        st.success("PDF downloaded successfully!")
        else:
            st.info("Please upload a contract document to generate a compliance report.")
