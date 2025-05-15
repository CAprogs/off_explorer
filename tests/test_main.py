"""Testing the simulated Streamlit app to check the correctness of displayed elements and outputs.

This isn't yet available for multipage apps.
See https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest
"""

from streamlit.testing.v1 import AppTest


def test_main() -> None:
    at = AppTest.from_file("app.py")

    # Run the simulated app

    at.run()

    assert not at.exception

    # Number of displayed elements

    assert len(at.title) == 1
    assert len(at.divider) == 1
    assert len(at.dataframe) == 1
    assert len(at.columns) == 12
    assert len(at.markdown) == 1
    assert len(at.text_input) == 1
    assert len(at.button) == 1

    # Inserting an invalid barcode

    at.text_input("user_input").input("some_invalid_barcode").run()
    at.button[0].click().run()
    assert at.warning[0].value == "Barcode must be a 13 length digit value present in the dataset."
    # An image is NOT displayed
    assert at.session_state["image_url"] is None
    # A product details is NOT displayed
    assert len(at.markdown) == 1
    assert at.session_state["product_details"] == {"product_name": "", "brand": "", "quantity": "", "nutriscore": ""}

    # Inserting a valid barcode

    at.text_input("user_input").input("3250390831488").run()
    at.button[0].click().run()
    # An image is displayed
    assert at.session_state["image_url"] is not None
    # A product details is displayed
    assert len(at.markdown) == 5
    assert at.session_state["product_details"] == {
        "product_name": "Craquilles fromage",
        "brand": "Bouton d'or",
        "quantity": "90 g",
        "nutriscore": "e",
    }
