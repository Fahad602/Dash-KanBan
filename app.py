import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ClientsideFunction, MATCH
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    desc,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
import time

# Define SQLAlchemy base class
Base = declarative_base()


# Define Card model
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    type = Column(String, default="New Ideas")
    stage = Column(String)
    entry_datetime = Column(String, default=datetime.now().strftime("%d/%m/%Y"))
    stock_name = Column(String)
    due_date = Column(String)
    analyst_name = Column(String)
    second_analyst = Column(String)
    Sedol = Column(Integer)
    ISIN = Column(Integer)
    link1 = Column(String)
    link2 = Column(String)
    link3 = Column(String)
    link4 = Column(String)
    link5 = Column(String)
    other = Column(String)
    link1_name = Column(String)
    link2_name = Column(String)
    link3_name = Column(String)
    link4_name = Column(String)
    link5_name = Column(String)
    other_name = Column(String)
    primary_analyst_id = Column(Integer, ForeignKey("analyst.id"))
    secondary_analyst_id = Column(Integer, ForeignKey("analyst.id"))
    active = Column(Integer, default=1)

    # Establish a one-to-many relationship with Log table
    logs = relationship("Log", back_populates="card")


# Define Log model
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey("cards.id"))
    timestamp = Column(DateTime, default=datetime.now)
    old_stage = Column(String)
    new_stage = Column(String)

    # Establish a many-to-one relationship with Card table
    card = relationship("Card", back_populates="logs")


# Define Analyst model
class Analyst(Base):
    __tablename__ = "analyst"

    id = Column(Integer, primary_key=True)
    name = Column(String)


# Connect to SQLite database
engine = create_engine("sqlite:///cards.db", echo=True)

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# Query records for each stage
def get_cards_by_stage(stage):
    return (
        session.query(Card)
        .filter_by(stage=stage, active=1)
        .order_by(desc(Card.id))
        .all()
    )


def get_analysts():
    return session.query(Analyst).all()


app = dash.Dash(
    __name__,
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
)


event = {
    "event": "dropcomplete",
    "props": [
        "detail.sourceContainer",
        "detail.targetContainer",
        "detail.draggedCardID",
    ],
}


