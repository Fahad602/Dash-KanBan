import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ClientsideFunction, MATCH
from dash_extensions import EventListener

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

# Define SQLAlchemy base class
Base = declarative_base()


# Define Card model
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    type = Column(String, default="New Ideas")
    stage = Column(String)
    entry_datetime = Column(String, default=datetime.now)
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
    primary_analyst_id = Column(Integer, ForeignKey("analyst.id"))
    secondary_analyst_id = Column(Integer, ForeignKey("analyst.id"))

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


# Define Log model
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
    return session.query(Card).filter_by(stage=stage).all()


def get_analysts():
    return session.query(Analyst).all()


# Query all records
def get_all_cards():
    return session.query(Card).all()


app = dash.Dash(
    __name__,
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
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


def generate_card(data):
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
                html.P(f"{data.stock_name}"),
                html.Br(),
                html.P([html.Strong("Analyst: "), html.Span(f"{data.analyst_name}")]),
                html.P([html.Strong("C Date: "), html.Span(f"{data.entry_datetime}")]),
                html.P(
                    [
                        html.Strong("Secondary Analyst: "),
                        dcc.Dropdown(
                            id={"type": "secondary-analyst-dropdown", "index": data.id},
                            options=[
                                {"label": analyst.name, "value": analyst.id}
                                for analyst in get_analysts()
                            ],
                            value=data.secondary_analyst_id,
                        ),
                    ]
                ),
                html.P(
                    [
                        html.Button(
                            "Attachments",
                            id={"type": "show-button", "index": data.id},
                            n_clicks=0,
                            style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                        ),
                    ]
                ),
                html.Div(
                    id={"type": "attachments", "index": data.id},
                    style={"display": "none"},
                    children=[
                        html.P([html.A(data.link1, href=data.link1, target=data.link1)])
                        if data.link1
                        else html.Div(
                            id={"type": "link-container", "index": data.id, "attachment-type": "link1"},
                            children=[
                                dcc.Input(
                                    id={"type": "new-link-input", "index": data.id, "attachment-type": "link1"},
                                    type="text",
                                    placeholder="Link 1",
                                    style={"width": "69%", "display": "inline", "margin": '2px', "borderRadius": '3px', "border": 0},
                                ),
                                html.Button(
                                    "Save",
                                    id={"type": "save-link-button", "index": data.id, "attachment-type": "link1"},
                                    style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                                ),
                            ]
                        ),
                        html.P([html.A(data.link2, href=data.link2, target=data.link2)])
                        if data.link2
                        else html.Div(
                            id={"type": "link-container", "index": data.id, "attachment-type": "link2"},
                            children=[
                                dcc.Input(
                                    id={"type": "new-link-input", "index": data.id, "attachment-type": "link2"},
                                    type="text",
                                    placeholder="Link 2",
                                    style={"width": "69%", "display": "inline", "margin": '2px', "borderRadius": '3px', "border": 0},
                                ),
                                html.Button(
                                    "Save",
                                    id={"type": "save-link-button", "index": data.id, "attachment-type": "link2"},
                                    style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                                ),
                            ]
                        ),
                        html.P([html.A(data.link3, href=data.link3, target=data.link3)])
                        if data.link3
                        else html.Div(
                            id={"type": "link-container", "index": data.id, "attachment-type": "link3"},
                            children=[
                                dcc.Input(
                                    id={"type": "new-link-input", "index": data.id, "attachment-type": "link3"},
                                    type="text",
                                    placeholder="Link 3",
                                    style={"width": "69%", "display": "inline", "margin": '2px', "borderRadius": '3px', "border": 0},
                                ),
                                html.Button(
                                    "Save",
                                    id={"type": "save-link-button", "index": data.id, "attachment-type": "link3"},
                                    style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                                ),
                            ]
                        ),
                        html.P([html.A(data.link4, href=data.link4, target=data.link4)])
                        if data.link4
                        else html.Div(
                            id={"type": "link-container", "index": data.id, "attachment-type": "link4"},
                            children=[
                                dcc.Input(
                                    id={"type": "new-link-input", "index": data.id, "attachment-type": "link4"},
                                    type="text",
                                    placeholder="Link 4",
                                    style={"width": "69%", "display": "inline", "margin": '2px', "borderRadius": '3px', "border": 0},
                                ),
                                html.Button(
                                    "Save",
                                    id={"type": "save-link-button", "index": data.id, "attachment-type": "link4"},
                                    style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                                ),
                            ]
                        ),
                        html.P([html.A(data.link5, href=data.link5, target=data.link5)])
                        if data.link5
                        else html.Div(
                            id={"type": "link-container", "index": data.id, "attachment-type": "link5"},
                            children=[
                                dcc.Input(
                                    id={"type": "new-link-input", "index": data.id, "attachment-type": "link5"},
                                    type="text",
                                    placeholder="Link 5",
                                    style={"width": "69%", "display": "inline", "margin": '2px', "borderRadius": '3px', "border": 0},
                                ),
                                html.Button(
                                    "Save",
                                    id={"type": "save-link-button", "index": data.id, "attachment-type": "link5"},
                                    style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                                ),
                            ]
                        ),
                        html.P([html.A(data.other, href=data.other, target=data.other)])
                        if data.other
                        else html.Div(
                            id={"type": "link-container", "index": data.id, "attachment-type": "other"},
                            children=[
                                dcc.Input(
                                    id={"type": "new-link-input", "index": data.id, "attachment-type": "other"},
                                    type="text",
                                    placeholder="Other",
                                    style={"width": "69%", "display": "inline", "margin": '2px', "borderRadius": '3px', "border": 0},
                                ),
                                html.Button(
                                    "Save",
                                    id={"type": "save-link-button", "index": data.id, "attachment-type": "other"},
                                    style={"background": "transparent", "margin": '2px', "borderRadius": '3px', "border": "1px solid grey"},
                                ),
                            ]
                        ),
                    ],
                ),
                html.Br(),
                html.P(
                    f"Due {data.due_date}",
                    style={"textAlign": "right", "marginBottom": 0},
                ),
            ],
        ),
    ]
    return dbc.Card(card_content, className="mb-3")


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
                        "Ideas",
                        className="col header",
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
                            className="col custom-col",
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
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Buy List")
                            ],
                        ),
                        html.Div(
                            id="drag_container9",
                            className="col custom-col",
                            children=[
                                generate_card(card_data)
                                for card_data in get_cards_by_stage("Fail List")
                            ],
                        ),
                    ],
                ),
                events=[event],
                logging=True,
                id="el",
            ),
        ],
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


