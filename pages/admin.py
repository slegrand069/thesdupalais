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
                        '<div class="form-card">',
                        unsafe_allow_html=True
                    )

                    col0, col1, col2, col3, col4 = st.columns([1,3,2,2,1])

                    # =================================================
                    # PREVIEW COLOR
                    # =================================================

                    with col0:

                        color_value = c.get("extra") or "#FFFFFF"

                        st.markdown(f"""
                            <div style="
                                width:32px;
                                height:32px;
                                border-radius:8px;
                                background:{color_value};
                                border:1px solid rgba(0,0,0,0.15);
                                margin-top:28px;
                            "></div>
                        """, unsafe_allow_html=True)

                    # =================================================
                    # VALUE
                    # =================================================

                    with col1:

                        new_value = st.text_input(
                            "Nom",
                            c["value"],
                            key=f"value_{c['id']}"
                        )

                    # =================================================
                    # COLOR PICKER
                    # =================================================

                    with col2:

                        new_extra = st.color_picker(
                            "Couleur",
                            value=color_value,
                            key=f"extra_{c['id']}"
                        )

                    # =================================================
                    # SORT
                    # =================================================

                    with col3:

                        new_sort = st.number_input(
                            "Ordre",
                            value=c.get("sort_order", 0),
                            step=1,
                            key=f"sort_{c['id']}"
                        )

                    # =================================================
                    # ACTIVE
                    # =================================================

                    with col4:

                        new_active = st.checkbox(
                            "ON",
                            value=c.get("active", True),
                            key=f"active_{c['id']}"
                        )

                    st.markdown(
                        "</div>",
                        unsafe_allow_html=True
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
                                "extra": new_extra,
                                "sort_order": new_sort,
                                "active": new_active
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

                    col1, col2, col3, col4 = st.columns([3,3,1,2])

                    # VALUE

                    new_value = col1.text_input(
                        "Nom",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Synonymes",
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

        # =================================================
        # NATIONALITIES
        # =================================================

        with st.expander("🌍 nationalités", expanded=False):

            countries = get_config_values("nationality")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------

            with st.form("add_nationality"):

                new_nationality = st.text_input("Nouvelle nationalité")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_nationality:

                add_config("nationality", new_nationality)

                st.success("Nationalité ajoutée")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in countries:

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
                        "Nationalité",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Pays",
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

        # =================================================
        # MOMENTS INTENTS
        # =================================================

        with st.expander("🌇 Moments Intents", expanded=False):

            moments = get_config_values("momentsIntents")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------
            with st.form("add_moment_intent"):

                new_moment_intent = st.text_input("Nouveau moment intent")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_moment_intent:

                add_config("momentsIntents", new_moment_intent)

                st.success("Moment intent ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in moments:

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
                        "Moment Intent",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Moment",
                        c.get("extra", ""),
                        key=f"extra_{c['id']}", placeholder="Période"
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
        # CONCEPTS
        # =================================================

        with st.expander("🎛️ Concepts", expanded=False):

            concepts = get_config_values("concept")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------
            with st.form("add_concept"):

                new_concept = st.text_input("Nouveau concept")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_concept:

                add_config("concept", new_concept)

                st.success("Concept ajouté")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in concepts:

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
                        "Concept",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Traduction",
                        c.get("extra", ""),
                        key=f"extra_{c['id']}", placeholder="Valeurs"
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
        # FUZZY MATCHING
        # =================================================

        with st.expander("📝 Auto corrections", expanded=False):

            fuzzyMatchings = get_config_values("fuzzyMatching")

            # ---------------------------------------------
            # AJOUT
            # ---------------------------------------------
            with st.form("add_fuzzyMatching"):

                new_fuzzyMatching = st.text_input("Nouvelle auto correction")

                submitted = st.form_submit_button(
                    "➕ Ajouter"
                )

            if submitted and new_fuzzyMatching:

                add_config("fuzzyMatching", new_fuzzyMatching)

                st.success("Auto correction ajoutée")

                st.rerun()

            # ---------------------------------------------
            # LISTE
            # ---------------------------------------------

            for c in fuzzyMatchings:

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
                        "Auto correction",
                        c["value"],
                        key=f"value_{c['id']}"
                    )

                    # EXTRA
                    extra = col2.text_input(
                        "Correction",
                        c.get("extra", ""),
                        key=f"extra_{c['id']}", placeholder="Valeurs"
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