def generate_card_body(data):
    card_content = [
        dbc.CardBody(
            [
                html.P(
                    f"{data.id}",
                    className="cardID",
                    style={
                        "display": "none",
                    },
                ),
                html.Div(
                    [
                        html.P(f"{data.stock_name}"),
                        html.I(
                            id={"type": "edit-button", "index": data.id},
                            className="bi bi-pencil edit-icon",
                            n_clicks=0,
                        ),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.Strong("Update Card")),
                                dbc.ModalBody(
                                    dbc.Form(
                                        [
                                            html.Div(
                                                [
                                                    html.Strong("Secondary Analyst"),
                                                    dcc.Dropdown(
                                                        id={
                                                            "type": "secondary_analyst",
                                                            "index": data.id,
                                                        },
                                                        options=[
                                                            {
                                                                "label": analyst.name,
                                                                "value": analyst.id,
                                                            }
                                                            for analyst in get_analysts()
                                                        ],
                                                    ),
                                                ],
                                                style={"padding": "5px"},
                                            ),
                                            html.Div(
                                                [
                                                    html.Strong("Attachments"),
                                                    html.Div(
                                                        [
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link1",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Link 1",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "50%",
                                                                    "marginRight": "5px",
                                                                },
                                                            ),
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link1_name",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Display Name",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "40%",
                                                                },
                                                            ),
                                                        ],
                                                        style={"padding": "3px"},
                                                    ),
                                                    html.Div(
                                                        [
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link2",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Link 2",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "50%",
                                                                    "marginRight": "5px",
                                                                },
                                                            ),
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link2_name",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Display Name",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "40%",
                                                                },
                                                            ),
                                                        ],
                                                        style={"padding": "3px"},
                                                    ),
                                                    html.Div(
                                                        [
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link3",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Link 3",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "50%",
                                                                    "marginRight": "5px",
                                                                },
                                                            ),
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link3_name",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Display Name",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "40%",
                                                                },
                                                            ),
                                                        ],
                                                        style={"padding": "3px"},
                                                    ),
                                                    html.Div(
                                                        [
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link4",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Link 4",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "50%",
                                                                    "marginRight": "5px",
                                                                },
                                                            ),
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link4_name",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Display Name",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "40%",
                                                                },
                                                            ),
                                                        ],
                                                        style={"padding": "3px"},
                                                    ),
                                                    html.Div(
                                                        [
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link5",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Link 5",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "50%",
                                                                    "marginRight": "5px",
                                                                },
                                                            ),
                                                            dbc.Input(
                                                                id={
                                                                    "type": "link5_name",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Display Name",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "40%",
                                                                },
                                                            ),
                                                        ],
                                                        style={"padding": "3px"},
                                                    ),
                                                    html.Div(
                                                        [
                                                            dbc.Input(
                                                                id={
                                                                    "type": "other",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Other",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "50%",
                                                                    "marginRight": "5px",
                                                                },
                                                            ),
                                                            dbc.Input(
                                                                id={
                                                                    "type": "other_name",
                                                                    "index": data.id,
                                                                },
                                                                type="text",
                                                                placeholder="Display Name",
                                                                style={
                                                                    "display": "inline-block",
                                                                    "width": "40%",
                                                                },
                                                            ),
                                                        ],
                                                        style={"padding": "3px"},
                                                    ),
                                                ],
                                                style={"padding": "5px"},
                                            ),
                                        ]
                                    )
                                ),
                                dbc.ModalFooter(
                                    dbc.Button(
                                        "Update",
                                        id={"type": "update-button", "index": data.id},
                                        color="#e6687d",
                                        style={"backgroundColor": "#e6687d"},
                                    ),
                                ),
                            ],
                            id={"type": "update_card_modal", "index": data.id},
                        ),
                    ],
                    style={"display": "flex", "justifyContent": "space-between"},
                ),
                html.P(
                    [html.Strong("Analyst: "), f"{data.analyst_name}"],
                    style={"marginBottom": "0px"},
                ),
                html.P(
                    [html.Strong("C Date: "), f"{data.entry_datetime}"],
                    style={"marginBottom": "0px"},
                ),
                html.P([html.Strong("Sec Analyst: "), f"{data.second_analyst}"]),
                html.P(
                    [
                        html.Button(
                            "Attachments",
                            id={"type": "show-button", "index": data.id},
                            n_clicks=0,
                            style={
                                "background": "transparent",
                                "margin": "2px",
                                "borderRadius": "3px",
                                "border": "1px solid grey",
                            },
                        ),
                    ]
                ),
                html.Div(
                    id={"type": "attachments", "index": data.id},
                    style={"display": "none"},
                    children=[
                        html.P(
                            [
                                html.A(
                                    data.link1_name, href=data.link1, target=data.link1
                                )
                            ]
                        ),
                        html.P(
                            [
                                html.A(
                                    data.link2_name, href=data.link2, target=data.link2
                                )
                            ]
                        ),
                        html.P(
                            [
                                html.A(
                                    data.link3_name, href=data.link3, target=data.link3
                                )
                            ]
                        ),
                        html.P(
                            [
                                html.A(
                                    data.link4_name, href=data.link4, target=data.link4
                                )
                            ]
                        ),
                        html.P(
                            [
                                html.A(
                                    data.link5_name, href=data.link5, target=data.link5
                                )
                            ]
                        ),
                        html.P(
                            [
                                html.A(
                                    data.other_name, href=data.other, target=data.other
                                )
                            ]
                        ),
                    ],
                ),
                html.P(
                    [
                        html.I(
                            id={"type": "delete-button", "index": data.id},
                            className="bi bi-trash-fill edit-icon",
                            n_clicks=0,
                        ),
                        html.P(
                            [
                                html.I(
                                    className="bi bi-clock",
                                    style={"margin": "8px"},
                                ),
                                f"{data.due_date}",
                            ],
                            style={"textAlign": "right", "marginBottom": 0},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "marginBottom": 0,
                    },
                ),
            ],
        ),
    ]
    return card_content


