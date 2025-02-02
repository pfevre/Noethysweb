# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import json
from django.urls import reverse
from django.views.generic import TemplateView
from core.views.base import CustomView
from core.utils import utils_dates
from core.models import Consommation, Groupe, UniteRemplissage


class View(CustomView, TemplateView):
    menu_code = "accueil"
    template_name = "consommations/detail_consommations.html"

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context["page_titre"] = "Détail des consommations"
        context["resultats"] = self.Get_resultats(donnee=kwargs["donnee"])
        return context

    def Get_resultats(self, donnee=None):
        date = utils_dates.ConvertDateENGtoDate(donnee.split("_")[0])
        unite_remplissage = UniteRemplissage.objects.prefetch_related("unites").get(pk=int(donnee.split("_")[1]))
        groupe = Groupe.objects.get(pk=int(donnee.split("_")[2]))

        # Importation des consommations associées à l'unité de remplissage
        dict_conso = {}
        consommations = Consommation.objects.select_related('unite', 'activite', 'groupe', 'evenement', 'inscription', 'individu').filter(date=date, unite__in=unite_remplissage.unites.all(), groupe=groupe).order_by("individu__nom", "individu__prenom")
        for conso in consommations:
            dict_conso.setdefault(conso.individu, [])
            dict_conso[conso.individu].append(conso)

        # Remplissage du tableau
        liste_lignes = []
        for individu, liste_conso in dict_conso.items():
            label = individu.Get_nom()
            unites = " + ".join(["%s (%s)" % (conso.unite.nom, conso.get_etat_display()) for conso in liste_conso])
            date_saisie = str(liste_conso[0].date_saisie.date().strftime("%d/%m/%Y"))
            action = " ".join([
                "<a type='button' title='Accéder à la fiche famille' class='btn btn-default btn-xs' href='%s'><i class='fa fa-folder-open-o'></i></a>" % reverse("famille_resume", args=[conso.inscription.famille_id]),
                "<a type='button' title='Accéder aux consommations' class='btn btn-default btn-xs' href='%s'><i class='fa fa-fw fa-calendar'></i></a>" % reverse("famille_consommations", args=[conso.inscription.famille_id, conso.inscription.individu_id]),
            ])
            liste_lignes.append({"label": label, "unites": unites, "date_saisie": date_saisie, "action": action})

        return {"date": date, "unite_remplissage": unite_remplissage, "groupe": groupe, "liste_lignes": json.dumps(liste_lignes)}
