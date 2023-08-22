import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ClientsideFunction


app = dash.Dash(
    __name__,
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

# Sample data for each card
data = [
    {
        "type": "new_ideas",
        "stage": "ideas",
        "entry_datetime": "01/06/2023",
        "stock_name": "APPLE INC",
        "due_date": "27/07/2023",
        "analyst_name": "Joe Smith",
        "second_analyst": "Jarn Gore",
        "Sedol": 81564326,
        "ISIN": 29817364,
        "link1": "https://attachment_link",
        "link2": "https://attachment_link",
        "link3": False,
        "link4": "https://attachment_link",
        "link5": False,
        "other": False,
    },
    {
        "type": "new_ideas",
        "stage": "ideas",
        "entry_datetime": "01/06/2023",
        "stock_name": "APPLE INC",
        "due_date": "27/07/2023",
        "analyst_name": "Joe Smith",
        "second_analyst": "Jarn Gore",
        "Sedol": 81564326,
        "ISIN": 29817364,
        "link1": "https://attachment_link",
        "link2": "https://attachment_link",
        "link3": False,
        "link4": "https://attachment_link",
        "link5": False,
        "other": False,
    },
    {
        "type": "new_ideas",
        "stage": "ideas",
        "entry_datetime": "01/06/2023",
        "stock_name": "APPLE INC",
        "due_date": "27/07/2023",
        "analyst_name": "Joe Smith",
        "second_analyst": "Jarn Gore",
        "Sedol": 81564326,
        "ISIN": 29817364,
        "link1": "https://attachment_link",
        "link2": "https://attachment_link",
        "link3": False,
        "link4": "https://attachment_link",
        "link5": False,
        "other": False,
    },
    {
        "type": "new_ideas",
        "stage": "ideas",
        "entry_datetime": "01/06/2023",
        "stock_name": "APPLE INC",
        "due_date": "27/07/2023",
        "analyst_name": "Joe Smith",
        "second_analyst": "Jarn Gore",
        "Sedol": 81564326,
        "ISIN": 29817364,
        "link1": "https://attachment_link",
        "link2": "https://attachment_link",
        "link3": False,
        "link4": "https://attachment_link",
        "link5": False,
        "other": False,
    },
    {
        "type": "new_ideas",
        "stage": "ideas",
        "entry_datetime": "01/06/2023",
        "stock_name": "APPLE INC",
        "due_date": "27/07/2023",
        "analyst_name": "Joe Smith",
        "second_analyst": "Jarn Gore",
        "Sedol": 81564326,
        "ISIN": 29817364,
        "link1": "https://attachment_link",
        "link2": "https://attachment_link",
        "link3": False,
        "link4": "https://attachment_link",
        "link5": False,
        "other": False,
    },
    # Add more data rows...
]

def generate_card(data):
    card_content = [
        dbc.CardHeader(f"Card {data['Sedol']}"),
        dbc.CardBody(
            [
                html.P(f"Type: {data['type']}"),
                html.P(f"Stage: {data['stage']}"),
                html.P(f"Entry Date: {data['entry_datetime']}"),
                # Add more data fields...
            ]
        ),
    ]
    return dbc.Card(card_content, className="mb-3")

app.layout = html.Div(
    id="main",
    children=[
        html.Div(
            id="drag_container",
            className="row",
            children=[
                html.Div(
                    id="drag_container1",
                    className="col",
                    style={"border": "1px solid #ccc", "padding": "10px"},
                    children=[
                        # html.Div(
                        #     className="create-card-form",
                        #     children=[
                        #         dbc.Card(
                        #             [
                        #                 dbc.CardHeader([
                        #                     dcc.Input(id="card-type", placeholder="Type")
                        #                 ]),
                        #                 dbc.CardBody([
                        #                     dcc.Input(id="card-type", placeholder="Type"),
                        #                     dcc.Input(id="card-stage", placeholder="Stage"),
                        #                     # Add more input fields for other card data
                        #                     dbc.Button("Create Card", id="create-card-button", color="primary"),
                        #                 ]),
                        #             ]
                        #         ),
                        #     ],
                        # ),
                        *[generate_card(card_data) for card_data in data]
                    ],
                ),
                html.Div(
                    id="drag_container2",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container3",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container4",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container5",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container6",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container7",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container8",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
                html.Div(
                    id="drag_container9",
                    className="col",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 1"),
                                dbc.CardBody("Some content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 2"),
                                dbc.CardBody("Some other content"),
                            ]
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader("Card 3"),
                                dbc.CardBody("Some more content"),
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ],
)

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container", "data-drag"),
    [Input("drag_container1", "id"),Input("drag_container2", "id"),Input("drag_container3", "id"),Input("drag_container4", "id"),Input("drag_container5", "id"),Input("drag_container6", "id"),Input("drag_container7", "id"),Input("drag_container8", "id"),Input("drag_container9", "id")],
)

if __name__ == "__main__":
    app.run_server(debug=True)
