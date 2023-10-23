"""
This file allows you to run the project app.
"""
from multipage import MultiPage
from pages import recuperation_choix
from pages import absences_oir
from pages import plan_dated_assign
from pages import regimes



app = MultiPage()

# Add all your application here
app.add_page("Récupération des Choix", recuperation_choix.app)
app.add_page("Récupération des Absences", absences_oir.app)
app.add_page("Plan Dated Assign", plan_dated_assign.app)
app.add_page("Récupération des Régimes", regimes.app)


# The main app
app.run()

