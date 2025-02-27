import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

st.set_page_config(page_title="AI Travel Planner", layout="centered", page_icon="✈️")


st.title("🌍 AI SmartTrip Planner")
st.write("### Plan your trip effortlessly with AI-powered travel recommendations! 🚆✈️🚌🚖")

# Input Fields
col1, col2 = st.columns(2)
with col1:
    source = st.text_input("📍 Source:", placeholder="Enter starting location")
with col2:
    destination = st.text_input("📍 Destination:", placeholder="Enter destination")

# Get Travel Plan Button
if st.button("🔍 Get Travel Plan"):
    if source and destination:
        with st.spinner("🔄 Finding best travel options..."):
            chat_template = ChatPromptTemplate(messages=[
                ("system", """
                You are an AI-powered travel assistant helping users find the best travel options.
                Provide travel options between the given source and destination, including:
                - Mode of transport (Cab, Bus, Train, Flight)
                - Estimated price 💰
                - Travel time ⏳
                - Important details (stops, transfers, best time to travel)
                Keep responses detailed, but clear and engaging, avoiding tabular formats.
                Conclude with a recommended best travel mode and the best time to travel.
                """),
                ("human", "Find travel options from {source} to {destination} along with estimated costs.")
            ])
            
            chat_model = ChatGoogleGenerativeAI(api_key=st.secrets["API_KEY"], model="gemini-2.0-flash-exp")
            parser = StrOutputParser()
            chain = chat_template | chat_model | parser
            
            response = chain.invoke({"source": source, "destination": destination})
            
            st.success("✅ Here are your travel options:")
            
            travel_modes = response.split("\n")
            for mode in travel_modes:
                if mode.strip():
                    st.markdown(f"🚀 {mode}")
            
            st.divider()
            st.markdown("💡 *Travel Smart & Safe! 🌍* ")
    else:
        st.error("⚠️ Please enter both Source and Destination.")
