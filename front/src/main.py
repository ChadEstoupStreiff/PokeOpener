import requests
import streamlit as st


def page1():
    if st.button("Open a card", use_container_width=True):
        result = requests.get(
            f"http://pokeopener_back:80/cards/draw?token={st.session_state.token}",
        ).json()
        st.session_state.last_card = result
    if "last_card" in st.session_state:
        card = st.session_state.last_card
        st.text(f"You got: {card['name']}")
        st.image(card["images"]["large"])

def page2():
    c1, c2 = st.columns(2)
    with c1:
        st.title(f"Inventory of {st.session_state.full_name}")
    with c2:
        n_cols = st.slider("Number of columns", 4, 15, 6)

    cards_id = requests.get(
        f"http://pokeopener_back:80/cards/inventory?token={st.session_state.token}",
    ).json()
    st.text(f"You have: {len(cards_id)} cards")

    cols = st.columns(n_cols)
    for i, card in enumerate(sorted(cards_id, key=lambda card: not card["faved"])):
        card_info = requests.get(
            f"http://pokeopener_back:80/cards/get?card_id={card['card_id']}",
        ).json()
        with cols[i % n_cols]:
            st.image(card_info["images"]["small"])
            if card["faved"]:
                st.markdown("⭐ **Favorite**")
            else:
                st.markdown(" ")
            if st.button("❤️", key=f"fav_{card['id']}", use_container_width=True):
                requests.post(
                    f"http://pokeopener_back:80/cards/fav?token={st.session_state.token}&id={card['id']}"
                )
                st.rerun()

def page3():
    c1, c2 = st.columns(2)
    with c1:
        st.title(f"Favorited cards of {st.session_state.full_name}")
    with c2:
        n_cols = st.slider("Number of columns", 4, 15, 6)

    cards_id = requests.get(
        f"http://pokeopener_back:80/cards/getFav?token={st.session_state.token}",
    ).json()
    st.text(f"You have: {len(cards_id)} favorited cards")

    cols = st.columns(n_cols)
    for i, card in enumerate(cards_id):
        card_info = requests.get(
            f"http://pokeopener_back:80/cards/get?card_id={card['card_id']}",
        ).json()
        with cols[i % n_cols]:
            st.image(card_info["images"]["small"])
            if st.button("unfav", key=f"fav_{card['id']}"):
                requests.post(
                    f"http://pokeopener_back:80/cards/fav?token={st.session_state.token}&id={card['id']}"
                )
                st.rerun()

def try_login(email, password):
    with st.spinner("Logging in..."):
        try:
            result = requests.post(
                f"http://pokeopener_back:80/auth/login?email={email}&password={password}",
            ).json()
            if "access_token" not in result:
                raise Exception()
            st.session_state.token = result["access_token"]
            st.session_state.full_name = result["user"]["full_name"]
            st.session_state.logged = True
            st.rerun()
        except Exception as _:
            st.error("Can't connect")


def disconnect():
    st.session_state.logged = False
    st.session_state.pop("token", None)
    st.session_state.pop("full_name", None)
    st.rerun()


st.set_page_config(page_title="PokeOpener", page_icon="🔥", layout="wide")

if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    c1, c2 = st.columns(2)
    with c1:
        st.text("Login")
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", key="password", type="password")
        if st.button("Login", use_container_width=True):
            try_login(email, password)
    with c2:
        st.text("Register")
        email = st.text_input("Email", key="email_register")
        password = st.text_input("Password", key="password_register", type="password")
        full_name = st.text_input("Full Name", key="full_name_register")
        if st.button("Register", use_container_width=True):
            try:
                with st.spinner("Registering..."):
                    result = requests.post(
                        f"http://pokeopener_back:80/auth/register?email={email}&password={password}&full_name={full_name}",
                    ).json()
                    if (
                        "message" not in result
                        or result["message"] != "User registered successfully"
                    ):
                        raise Exception()
                    try_login(email, password)
            except Exception as _:
                st.error("Can't register")

else:
    pg = st.navigation(
        [
            st.Page(page1, title="Card opening", icon="🔥"),
            st.Page(page2, title="Inventory", icon="💼"),
            st.Page(page3, title="Favorites", icon="💖"),
            # st.Page(disconnect, title="Disconnect", icon="🚪"),
        ]
    )
    pg.run()
