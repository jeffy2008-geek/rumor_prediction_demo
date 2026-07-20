import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

if __name__ == '__main__':
    
    # 1. Page settings
    st.set_page_config(
        page_title="𝕏 Rumor Live Feed", 
        page_icon="🚨", 
        layout="wide"
    )

    # Custom CSS for clean scrolling feed blocks
    st.markdown("""
    <style>
        .scroll-box {
            height: 400px;
            overflow-y: scroll;
            border: 1px solid #e6e9ef;
            border-radius: 8px;
            padding: 15px;
            background-color: #f8f9fa;
        }
        .post-card {
            background-color: white;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border-left: 5px solid #ff4b4b;
        }
        .post-card-pred {
            border-left: 5px solid #ffa500;
        }
        .post-date {
            font-size: 0.8rem;
            color: #6c757d;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🚨 Potential NBA Rumors on X")
    st.markdown("Potential NBA Rumors Updated Daily", unsafe_allow_html=True)

    # 2. Mock Dataset Creator
    @st.cache_data(ttl=600)
    def load_rumor_data():
        return pd.read_csv('rumors.csv')
        
    # Read the file
    df = load_rumor_data()
    df['DATE_OBJ'] = pd.to_datetime(df['DATE']).dt.date

    # 3. Sidebar Filtering Logic (Defaulting to the Most Recent Date)
    st.sidebar.header("Timing Your Rumors")
    unique_dates = sorted(df['DATE_OBJ'].unique())

    if unique_dates:
        min_date = unique_dates[0]
        max_date = unique_dates[-1] # The most recent date in the file
        
        # Setting default value range to start and end on the max_date
        selected_range = st.sidebar.date_input(
            "Select Time Window:",
            value=(max_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if isinstance(selected_range, tuple) and len(selected_range) == 2:
            start_date, end_date = selected_range
            filtered_df = df[(df['DATE_OBJ'] >= start_date) & (df['DATE_OBJ'] <= end_date)].copy()
        else:
            start_date = selected_range[0]
            end_date = start_date
            filtered_df = df[df['DATE_OBJ'] == start_date].copy()
    else:
        filtered_df = df.copy()
        st.sidebar.warning("No valid dates found in file.")

    # 4. Multi-Keyword Filtering Logic
    keyword_query = st.text_input(
        "🔍 Filter posts by keywords (separate with spaces):", 
        placeholder="e.g. 'Lebron Curry' or 'Lebron Cavaliers'"
    )

    if keyword_query:
        keywords = [kw.strip().lower() for kw in keyword_query.split(" ") if kw.strip()]
        for kw in keywords:
            filtered_df = filtered_df[filtered_df['POST'].str.lower().str.contains(kw, na=False)]

    # Update sidebar status text dynamically
    st.sidebar.write(f"Active Window: **{start_date}** to **{end_date}**")
    st.sidebar.info(f"📊 Total matching posts: {len(filtered_df)}")

    # 5. Embedded CSS for styling
    css_styles = """
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 0; padding: 5px; }
        .post-card {
            background-color: white;
            padding: 14px;
            border-radius: 6px;
            margin-bottom: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border-left: 5px solid #4A5568; 
        }
        .post-meta {
            font-size: 0.8rem;
            color: #6c757d;
            margin-bottom: 6px;
        }
    </style>
    """

    # 6. Build Unified Feed Window
    st.subheader(f"🔄 Rumor Stream Feed Window")

    html_feed = css_styles
    if not filtered_df.empty:
        for _, row in filtered_df.iterrows():
            html_feed += f"""
            <div class="post-card">
                <div class="post-meta">
                    <span>📅 {row['DATE']}</span>
                </div>
                <div style="font-size: 0.95rem; line-height: 1.4; color: #111;">{row['POST']}</div>
            </div>
            """
    else:
        html_feed += "<p style='color: gray; text-align: center; margin-top: 40px;'>No logs match the selected time window or keyword combination.</p>"

    # Render the window
    components.html(html_feed, height=500, scrolling=True)