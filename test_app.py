from app import app as dash_app


def test_header_present(dash_duo):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element(".chart-title", timeout=10)
    assert dash_duo.find_element(".chart-title").text == "Pink Morsel Sales Over Time"


def test_visualisation_present(dash_duo):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    dash_duo.wait_for_element("#sales-chart .js-plotly-plot", timeout=10)
    assert dash_duo.find_element("#sales-chart").is_displayed()


def test_region_picker_present(dash_duo):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    radios = dash_duo.find_elements("#region-filter input[type='radio']")
    assert len(radios) == 5