def generate_card(data):
    return dbc.Card(
        generate_card_body(data),
        className="mb-3",
        id={"type": "card_body", "index": data.id},
    )


def serve_dashboard():
    return html.Div(
        id="main",
        style={
            "display": "flex",
            "flexDirection": "column",
            "width": "100%",
            "paddingLeft": "15px",
            "paddingRight": "15px",
        },
        children=[
            html.Label(id="order"),
            html.Div(
                id="header_container",
                className="row",
                style={
                    "display": "flex",
                    "fontWeight": "bold",
                    "color": "white",
                    "height": "32px",
                },
                children=[
                    html.Div(
                        className="col header",
                        style={"justifyContent": "space-between"},
                        children=[
                            html.Span(""),
                            html.Span("Ideas"),
                            html.I(
                                id="open_create_card_modal_button",
                                className="bi bi-plus-circle add-button",
                            ),
                        ],
                    ),
                    html.Div(
                        "Correction of Errors",
                        className="col header",
                    ),
                    html.Div(
                        "Short Note",
                        className="col header",
                    ),
                    html.Div(
                        "Q&A",
                        className="col header",
                    ),
                    html.Div(
                        "Model",
                        className="col header",
                    ),
                    html.Div(
                        "Pre Mortem",
                        className="col header",
                    ),
                    html.Div(
                        "Full Note",
                        className="col header",
                    ),
                    html.Div(
                        "Buy List",
                        className="col header",
                    ),
                    html.Div(
                        "Fail List",
                        className="col header",
                    ),
                ],
            ),
            EventListener(
                html.Div(
                    id="drag_container",
                    className="row",
                    style={"display": "flex", "flexWrap": "nowrap"},
                    children=[
                        html.Div(
                            id="drag_container1",
                            className="col custom-col1",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Ideas")
                            ],
                        ),
                        html.Div(
                            id="drag_container2",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage(
                                    "Correction of Errors Report"
                                )
                            ],
                        ),
                        html.Div(
                            id="drag_container3",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Short Note")
                            ],
                        ),
                        html.Div(
                            id="drag_container4",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Q&A")
                            ],
                        ),
                        html.Div(
                            id="drag_container5",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Model")
                            ],
                        ),
                        html.Div(
                            id="drag_container6",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Pre Mortem")
                            ],
                        ),
                        html.Div(
                            id="drag_container7",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Full Note")
                            ],
                        ),
                        html.Div(
                            id="drag_container8",
                            className="col custom-col8",
                            children=[
                                # generate_card(card_data)
                                # for card_data in get_cards_by_stage("Buy List")
                            ],
                        ),
                        html.Div(
                            id="drag_container9",
                            className="col custom-col9",
                            children=[
                                # generate_card(card_data)
                                # for card_data in get_cards_by_stage("Fail List")
                            ],
                        ),
                    ],
                ),
                events=[event],
                logging=True,
                id="el",
            ),
            create_card_modal,
        ],
    )


