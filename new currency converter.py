import streamlit as st
import requests
import pandas as pd

# Function to fetch exchange rate
def get_exchange_rate(from_currency, to_currency):
    """
    Fetches the exchange rate for the given currencies from the API.
    """
    api_key = "8483359d1712d0cbc49ec998"  
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rates = data["conversion_rates"]
            if to_currency in rates:
                return rates[to_currency]
            else:
                st.error(f"Currency {to_currency} is not available.")
                return None
        else:
            st.error(f"Error: Unable to fetch exchange rate. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error: Unable to connect to the API. Details: {str(e)}")
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="ForexFlex: Seamless Currency Converter", layout="centered")
    
    # Add custom CSS and HTML for background and animation
    st.markdown("""
        <style>
            /* Background Gradient */
            .stApp {
                background: linear-gradient(135deg, #f0e68c, #dcdcdc);
                color: #333333;
                font-family: 'Arial', sans-serif;
            }
            
            /* Floating Coins Animation */
            .coin {
                position: absolute;
                animation: float 5s infinite ease-in-out;
                z-index: 1;
            }
            @keyframes float {
                0% { transform: translateY(100vh); }
                50% { transform: translateY(50vh); }
                100% { transform: translateY(-10vh); }
            }
            .coin1 { left: 15%; animation-delay: 0s; }
            .coin2 { left: 40%; animation-delay: 2s; }
            .coin3 { left: 65%; animation-delay: 4s; }
            
            /* Styling for Sidebar (History Tab) */
            .history-card {
                background-color: #e0f7fa;  /* Light cyan background */
                border-radius: 8px;
                border: 1px solid #00796b;  /* Darker green border */
                padding: 15px;
                margin-bottom: 12px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            .history-card:hover {
                transform: translateY(-5px);
                background-color: #b2ebf2;  /* Light blue on hover */
            }
            .history-card-title {
                font-size: 1.2em;
                font-weight: bold;
                color: #004d40;  /* Dark green */
            }
            .history-card-details {
                font-size: 1em;
                color: #555;
                margin: 5px 0;
            }
            .history-card .rate {
                font-weight: bold;
                color: #0288d1;  /* Blue for the rate */
            }
            .history-card .converted-amount {
                font-weight: bold;
                color: #e91e63;  /* Pink for the converted amount */
            }
        </style>
        <div class="coin coin1">🪙</div>
        <div class="coin coin2">💰</div>
        <div class="coin coin3">🪙</div>
    """, unsafe_allow_html=True)

    # Header
    st.title("💱 ForexFlex: Seamless Currency Converter")
    st.subheader("Navigate Exchange Rates with Ease")

    # Load and format currency options
    try:
        currency_data = pd.read_csv(r"C:\Users\Shrinivass\Downloads\currency_list.csv")
        currency_options = currency_data['Code'] + " (" + currency_data['Name'] + ")"
    except Exception as e:
        st.error(f"Error loading currency list: {str(e)}")
        return
    
    # Initialize session state for conversion history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Input form
    with st.form("currency_converter_form"):
        st.markdown("### Enter Currency Details")
        col1, col2 = st.columns(2)
        with col1:
            from_currency = st.selectbox("Convert from:", currency_options)
        with col2:
            to_currency = st.selectbox("Convert to:", currency_options)

        from_currency_code = from_currency.split(" ")[0]
        to_currency_code = to_currency.split(" ")[0]

        amount = st.number_input("Enter the amount to convert:", min_value=0.0, step=1.0)
        submit_button = st.form_submit_button("Convert")

    # Handle form submission
    if submit_button:
        if from_currency_code and to_currency_code and amount > 0:
            rate = get_exchange_rate(from_currency_code, to_currency_code)
            if rate:
                converted_amount = amount * rate
                st.success(f"### {amount} {from_currency_code} = {converted_amount:.2f} {to_currency_code}")
                st.metric(label="Exchange Rate", value=f"{rate:.4f}", delta=f"{rate - 1:.4f}")
                
                # Save conversion to history
                conversion_details = {
                    "From": from_currency,
                    "To": to_currency,
                    "Amount": amount,
                    "Converted Amount": converted_amount,
                    "Rate": rate
                }
                st.session_state.history.append(conversion_details)
        else:
            st.warning("Please complete all fields and enter a valid amount.")

    # Sidebar for Conversion History (Sideways Tab)
    st.sidebar.title("Conversion History")
    if st.session_state.history:
        for conversion in st.session_state.history:
            st.sidebar.markdown(f"""
            <div class="history-card">
                <div class="history-card-title">
                    {conversion['Amount']} {conversion['From']} → {conversion['Converted Amount']:.2f} {conversion['To']}
                </div>
                <div class="history-card-details">
                    <span><b>Rate:</b> <span class="rate">{conversion['Rate']:.4f}</span></span><br>
                    <span><b>Converted Amount:</b> <span class="converted-amount">{conversion['Converted Amount']:.2f} {conversion['To']}</span></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.sidebar.markdown("""
        <div class="history-card">
            No conversion history available.
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <hr>
        <div style="text-align:center; font-size:14px; color:#333333;">
            Created by <b>R.Shrinivass</b>. Powered by ExchangeRate-API.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
