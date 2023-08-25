import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ClientsideFunction
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


app = dash.Dash(
    __name__,
    external_scripts=[
        "https://cdnjs.cloudflare.com/ajax/libs/dragula/3.7.2/dragula.min.js"
    ],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
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
                html.P(f"{data.id}", className="cardID"),
                html.P(f"Type: {data.type}"),
                html.P(f"Stage: {data.stage}"),
                html.P(f"Entry Date: {data.entry_datetime}"),
                # Add more data fields...
            ]
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
