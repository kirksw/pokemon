import pandas as pd
import streamlit as st
from dataclasses import dataclass, field

st.set_page_config(page_title="Pokédex", layout="wide")


@dataclass
class Pokemon:
    """Object representing a pokemon"""

    id: int
    name: str
    base_experience: int
    weight: int
    height: int
    order: int
    sprite: str
    type_slot_1: str
    type_slot_2: str
    bmi: str
    games: list[str] = field(default_factory=list)


@st.cache()
def load_data(data_path: str) -> pd.DataFrame:
    return pd.read_parquet(data_path)


def get_pokemon_label(pokemon_id: int) -> str:
    """get label of pokemon"""
    pokemon = Pokemon(
        **pokemon_data.loc[pokemon_data["id"] == pokemon_id, :].to_dict("records")[0]
    )
    return f"#{pokemon.id:03} - {pokemon.name}"


pokemon_data = load_data("data/str/pokemon")


# filter panel
filter_form = st.sidebar.form(key="Selector")
filter_form.header("Selector")
pokemon_selection = filter_form.selectbox(
    label="Name",
    options=pokemon_data["id"].sort_values(),
    format_func=get_pokemon_label,
)
select_submit = filter_form.form_submit_button("Submit")


def render_main(pokemon_id: int):
    """Render main panel for the specified pokemon"""
    pokemon_dict = pokemon_data.loc[pokemon_data["id"] == pokemon_id, :].to_dict(
        "records"
    )[0]
    pokemon = Pokemon(**pokemon_dict)

    st.title(f"{pokemon.name} #{pokemon.id:03}")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            pokemon.sprite,
            width=200,
        )

    with col2:
        st.text(f"Games: {', '.join(pokemon.games)}")
        st.text(f"Base experience: {pokemon.base_experience}")
        st.text(f"Order: {pokemon.order}")
        st.text(f"Weight: {pokemon.weight}")
        st.text(f"Height: {pokemon.height}")
        st.text(f"BMI: {pokemon.bmi:0.2f}")
        st.text(f"Type 1: {pokemon.type_slot_1}")
        if pokemon.type_slot_2:
            st.text(f"Type 2: {pokemon.type_slot_2}")


if select_submit:
    render_main(pokemon_id=pokemon_selection)
else:
    render_main(pokemon_id=1)
