# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from core.views import crud
from core.models import Collaborateur, DestinataireSMS
from core.views.mydatatableview import MyDatatable, columns
from outils.views.editeur_sms import Page_destinataires


class Liste(Page_destinataires, crud.Liste):
    model = Collaborateur
    template_name = "outils/editeur_sms_destinataires.html"
    categorie = "collaborateur"

    def get_queryset(self):
        return Collaborateur.objects.filter(self.Get_filtres("Q"))

    def get_context_data(self, **kwargs):
        context = super(Liste, self).get_context_data(**kwargs)
        context['box_titre'] = "Sélection de collaborateurs"
        context['box_introduction'] = context['box_introduction'] = "Cochez les collaborateurs souhaités ci-dessous. Cochez la case de l'entête en haut à gauche pour cocher tous les collaborateurs affichés. Astuce : Utilisez le bouton Filtrer <i class='fa fa-filter text-gray'></i> pour sélectionner les présents d'une période spécifique."
        context['active_checkbox'] = True
        context['bouton_supprimer'] = False
        context["hauteur_table"] = "400px"
        context['liste_coches'] = [destinataire.collaborateur_id for destinataire in DestinataireSMS.objects.filter(categorie="collaborateur", sms=self.kwargs.get("idsms"))]
        return context

    class datatable_class(MyDatatable):
        filtres = ["idcollaborateur", "nom", "prenom", "tel_mobile", "rue_resid", "cp_resid", "ville_resid"]
        check = columns.CheckBoxSelectColumn(label="")

        class Meta:
            structure_template = MyDatatable.structure_template
            columns = ['check', "idcollaborateur", "nom", "prenom", "tel_mobile", "rue_resid", "cp_resid", "ville_resid"]
            ordering = ["nom", "prenom"]
