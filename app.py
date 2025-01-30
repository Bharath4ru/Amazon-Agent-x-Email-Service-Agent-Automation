import streamlit as st
import requests
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Amazon Product Search & Email Service",
    page_icon="🛍️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF9900;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #FF8000;
    }
    .success-msg {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    .error-msg {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        color: #721c24;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def query_amazon_agent(api_key, external_user_id, user_query):
    with st.spinner('Querying Amazon... Please wait'):
        create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
        headers = {'apikey': api_key}
        create_session_body = {
            "pluginIds": [],
            "externalUserId": external_user_id
        }

        response = requests.post(create_session_url, headers=headers, json=create_session_body)
        if response.status_code == 201:
            session_id = response.json()['data']['id']
            submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
            submit_query_body = {
                "endpointId": "predefined-openai-gpt4o",
                "query": user_query,
                "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1716334779"],
                "responseMode": "sync"
            }
            
            response = requests.post(submit_query_url, headers=headers, json=submit_query_body)
            if response.status_code == 200:
                return response.json()['data']['answer']
            else:
                return f"Error: Unable to get Amazon results. Status code: {response.status_code}"
        else:
            return f"Error: Unable to create session. Status code: {response.status_code}"

def send_email(api_key, external_user_id, amazon_output, recipient_email):
    with st.spinner('Sending email... Please wait'):
        create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
        headers = {'apikey': api_key}
        create_session_body = {
            "pluginIds": [],
            "externalUserId": external_user_id
        }

        response = requests.post(create_session_url, headers=headers, json=create_session_body)
        if response.status_code == 201:
            session_id = response.json()['data']['id']
            submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
            # Construct the email query
            submit_query_body = {
                "endpointId": "predefined-openai-gpt4o",
                "query": f"send mail to {recipient_email} with body '{amazon_output}' and subject: 'Amazon Product Search Results - {datetime.now().strftime('%Y-%m-%d')}'",
                "pluginIds": ["plugin-1712327325", "plugin-1713962163", "plugin-1722285968"],
                "responseMode": "sync"
            }

            query_response = requests.post(submit_query_url, headers=headers, json=submit_query_body)
            if query_response.status_code == 200:
                return True
            else:
                return False
        return False

def main():
    # Header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://i.pinimg.com/originals/01/ca/da/01cada77a0a7d326d85b7969fe26a728.jpg", width=64)
    with col2:
        st.title("Amazon Product Search & Email Service")
    
    st.markdown("---")

    # Create two columns for better layout
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("🔑 Authentication")
        with st.expander("Enter Credentials", expanded=True):
            api_key = st.text_input("API Key", type="password", help="Enter your API key for authentication")
            external_user_id = st.text_input("User ID", help="Enter your user identification number")

        st.subheader("📧 Email Settings")
        with st.expander("Email Configuration", expanded=True):
            email = st.text_input("Recipient Email", help="Enter the email address to receive the results")

    with right_col:
        st.subheader("🔍 Search Configuration")
        with st.expander("Search Parameters", expanded=True):
            product_query = st.text_input("Product Search", 
                                        placeholder="Enter product name or description (e.g., wireless headphones, gaming laptop)",
                                        help="Enter what you're looking for on Amazon")
            max_price = st.text_input("Maximum Price (₹)", 
                                    placeholder="Enter maximum price (e.g., 50000)",
                                    help="Enter the maximum price you want to pay")
            
            # Construct the search query
            if product_query and max_price:
                try:
                    max_price = float(max_price)
                    amazon_query = f"{product_query} from amazon under {max_price} price"
                except ValueError:
                    st.error("Please enter a valid number for the price")
                    amazon_query = None
            else:
                amazon_query = None

        search_button = st.button("🔍 Search and Send Results", use_container_width=True)

    # Process the search and email
    if search_button:
        if not all([api_key, external_user_id, email, amazon_query]):
            st.error("Please fill in all required fields!")
            return

        # Query Amazon
        amazon_output = query_amazon_agent(api_key, external_user_id, amazon_query)
        
        # Display results
        st.markdown("### 📊 Search Results")
        st.info(amazon_output)

        # Send email
        if amazon_output:
            if send_email(api_key, external_user_id, amazon_output, email):
                st.markdown(
                    """
                    <div class="success-msg">
                        ✅ Email sent successfully! Check your inbox for the results.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="error-msg">
                        ❌ Failed to send email. Please try again.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
