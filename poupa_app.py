import streamlit as st
import app_pages.connexion
from app_pages.experience_view import ExperiencePage
from app_pages.home import HomePage
from app_pages.results_view import ResultPage
from app_pages.projet_view import AddProjectPage
from hydralit import HydraApp
from app_pages.merge_capteurs import MergePage
from app_pages.element_view import FarinePage, LevainPage, LevurePage, BoitierPage
import myloading


test = True
# if "login" in st.session_state and "prenom_nom" in st.session_state:
app = HydraApp(title="PouPâ",
               favicon="resources/bread.png",
               hide_streamlit_markers=True,
               use_navbar=True,
               navbar_sticky=False,
               navbar_animation=True,
               )
app.add_app("Home", icon="🏠", app=HomePage("Accueil"), is_home=True)

app.add_app("Nouvelle Expérience", icon="🥼", app=ExperiencePage("Nouvelle Expérience"))
app.add_app("Résultats", icon="📚", app=ResultPage("Résultats"))
app.add_app("Comparaison de capteurs", icon="🔃", app=MergePage("Comparaison de capteurs"))
app.add_app("Farines", icon="🌾", app=FarinePage("Farines"))
app.add_app("Levains", icon="🦠", app=LevainPage("Levains"))
app.add_app("Levures", app=LevurePage("Levures"))
app.add_app("Boitiers", icon='⚙', app=BoitierPage("Boitiers"))
app.add_app("Projets", icon="🗒️", app=AddProjectPage("Projets"))

app.add_app("Signup", icon="🛰️", app=app_pages.connexion.InscriptionPage("Inscription"), is_unsecure=True)

app.add_app("Login", app=app_pages.connexion.ConnexionPage("Connexion"), is_login=True)

app.add_loader_app(myloading.MyLoadingApp())

user_access_level, username = app.check_access()

if user_access_level > 1:
    menu_data = {
        'Home': ['Accueil'],
        'Nouvelle Expérience': ['Nouvelle Expérience'],
        'Résultats': ['Résultats'],
        'Projets': ["Projets"],
        'Comparaison de capteurs': ['Comparaison de capteurs'],
        'Ajouter éléments': ["Farines", "Levains", "Levures", "Boitiers"], }
else:
    menu_data = {
        'Home': ['Accueil'],
        'Nouvelle Expérience': ['Nouvelle Expérience'],
        'Résultats': ['Résultats'],
        'Comparaison de capteurs': ['Comparaison de capteurs'],
        'Ajouter éléments': ["Farines", "Levains", "Levures"], }

over_theme = {'txc_inactive': '#FFFFFF'}

app.run(menu_data)


@app.logout_callback
def mylogout_callback():
    app.session_state.logged_in = False


@app.login_callback
def mylogin_callback():
    print('i was here')
    app.session_state.logged_in = True
    st.success("Bienvenu !!")
