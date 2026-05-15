import streamlit as st

from models import (
    get_config_values,
    add_config,
    update_config
)


def admin_screen():

    col1, col2 = st.columns([1,5])

    with col1:
        if st.button("⬅️"):

            st.session_state.page = "main"

            st.rerun()

    with col2:
        st.markdown("## ⚙️ Administration")
        # =================================================
        # COLORS
        # =================================================

        with st.expander("🎨 Couleurs", expanded=False):

            colors = get_config_values("color")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_color"):

                new_color = st.text_input("Nouvelle couleur")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_color:

                add_config("color", new_color)

                st.success("Couleur ajoutée")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in colors:

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3, col4 = st.columns([3,2,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Extra",
                        c.get("extra", ""),
                        key=f"extra_{c['id']}", placeholder="#FFFFFF"
                    )

                    # SORT

                    new_sort = col3.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col4.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "extra": extra,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        # =================================================
        # BADGES
        # =================================================
        with st.expander("🎖️ Badges", expanded=False):

            badges = get_config_values("badge")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_badge"):

                new_badge = st.text_input("Nouveau badge")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_badge:

                add_config("badge", new_badge)

                st.success("Badge ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in badges :

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns([4,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # SORT

                    new_sort = col2.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col3.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        # =================================================
        # Profil aromatique
        # =================================================
        with st.expander("🌸 Profil aromatique", expanded=False):

            keywords = get_config_values("profilAromatique")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_keyword"):

                new_keyword = st.text_input("Nouveau mot-clé")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_keyword:

                add_config("profilAromatique", new_keyword)

                st.success("Mot-clé ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in keywords :

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns([4,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # SORT

                    new_sort = col2.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col3.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        # =================================================
        # Moments
        # =================================================
        with st.expander("🕒 Moments", expanded=False):

            moments = get_config_values("moment")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_moment"):

                new_moment = st.text_input("Nouveau moment")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_moment:

                add_config("moment", new_moment)

                st.success("Moment ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in moments :

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns([4,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # SORT

                    new_sort = col2.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col3.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        # =================================================
        # Containers
        # =================================================
        with st.expander("📦 Containers", expanded=False):

            containers = get_config_values("contenant")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_container"):

                new_container = st.text_input("Nouveau contenant")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_container:

                add_config("contenant", new_container)

                st.success("Contenant ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in containers :

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns([4,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # SORT

                    new_sort = col2.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col3.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        # =================================================
        # Statuts
        # =================================================
        with st.expander("📋 Statuts", expanded=False):

            statuses = get_config_values("status")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_status"):

                new_status = st.text_input("Nouveau statut")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_status:

                add_config("status", new_status)

                st.success("Statut ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in statuses :

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns([4,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # SORT

                    new_sort = col2.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col3.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

        # =================================================
        # SYNONYMS
        # =================================================

        with st.expander("🧠 synonymes", expanded=False):

            synonyms = get_config_values("synonym")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_synonym"):

                new_synonym = st.text_input("Nouveau synonyme")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_synonym:

                add_config("synonym", new_synonym)

                st.success("Synonyme ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in synonyms:

                with st.container():

                    st.markdown(
                        """
                        <div class="form-card">
                        """,
                        unsafe_allow_html=True
                    )

                    col1, col2, col3, col4 = st.columns([3,2,2,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Synonymes (séparés par des virgules)",
                        c.get("extra", ""),
                        key=f"extra_{c['id']}", placeholder="valeur1,valeur2,valeur3"
                    )

                    # SORT

                    new_sort = col3.number_input(
                        "Ordre",
                        value=c.get("sort_order", 0),
                        step=1,
                        key=f"sort_{c['id']}"
                    )

                    # ACTIVE

                    active = col4.checkbox(
                        "Active",
                        value=c.get("active", True),
                        key=f"active_{c['id']}"
                    )

                    # SAVE

                    if st.button(
                        "💾 Sauvegarder",
                        key=f"save_{c['id']}"
                    ):

                        update_config(
                            c["id"],
                            {
                                "value": new_value,
                                "extra": extra,
                                "sort_order": new_sort,
                                "active": active
                            }
                        )

                        st.success("Sauvegardé")

                        st.rerun()

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
                    )

