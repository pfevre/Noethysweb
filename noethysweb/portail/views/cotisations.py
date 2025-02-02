# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import logging
logger = logging.getLogger(__name__)
from portail.views.base import CustomView
from django.views.generic import TemplateView
from cotisations.utils import utils_cotisations_manquantes
from core.models import Cotisation


class View(CustomView, TemplateView):
    menu_code = "portail_cotisations"
    template_name = "portail/cotisations.html"

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['page_titre'] = "Adhésions"

        # Adhésions à fournir
        context['cotisations_fournir'] = utils_cotisations_manquantes.Get_cotisations_manquantes(famille=self.request.user.famille)

        # Liste des dernières adhésions
        context['liste_cotisations'] = Cotisation.objects.select_related("prestation", "individu").filter(famille=self.request.user.famille).order_by("date_debut")

        return context