# Callback to save attachment link
@app.callback(
    Output({"type": "link-container", "index": MATCH, "attachment-type": MATCH}, "children"),
    Input({"type": "save-link-button", "index": MATCH, "attachment-type": MATCH}, "n_clicks"),
    State({"type": "new-link-input", "index": MATCH, "attachment-type": MATCH}, "value"),
    prevent_initial_call=True,
)
def save_attachment_link(n_clicks, new_link, **kwargs):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    button_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])
    card_id = button_id["index"]
    attachment_type = button_id["attachment-type"]

    if new_link:
        card = session.query(Card).get(card_id)
        setattr(card, attachment_type, new_link)
        session.commit()
        return html.P([html.A(new_link, href=new_link, target=new_link)])
    
    return dash.no_update


@app.callback(
    Output({"type": "secondary-analyst-dropdown", "index": MATCH}, "value"),
    Input({"type": "secondary-analyst-dropdown", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def update_secondary_analyst(selected_analyst_id):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    if selected_analyst_id:
        card_id = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
        card = session.query(Card).get(card_id)
        card.secondary_analyst_id = selected_analyst_id
        selected_analyst = session.query(Analyst).get(selected_analyst_id)
        card.second_analyst = selected_analyst.name
        session.commit()

        return selected_analyst_id
    return dash.no_update


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
        print(event_data)

        if event_data["detail.sourceContainer"] != event_data["detail.targetContainer"]:
            card = (
                session.query(Card)
                .filter_by(id=event_data["detail.draggedCardID"])
                .first()
            )
            if event_data["detail.targetContainer"] == "drag_container1":
                card.stage = "Ideas"
            elif event_data["detail.targetContainer"] == "drag_container2":
                card.stage = "Correction of Errors Report"
            elif event_data["detail.targetContainer"] == "drag_container3":
                card.stage = "Short Note"
            elif event_data["detail.targetContainer"] == "drag_container4":
                card.stage = "Q&A"
            elif event_data["detail.targetContainer"] == "drag_container5":
                card.stage = "Model"
            elif event_data["detail.targetContainer"] == "drag_container6":
                card.stage = "Pre Mortem"
            elif event_data["detail.targetContainer"] == "drag_container7":
                card.stage = "Full Note"
            elif event_data["detail.targetContainer"] == "drag_container8":
                card.stage = "Buy List"
            elif event_data["detail.targetContainer"] == "drag_container9":
                card.stage = "Fail List"
            session.commit()

    return ""


if __name__ == "__main__":
    app.run_server(debug=True)
