"""Python script to display images from the Open Food Facts Project in a Streamlit app."""

import streamlit as st


def main() -> None:
    """Application entry point."""
    st.set_page_config(page_title="Food Search", page_icon=":stuffed_flatbread:", layout="wide")

    from off_streamlit_app.utils import fetch_data, fetch_nutricore_color, find_image_by_barcode

    if "product_details" not in st.session_state:
        st.session_state["product_details"] = {"product_name": "", "brand": "", "quantity": "", "nutriscore": ""}
    if "image_url" not in st.session_state:
        st.session_state["image_url"] = None

    _, top_middle, _ = st.columns([1.2, 2, 1])

    with top_middle:
        st.title(":green[Open Food Facts Explorer] :material/nutrition:", anchor=False)
        _, info_col, _ = st.columns([1.5, 8, 1.5], vertical_alignment="center")
        with info_col:
            st.markdown("Find **french** food informations using barcodes")
        st.divider()

    with st.container():
        st.dataframe(fetch_data(), use_container_width=True, hide_index=False)

    left_bottom, right_bottom = st.columns([3, 2])

    with right_bottom:
        left_column, right_column = st.columns([3, 2], vertical_alignment="bottom")
        left_column.text_input(
            label="Barcode SearchBar",
            placeholder="Insert a barcode",
            max_chars=13,
            label_visibility="hidden",
            key="user_input",
        )
        if right_column.button("Search Product", icon=":material/manage_search:"):
            st.session_state["image_url"], st.session_state["product_details"] = find_image_by_barcode(
                st.session_state.get("user_input")
            )

    with left_bottom:
        left_column, right_column = st.columns([3, 2])
        if st.session_state.get("image_url"):
            left_column.image(
                image=st.session_state["image_url"], caption=st.session_state["product_details"]["product_name"]
            )
            right_column.markdown(f"Product:  **{st.session_state['product_details']['product_name']}**")
            right_column.markdown(f"Brand:  **{st.session_state['product_details']['brand']}**")
            right_column.markdown(f"Quantity:  **{st.session_state['product_details']['quantity']}**")
            nutriscore = st.session_state["product_details"]["nutriscore"]
            color = fetch_nutricore_color(nutriscore)
            right_column.markdown(
                f'<span style="color:{color}; font-size:48px; font-weight:bold;">{nutriscore.upper()}</span>',
                unsafe_allow_html=True,
            )
