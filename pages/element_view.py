import streamlit as st
from hydralit import HydraHeadApp
import models


class FarinePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        with st.expander("Ajouter une farine"):
            with st.form("add_farine"):
                input_alias = st.text_input("Alias", max_chars=50)
                input_cereale = st.text_input("Céréale", max_chars=50)
                input_mouture = st.text_input("Mouture", max_chars=50)
                input_cendre = st.text_input("Cendres", max_chars=50)
                input_origine = st.text_input("Origine", max_chars=50)
                st.write("Champs obligatoires marqués d'un *")
                if st.form_submit_button("Ajouter"):
                    farine = models.Farine(input_alias, input_cereale, input_mouture, input_cendre, input_origine)
                    if self.session_state.allow_access > 1:
                        farine.create_farine()
                    else:
                        if "farines" not in st.session_state:
                            st.session_state['farines'] = []
                        st.session_state['farines'].append(farine)

        with st.container():
            all_farines = []
            if self.session_state.allow_access > 1:
                all_farines = models.Farine.get_farines()
            if "farines" in st.session_state:
                all_farines = st.session_state['farines']

            for farine in all_farines:
                st.write(str(farine))


class LevainPage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        with st.expander("Ajouter un Levain"):
            with st.form("add_levain"):
                farines = []
                if self.session_state.allow_access > 1:
                    farines = models.Farine.get_farines()
                if "farines" in st.session_state:
                    farines = st.session_state['farines']

                farines_id = {"---": "---", }
                for farine in farines:
                    if self.session_state.allow_access > 1:
                        farines_id[farine.id_farine] = str(farine)
                    else:
                        farines_id[farine] = str(farine)
                input_alias = st.text_input("Alias", max_chars=50)
                select_farine = st.selectbox("Numéro de la farine", list(farines_id.items()), 0, format_func=lambda o: o[1])
                input_origine = st.text_input("Origine", max_chars=100)
                input_cereale = st.text_input("Céréale", max_chars=50)
                input_hydratation = st.number_input("% Hydratation", max_value=999)
                input_bacterie = st.text_input("Bactérie", max_chars=50)
                st.write("Champs obligatoirs marqués d'un *")
                if st.form_submit_button("Ajouter"):
                    if input_hydratation < 0:
                        hydratation_value = ''
                    else:
                        hydratation_value = input_hydratation
                    if select_farine == "---":
                        farine_choosen = ''
                    else:
                        farine_choosen = select_farine[0]

                    levain = models.Levain(input_alias, farine_choosen, input_origine, input_cereale,
                                           hydratation_value, input_bacterie)

                    if self.session_state.allow_access > 1:
                        levain.create_levain()
                    else:
                        if "levains" not in st.session_state:
                            st.session_state["levains"] = []

                        st.session_state["levains"].append(levain)

        with st.container():
            all_levains = []
            if self.session_state.allow_access > 1:
                all_levains = models.Levain.get_levains()
            if "levains" in st.session_state:
                all_levains = st.session_state["levains"]
            for levain in all_levains:
                st.write(str(levain))


class LevurePage(HydraHeadApp):
    def __init__(self, title='', **kwargs):
        self.__dict__.update(kwargs)
        self.title = title

    def run(self):
        with st.expander("Ajouter levure"):
            with st.form("form levures"):
                input_espece = st.text_input("Espèce*", max_chars=50)
                input_origine = st.text_input("Origine*", max_chars=50)
                st.write("champs obligatoires marqués d'un *")

                if st.form_submit_button("Ajouter"):
                    levure = models.Levure(input_espece, input_origine)
                    if self.session_state.allow_access > 1:
                        levure.create_levure()
                    if "levures" not in st.session_state:
                        st.session_state["levures"] = []
                    st.session_state["levures"].append(levure)

        with st.container():
            all_levures = []
            if self.session_state.allow_access > 1:
                all_levures = models.Levure.get_levures()
            if "levures" in st.session_state:
                all_levures = st.session_state["levures"]
            for levure in all_levures:
                st.write(str(levure))