create_card_modal = dbc.Modal(
    [
        dbc.ModalHeader(html.Strong("Add New Idea")),
        dbc.ModalBody(
            dbc.Form(
                [
                    html.Div(
                        [
                            html.Strong("Stock Name"),
                            dbc.Input(id="stock_name", type="text"),
                        ],
                        style={"padding": "5px"},
                    ),
                    html.Div(
                        [
                            html.Strong("Due Date"),
                            dcc.DatePickerSingle(
                                id="due_date",
                                display_format="DD/MM/YYYY",
                                date=datetime.now().date().strftime("%d/%m/%Y"),
                                style={"display": "block", "font-size": "16px"},
                            ),
                        ],
                        style={"padding": "5px", "font-size": "0.8rem"},
                    ),
                    html.Div(
                        [
                            html.Strong("Primary Analyst"),
                            dcc.Dropdown(
                                id="primary_analyst",
                                options=[
                                    {"label": analyst.name, "value": analyst.id}
                                    for analyst in get_analysts()
                                ],
                                value=1,
                            ),
                        ],
                        style={"padding": "5px"},
                    ),
                    html.Div(
                        [
                            html.Strong("Secondary Analyst"),
                            dcc.Dropdown(
                                id="secondary_analyst",
                                options=[
                                    {"label": analyst.name, "value": analyst.id}
                                    for analyst in get_analysts()
                                ],
                            ),
                        ],
                        style={"padding": "5px"},
                    ),
                    html.Div(
                        [
                            html.Strong("Attachments"),
                            html.Div(
                                [
                                    dbc.Input(
                                        id="link1",
                                        type="text",
                                        placeholder="Link 1",
                                        style={
                                            "display": "inline-block",
                                            "width": "50%",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    dbc.Input(
                                        id="link1_name",
                                        type="text",
                                        placeholder="Display Name",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                style={"padding": "3px"},
                            ),
                            html.Div(
                                [
                                    dbc.Input(
                                        id="link2",
                                        type="text",
                                        placeholder="Link 2",
                                        style={
                                            "display": "inline-block",
                                            "width": "50%",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    dbc.Input(
                                        id="link2_name",
                                        type="text",
                                        placeholder="Display Name",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                style={"padding": "3px"},
                            ),
                            html.Div(
                                [
                                    dbc.Input(
                                        id="link3",
                                        type="text",
                                        placeholder="Link 3",
                                        style={
                                            "display": "inline-block",
                                            "width": "50%",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    dbc.Input(
                                        id="link3_name",
                                        type="text",
                                        placeholder="Display Name",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                style={"padding": "3px"},
                            ),
                            html.Div(
                                [
                                    dbc.Input(
                                        id="link4",
                                        type="text",
                                        placeholder="Link 4",
                                        style={
                                            "display": "inline-block",
                                            "width": "50%",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    dbc.Input(
                                        id="link4_name",
                                        type="text",
                                        placeholder="Display Name",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                style={"padding": "3px"},
                            ),
                            html.Div(
                                [
                                    dbc.Input(
                                        id="link5",
                                        type="text",
                                        placeholder="Link 5",
                                        style={
                                            "display": "inline-block",
                                            "width": "50%",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    dbc.Input(
                                        id="link5_name",
                                        type="text",
                                        placeholder="Display Name",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                style={"padding": "3px"},
                            ),
                            html.Div(
                                [
                                    dbc.Input(
                                        id="other",
                                        type="text",
                                        placeholder="Other",
                                        style={
                                            "display": "inline-block",
                                            "width": "50%",
                                            "marginRight": "5px",
                                        },
                                    ),
                                    dbc.Input(
                                        id="other_name",
                                        type="text",
                                        placeholder="Display Name",
                                        style={
                                            "display": "inline-block",
                                            "width": "40%",
                                        },
                                    ),
                                ],
                                style={"padding": "3px"},
                            ),
                        ],
                        style={"padding": "5px"},
                    ),
                ]
            )
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Add",
                id="create_card_button",
                color="#e6687d",
                style={"backgroundColor": "#e6687d"},
            ),
        ),
    ],
    id="create_card_modal",
)


app.layout = serve_dashboard

app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="make_draggable"),
    Output("drag_container", "data-drag"),
    [
        Input("drag_container1", "id"),
        Input("drag_container2", "id"),
        Input("drag_container3", "id"),
        Input("drag_container4", "id"),
        Input("drag_container5", "id"),
        Input("drag_container6", "id"),
        Input("drag_container7", "id"),
        Input("drag_container8", "id"),
        Input("drag_container9", "id"),
    ],
    [State("drag_container", "children")],
)


# @app.callback(
#     Output({"type": "hidden_div", "index": MATCH}, "children"),
#     Input({"type": "delete-button", "index": MATCH}, "n_clicks"),
#     prevent_initial_call=True,
# )
# def open_delete_card(
#     delete_n_clicks,
# ):
#     breakpoint()
#     if delete_n_clicks:
#         card_id = json.loads(
#             dash.callback_context.triggered[0]["prop_id"].split(".")[0]
#         )["index"]
#         card = session.query(Card).filter_by(id=card_id).first()
#         card.active = 0
#         session.commit()
#         return


@app.callback(
    Output({"type": "update_card_modal", "index": MATCH}, "is_open"),
    Output({"type": "secondary_analyst", "index": MATCH}, "value"),
    Output({"type": "link1", "index": MATCH}, "value"),
    Output({"type": "link1_name", "index": MATCH}, "value"),
    Output({"type": "link2", "index": MATCH}, "value"),
    Output({"type": "link2_name", "index": MATCH}, "value"),
    Output({"type": "link3", "index": MATCH}, "value"),
    Output({"type": "link3_name", "index": MATCH}, "value"),
    Output({"type": "link4", "index": MATCH}, "value"),
    Output({"type": "link4_name", "index": MATCH}, "value"),
    Output({"type": "link5", "index": MATCH}, "value"),
    Output({"type": "link5_name", "index": MATCH}, "value"),
    Output({"type": "other", "index": MATCH}, "value"),
    Output({"type": "other_name", "index": MATCH}, "value"),
    Output({"type": "edit-button", "index": MATCH}, "n_clicks"),
    Output({"type": "update-button", "index": MATCH}, "n_clicks"),
    Output({"type": "delete-button", "index": MATCH}, "n_clicks"),
    Output({"type": "card_body", "index": MATCH}, "children"),
    Output({"type": "card_body", "index": MATCH}, "style"),
    Input({"type": "edit-button", "index": MATCH}, "n_clicks"),
    Input({"type": "update-button", "index": MATCH}, "n_clicks"),
    Input({"type": "delete-button", "index": MATCH}, "n_clicks"),
    State({"type": "secondary_analyst", "index": MATCH}, "value"),
    State({"type": "link1", "index": MATCH}, "value"),
    State({"type": "link1_name", "index": MATCH}, "value"),
    State({"type": "link2", "index": MATCH}, "value"),
    State({"type": "link2_name", "index": MATCH}, "value"),
    State({"type": "link3", "index": MATCH}, "value"),
    State({"type": "link3_name", "index": MATCH}, "value"),
    State({"type": "link4", "index": MATCH}, "value"),
    State({"type": "link4_name", "index": MATCH}, "value"),
    State({"type": "link5", "index": MATCH}, "value"),
    State({"type": "link5_name", "index": MATCH}, "value"),
    State({"type": "other", "index": MATCH}, "value"),
    State({"type": "other_name", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def open_update_card_modal(
    edit_n_clicks,
    update_n_clicks,
    delete_n_clicks,
    secondary_analyst,
    link1,
    link1_name,
    link2,
    link2_name,
    link3,
    link3_name,
    link4,
    link4_name,
    link5,
    link5_name,
    other,
    other_name,
):
    if edit_n_clicks:
        card_id = json.loads(
            dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        )["index"]
        card = session.query(Card).filter_by(id=card_id).first()

        return (
            True,
            card.secondary_analyst_id,
            card.link1,
            card.link1_name,
            card.link2,
            card.link2_name,
            card.link3,
            card.link3_name,
            card.link4,
            card.link4_name,
            card.link5,
            card.link5_name,
            card.other,
            card.other_name,
            0,
            0,
            0,
            dash.no_update,
            dash.no_update,
        )
    if update_n_clicks:
        card_id = json.loads(
            dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        )["index"]
        card = session.query(Card).filter_by(id=card_id).first()
        s_analyst = session.query(Analyst).filter_by(id=secondary_analyst).first()

        card.secondary_analyst_id = secondary_analyst
        card.second_analyst = s_analyst.name
        card.link1 = link1
        card.link1_name = link1_name
        card.link2 = link2
        card.link2_name = link2_name
        card.link3 = link3
        card.link3_name = link3_name
        card.link4 = link4
        card.link4_name = link4_name
        card.link5 = link5
        card.link5_name = link5_name
        card.other = other
        card.other_name = other_name
        session.commit()

        return (
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0,
            0,
            0,
            generate_card_body(card),
            dash.no_update,
        )
    if delete_n_clicks:
        card_id = json.loads(
            dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        )["index"]
        card = session.query(Card).filter_by(id=card_id).first()
        card.active = 0
        session.commit()
        style = {"display": "none"}
        return (
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            0,
            0,
            0,
            dash.no_update,
            style
        )
    return (
        False,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        0,
        0,
        0,
        dash.no_update,
        dash.no_update,
    )


@app.callback(
    Output("create_card_modal", "is_open"),
    Output("drag_container1", "children"),
    Output("open_create_card_modal_button", "n_clicks"),
    [
        Input("create_card_button", "n_clicks"),
        Input("open_create_card_modal_button", "n_clicks"),
    ],
    [
        State("stock_name", "value"),
        State("due_date", "date"),
        State("primary_analyst", "value"),
        State("secondary_analyst", "value"),
        State("link1", "value"),
        State("link1_name", "value"),
        State("link2", "value"),
        State("link2_name", "value"),
        State("link3", "value"),
        State("link3_name", "value"),
        State("link4", "value"),
        State("link4_name", "value"),
        State("link5", "value"),
        State("link5_name", "value"),
        State("other", "value"),
        State("other_name", "value"),
        State("drag_container1", "children"),
    ],
    prevent_initial_call=True,
)
def add_new_card(
    n_clicks,
    open_modal_n_clicks,
    stock_name,
    due_date,
    primary_analyst,
    secondary_analyst,
    link1,
    link1_name,
    link2,
    link2_name,
    link3,
    link3_name,
    link4,
    link4_name,
    link5,
    link5_name,
    other,
    other_name,
    drag_container1_children,
):
    if open_modal_n_clicks:
        return True, drag_container1_children, 0

    if n_clicks:
        if not stock_name:
            return PreventUpdate, drag_container1_children, 0

        p_analyst = session.query(Analyst).filter_by(id=primary_analyst).first()
        s_analyst = session.query(Analyst).filter_by(id=secondary_analyst).first()
        new_card = Card(
            stage="Ideas",
            stock_name=stock_name,
            due_date=due_date,
            primary_analyst_id=primary_analyst,
            secondary_analyst_id=secondary_analyst,
            analyst_name=p_analyst.name,
            Sedol=int(time.time() * 1001) % 100000000,
            ISIN=int(time.time() * 1000) % 100000000,
            link1=link1,
            link2=link2,
            link3=link3,
            link4=link4,
            link5=link5,
            other=other,
            link1_name=link1_name,
            link2_name=link2_name,
            link3_name=link3_name,
            link4_name=link4_name,
            link5_name=link5_name,
            other_name=other_name,
        )
        if s_analyst:
            new_card.second_analyst = s_analyst.name
        session.add(new_card)
        session.commit()

        updated_children = [generate_card(new_card)] + drag_container1_children
        return False, updated_children, 0

    return False, drag_container1_children, 0


# Callback to toggle attachments visibility
@app.callback(
    Output({"type": "attachments", "index": MATCH}, "style"),
    Input({"type": "show-button", "index": MATCH}, "n_clicks"),
    prevent_initial_call=True,
)
def toggle_attachments(n_clicks):
    if n_clicks % 2 == 1:
        return {"display": "block"}  # Show attachments container
    else:
        return {"display": "none"}  # Hide attachments container


@app.callback(
    Output("order", "children"),
    [Input("el", "n_events"), State("el", "event")],
)
def update_card(nevents, event_data):
    if event_data:
        if event_data["detail.sourceContainer"] != event_data["detail.targetContainer"]:
            card = (
                session.query(Card)
                .filter_by(id=event_data["detail.draggedCardID"])
                .first()
            )
            log = Log(card_id=card.id, old_stage=card.stage)
            if event_data["detail.targetContainer"] == "drag_container1":
                card.stage = "Ideas"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container2":
                card.stage = "Correction of Errors Report"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container3":
                card.stage = "Short Note"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container4":
                card.stage = "Q&A"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container5":
                card.stage = "Model"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container6":
                card.stage = "Pre Mortem"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container7":
                card.stage = "Full Note"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container8":
                card.stage = "Buy List"
                log.new_stage = card.stage
            elif event_data["detail.targetContainer"] == "drag_container9":
                card.stage = "Fail List"
                log.new_stage = card.stage
            session.add(log)
            session.commit()
    return ""


if __name__ == "__main__":
    app.run_server(debug=True)
