import models
from models import *
from app_pages.element_view import FarinePage, LevainPage, LevurePage, BoitierPage
from hydralit import HydraHeadApp
from datetime import date

test = True


class ExperiencePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        with open("css/experience.css", "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        st.header("Créer une experience")
        st.write(f"Bienvenue sur la page de création d'experience ! Personnalisez votre experience à votre guise et "
                 f"appuyez sur **'Lancer'** pour générer les résultats. Rendez-vous ensuite sur la page **'Résultats'**"
                 f" pour les consulter ")

        value_poupa = 1
        value_date = date.today()
        value_lieu = ""
        value_operateur = ""
        if "dic_previous" in st.session_state:
            dp = st.session_state["dic_previous"]
            value_date = dp["Date"]
            value_lieu = dp["Lieu"]
            value_operateur = dp["Operateur"]

        with st.sidebar:
            with st.expander("Ajouter une Farine"):
                FarinePage.generate_form(self.session_state.allow_access)
            with st.expander("Ajouter un Levain"):
                LevainPage.generate_form(self.session_state.allow_access)
            with st.expander("Ajouter une Levure"):
                LevurePage.generate_form(self.session_state.allow_access)
            if self.session_state.allow_access > 1:
                with st.expander("Ajouter Boitier"):
                    BoitierPage.generate_form()

        with st.form("form experience"):
            st.subheader("Informations de l'experience")
            if self.session_state.allow_access > 1:
                list_of_projets = Projet.get_projects_from_participant(st.session_state['login'])
                dict_projet = {'---': '---'}
                for projet in list_of_projets:
                    dict_projet[projet.id_projet] = projet.str_form()
                selectprojet = st.selectbox("Projet", list(dict_projet.items()), format_func=lambda o: o[1])

                list_of_boitiers = models.Boitier.get_boitiers()
                dict_boitiers = {}
                for boitier in list_of_boitiers:
                    dict_boitiers[boitier.id] = str(boitier)
                boitier_selected = st.selectbox("Numéro du PouPa utilisé*", list(dict_boitiers.items()),
                                                format_func=lambda o: o[1])
            else:
                boitier_selected = st.number_input("Numéro du PouPa utilisé*", max_value=999, min_value=1,
                                                   value=int(value_poupa))

            upload_file = st.file_uploader("Fichier de données*", type=["csv", "TXT"])
            input_date = st.date_input("Date de l'experience*", value=value_date)
            input_lieu = st.text_input("Lieu de l'experience*", value=value_lieu)
            if "login" in st.session_state:
                input_operateur = st.session_state['login']
                st.warning(f"Opérateur/trice : {st.session_state['login']}")
            else:
                input_operateur = st.text_input("Operateur/trice de l'experience*", value=value_operateur)

            st.subheader("Capteurs")
            tab_titre_cpt = []
            tab_cpt = []

            dic_previous = {"Date": input_date,
                            "Lieu": input_lieu,
                            "Operateur": input_operateur}
            st.session_state["dic_previous"] = dic_previous
            # Récupération des données des farines, levains et levures et création de dictionnaire pour les
            # selectbox
            # Farines
            list_of_farines = []
            # Si on est connecté on récupère la farine de la base de donnée
            if self.session_state.allow_access > 1:
                list_of_farines = models.Farine.get_farines()
            # Si farines est dans st.session_state alors on est mode visiteur
            if "farines" in st.session_state:
                list_of_farines = st.session_state["farines"]
            # valeurs par défauts et pour un choix nul
            dict_farines = {"---": "---"}
            for farine in list_of_farines:
                # Si on est connecté alors l'index est l'identifiant
                if self.session_state.allow_access > 1:
                    dict_farines[farine.id_farine] = farine.str_form()
                # Si on est en mode visiteur l'index est l'objet Farine
                else:
                    dict_farines[farine] = farine.str_form()

            # Levains
            list_of_levains = []
            if self.session_state.allow_access > 1:
                list_of_levains = models.Levain.get_levains()
            if "levains" in st.session_state:
                list_of_levains = st.session_state["levains"]
            dict_levains = {"---": "---"}
            for levain in list_of_levains:
                if self.session_state.allow_access > 1:
                    dict_levains[levain.id] = levain.str_form()
                else:
                    dict_levains[levain] = levain.str_form()

            # Levures
            list_of_levures = []
            if self.session_state.allow_access > 1:
                list_of_levures = models.Levure.get_levures()
            if "levures" in st.session_state:
                list_of_levures = st.session_state["levures"]
            dict_levures = {"---": "---"}
            for levure in list_of_levures:
                dict_levures[levure.espece] = str(levure)

            # Mise en page et création des formulaires pour les capteurs
            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)
            list_col = [col1, col2, col3, col4]
            for i in range(4):
                with list_col[i]:
                    st.write(f"**Capteur_{i + 1}**")
                    input_alias = st.text_input("Alias*", key=i, value=f"Capteur-{i+1}")
                    selectfarine = st.selectbox("Farine", list(dict_farines.items()), key=i,
                                                format_func=lambda o: o[1])
                    selectlevain = st.selectbox("Levain", list(dict_levains.items()), key=i, format_func=lambda o: o[1])
                    select_levure = st.selectbox("Levure", list(dict_levures.items()), key=i,
                                                 format_func=lambda o: o[1])
                    input_remarque = st.text_area("Remarque", max_chars=100, key=i)
                    tab_cpt.append((input_alias, selectfarine[0], selectlevain[0], select_levure[0],
                                    input_remarque))
                    tab_titre_cpt.append(input_alias)

            if st.form_submit_button('Lancer'):
                can_go = True
                if upload_file is None or input_operateur == "" or input_lieu == "":
                    st.error("Certains champs obligatoires ne sont pas encore remplis.")
                    can_go = False
                projet_chosen = None
                if self.session_state.allow_access > 1:
                    operateur = models.get_by("users", "login", input_operateur)
                    if not operateur:
                        st.error("Opérateur inconnus")
                        can_go = False
                    if selectprojet[0] == '---':
                        projet_chosen = None
                    else:
                        projet_chosen = selectprojet[0]
                    boitier_chosen = int(boitier_selected[0])
                else:
                    boitier_chosen = boitier_selected
                if can_go:
                    experience = Experience(boitier_chosen, input_date, input_lieu, input_operateur,
                                            tab_titre_cpt, projet_chosen, upload_file)
                    experience.fichier_resultat = f"files/{experience.identificateur}.TXT"
                    st.session_state['experience'] = experience
                    list_of_capteurs = []
                    i = 1
                    for infos in tab_cpt:
                        if infos[1] == '---':
                            farine_chosen = None
                        else:
                            farine_chosen = infos[1]
                        if infos[2] == '---':
                            levain_chosen = None
                        else:
                            levain_chosen = infos[2]
                        if infos[3] == '---':
                            levure_chosen = None
                        else:
                            levure_chosen = infos[3]
                        cpt = Capteur(i, experience.get_id(), infos[0], farine_chosen, levain_chosen, levure_chosen,
                                      infos[4], experience.get_id() + infos[0] + '.csv')
                        i += 1
                        list_of_capteurs.append(cpt)
                    st.session_state[f'capteurs'] = list_of_capteurs
                    st.success(f"Résultats génerés ! **Allez consulter la page Résultats**")
