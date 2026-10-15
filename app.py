import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="ERP DigiPrint", page_icon="🖨️", layout="wide")

PAGES = [
    "Tableau de bord", "Commercial", "Infographie", "Stock", "Achats",
    "Production", "Finition", "Livraison", "Comptabilité clients",
    "Comptabilité fournisseurs", "Direction d'exploitation", "Coût de revient",
    "Administration & sécurité", "Référentiel", "Informatique & maintenance"
]

LIMITS = {
"Tableau de bord":["Indicateurs basés uniquement sur les données de démonstration.","Aucun calcul comptable certifié ni synchronisation avec les autres logiciels."],
"Commercial":["Devis et commandes simulés : aucun document n'est envoyé.","Pas de signature, gestion avancée du crédit client ni validation juridique."],
"Infographie":["Suivi du statut du fichier uniquement ; aucun contrôle prépresse/RIP réel.","Pas de GED sécurisée, versioning fiable ou BAT signé."],
"Stock":["Quantités fictives ; pas de codes-barres, lots ni inventaire mobile.","Conversions d'unités, valorisation et règles de réutilisation des chutes à valider."],
"Achats":["Aucune commande n'est envoyée aux fournisseurs.","Pas de rapprochement automatique commande-réception-facture."],
"Production":["Saisie manuelle ; aucune connexion aux machines ou capteurs.","Cadences, temps, rebuts et consommations doivent être mesurés sur le terrain."],
"Finition":["Contrôle qualité illustratif, sans preuve signée ni traçabilité par lot.","Critères d'acceptation à définir par type de produit."],
"Livraison":["Pas de transporteur, GPS, SMS ni preuve électronique de livraison.","Retours, livraisons partielles et frais de transport restent à spécifier."],
"Comptabilité clients":["Factures et encaissements fictifs, non comptabilisés.","Pas de FNE, rapprochement bancaire ni validation fiscale."],
"Comptabilité fournisseurs":["Échéances fictives ; aucune écriture comptable réelle.","Taxes, retenues et pièces justificatives à valider avec un professionnel local."],
"Direction d'exploitation":["Qualité des indicateurs dépendante des saisies.","Seuils d'alerte, objectifs et responsabilités à valider par la direction."],
"Coût de revient":["Tarifs horaires et taux de frais indirects illustratifs.","Fiabilité dépend des consommations, temps, pertes et règles de valorisation des chutes."],
"Administration & sécurité":["Le prototype ne fournit pas de vraie authentification ni autorisation.","Pas de MFA, audit inviolable, gestion des secrets ou séparation des rôles en base."],
"Référentiel":["Données d'exemple sans contrôle complet des doublons.","Identifiants, relations, unités et contraintes doivent être définis avant production."],
"Informatique & maintenance":["Suivi manuel sans notifications ni supervision.","Sauvegardes, reprise après sinistre et calendrier de maintenance non automatisés."]
}

if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame([
        {"Commande":"CMD-26041","Client":"Client Démo A","Produit":"Cabas personnalisé","Quantité":500,"Échéance":"2026-10-18","Statut":"En production","Montant FCFA":425000},
        {"Commande":"CMD-26042","Client":"Client Démo B","Produit":"Affiches A2","Quantité":1000,"Échéance":"2026-10-16","Statut":"Infographie","Montant FCFA":180000},
        {"Commande":"CMD-26043","Client":"Client Démo C","Produit":"Cartes de visite","Quantité":2000,"Échéance":"2026-10-20","Statut":"À planifier","Montant FCFA":95000},
    ])
if "stock" not in st.session_state:
    st.session_state.stock = pd.DataFrame([
        {"Référence":"MAT-001","Article":"Papier couché","Catégorie":"Papier","Unité":"rame","Stock":42,"Seuil":15,"Coût unitaire":6500},
        {"Référence":"MAT-002","Article":"Encre cyan","Catégorie":"Encre","Unité":"L","Stock":8,"Seuil":10,"Coût unitaire":18000},
        {"Référence":"MAT-003","Article":"Support cabas","Catégorie":"Support","Unité":"m","Stock":120,"Seuil":30,"Coût unitaire":900},
        {"Référence":"PIE-001","Article":"Courroie machine","Catégorie":"Pièce détachée","Unité":"pièce","Stock":2,"Seuil":2,"Coût unitaire":22000},
        {"Référence":"MAT-004","Article":"Chutes réutilisables","Catégorie":"Chute","Unité":"m","Stock":18,"Seuil":0,"Coût unitaire":450},
    ])
if "production" not in st.session_state:
    st.session_state.production = pd.DataFrame([
        {"OF":"OF-1001","Commande":"CMD-26041","Produit":"Cabas personnalisé","Prévu":500,"Réalisé":320,"Machine":"Presse A","Statut":"En cours"},
        {"OF":"OF-1002","Commande":"CMD-26042","Produit":"Affiches A2","Prévu":1000,"Réalisé":0,"Machine":"Imprimante B","Statut":"À lancer"},
    ])
if "purchases" not in st.session_state:
    st.session_state.purchases = pd.DataFrame([
        {"Demande":"DA-026","Article":"Encre cyan","Quantité":20,"Fournisseur":"Fournisseur Démo","Statut":"À approuver"},
        {"Demande":"DA-027","Article":"Courroie machine","Quantité":4,"Fournisseur":"Fournisseur Démo","Statut":"Commandée"},
    ])

def fcfa(n):
    return f"{n:,.0f}".replace(",", " ") + " FCFA"

def limits(page):
    with st.expander("Limites de cette page et points à valider"):
        for item in LIMITS[page]:
            st.markdown("- " + item)

def header(title, sub):
    st.title(title)
    st.caption(sub)

def dashboard():
    header("Tableau de bord", "Vue générale des opérations — données fictives de présentation")
    o, s, p = st.session_state.orders, st.session_state.stock, st.session_state.production
    a,b,c,d = st.columns(4)
    a.metric("Commandes", len(o))
    b.metric("Montant commandes", fcfa(o["Montant FCFA"].sum()))
    c.metric("Références au seuil", int((s.Stock <= s.Seuil).sum()))
    d.metric("Quantité produite déclarée", int(p["Réalisé"].sum()))
    x,y = st.columns(2)
    with x:
        st.subheader("Commandes par statut")
        st.plotly_chart(px.histogram(o, x="Statut", color="Statut"), use_container_width=True)
    with y:
        st.subheader("Avancement de production")
        st.plotly_chart(px.bar(p, x="OF", y=["Réalisé","Prévu"], barmode="group"), use_container_width=True)
    st.subheader("Commandes à suivre")
    st.dataframe(o, use_container_width=True, hide_index=True)
    limits("Tableau de bord")

def commercial():
    header("Commercial", "Clients, devis, commandes et échéances")
    st.dataframe(st.session_state.orders, use_container_width=True, hide_index=True)
    with st.form("order"):
        client = st.text_input("Client")
        product = st.text_input("Produit")
        qty = st.number_input("Quantité", min_value=1, value=100)
        due = st.date_input("Échéance", value=date.today())
        amount = st.number_input("Montant estimatif (FCFA)", min_value=0, value=50000, step=5000)
        submit = st.form_submit_button("Ajouter commande de démonstration")
    if submit:
        if not client.strip() or not product.strip():
            st.error("Renseignez le client et le produit.")
        else:
            n = len(st.session_state.orders)+1
            row = {"Commande":f"CMD-DEMO-{n:03d}","Client":client,"Produit":product,"Quantité":int(qty),"Échéance":due.isoformat(),"Statut":"À planifier","Montant FCFA":int(amount)}
            st.session_state.orders = pd.concat([st.session_state.orders,pd.DataFrame([row])],ignore_index=True)
            st.success("Commande ajoutée en mémoire.")
            st.rerun()
    limits("Commercial")

def stock():
    header("Stock", "Matières premières, consommables, pièces et chutes")
    df=st.session_state.stock.copy()
    df["Valeur indicative FCFA"]=df.Stock*df["Coût unitaire"]
    st.dataframe(df,use_container_width=True,hide_index=True)
    low=df[df.Stock<=df.Seuil]
    if len(low): st.warning("À surveiller : "+", ".join(low.Article))
    with st.form("move"):
        ref=st.selectbox("Article",df.Référence.tolist())
        kind=st.radio("Mouvement",["Entrée","Sortie"],horizontal=True)
        qty=st.number_input("Quantité",min_value=0.01,value=1.0)
        reason=st.selectbox("Motif",["Réception achat","Consommation production","Retour atelier","Inventaire","Réutilisation de chute"])
        submit=st.form_submit_button("Enregistrer le mouvement")
    if submit:
        i=st.session_state.stock.index[st.session_state.stock.Référence==ref][0]
        new=float(st.session_state.stock.loc[i,"Stock"])+(qty if kind=="Entrée" else -qty)
        if new<0: st.error("Mouvement refusé : stock insuffisant.")
        else:
            st.session_state.stock.loc[i,"Stock"]=new
            st.success(f"Mouvement de {qty:g} enregistré ({reason}).")
            st.rerun()
    with st.expander("Simuler la valeur d'une chute réutilisable"):
        price=st.number_input("Prix de référence unitaire (FCFA)",min_value=0,value=1000)
        rate=st.slider("Coefficient indicatif de valorisation (%)",0,100,50)
        st.metric("Valeur indicative",fcfa(price*rate/100))
    limits("Stock")

def purchases():
    header("Achats","Demandes d'achat, approbations et commandes fournisseurs")
    st.dataframe(st.session_state.purchases,use_container_width=True,hide_index=True)
    with st.form("purchase"):
        article=st.text_input("Article à acheter")
        qty=st.number_input("Quantité demandée",min_value=1,value=5)
        supplier=st.text_input("Fournisseur")
        status=st.selectbox("Statut",["Brouillon","À approuver","Approuvée","Commandée","Reçue"])
        submit=st.form_submit_button("Créer demande")
    if submit:
        if article.strip() and supplier.strip():
            n=len(st.session_state.purchases)+1
            row={"Demande":f"DA-DEMO-{n:03d}","Article":article,"Quantité":int(qty),"Fournisseur":supplier,"Statut":status}
            st.session_state.purchases=pd.concat([st.session_state.purchases,pd.DataFrame([row])],ignore_index=True)
            st.success("Demande ajoutée."); st.rerun()
        else: st.error("Renseignez article et fournisseur.")
    limits("Achats")

def production():
    header("Production","Ordres de fabrication, avancement et machines")
    st.dataframe(st.session_state.production,use_container_width=True,hide_index=True)
    with st.form("of"):
        order=st.selectbox("Commande liée",st.session_state.orders.Commande.tolist())
        product=st.text_input("Produit","Produit de démonstration")
        planned=st.number_input("Quantité prévue",min_value=1,value=100)
        machine=st.selectbox("Machine",["Presse A","Imprimante B","Traceur C","Machine de finition"])
        submit=st.form_submit_button("Créer un OF")
    if submit:
        n=len(st.session_state.production)+1
        row={"OF":f"OF-DEMO-{n:03d}","Commande":order,"Produit":product,"Prévu":int(planned),"Réalisé":0,"Machine":machine,"Statut":"À lancer"}
        st.session_state.production=pd.concat([st.session_state.production,pd.DataFrame([row])],ignore_index=True)
        st.success("Ordre de fabrication créé."); st.rerun()
    with st.form("progress"):
        of=st.selectbox("OF à mettre à jour",st.session_state.production.OF.tolist())
        qty=st.number_input("Quantité réalisée à ajouter",min_value=1,value=10)
        submit2=st.form_submit_button("Déclarer la production")
    if submit2:
        i=st.session_state.production.index[st.session_state.production.OF==of][0]
        total=int(st.session_state.production.loc[i,"Réalisé"])+int(qty)
        planned=int(st.session_state.production.loc[i,"Prévu"])
        if total>planned: st.error("La quantité dépasserait le prévu.")
        else:
            st.session_state.production.loc[i,"Réalisé"]=total
            st.session_state.production.loc[i,"Statut"]="Terminé" if total==planned else "En cours"
            st.success("Avancement enregistré."); st.rerun()
    limits("Production")

def costing():
    header("Coût de revient","Estimation pédagogique du coût d'un produit")
    st.warning("Les paramètres sont fictifs : ne pas utiliser pour fixer un prix réel sans validation.")
    with st.form("cost"):
        product=st.text_input("Produit","Cabas personnalisé")
        qty=st.number_input("Quantité produite",min_value=1,value=500)
        material=st.number_input("Matières consommées (FCFA)",min_value=0,value=150000,step=5000)
        hours=st.number_input("Heures de main-d'œuvre",min_value=0.0,value=12.0,step=0.5)
        labor_rate=st.number_input("Coût horaire main-d'œuvre",min_value=0,value=2500,step=250)
        machine_hours=st.number_input("Heures machine",min_value=0.0,value=5.0,step=0.5)
        machine_rate=st.number_input("Coût horaire machine",min_value=0,value=8000,step=500)
        finish=st.number_input("Finition / emballage (FCFA)",min_value=0,value=25000,step=2500)
        overhead=st.slider("Frais indirects indicatifs (%)",0,50,10)
        planned=st.number_input("Coût prévu total (FCFA)",min_value=0,value=300000,step=10000)
        submit=st.form_submit_button("Calculer")
    if submit:
        labor=hours*labor_rate; machine=machine_hours*machine_rate
        direct=material+labor+machine+finish; indirect=direct*overhead/100; total=direct+indirect
        a,b,c=st.columns(3)
        a.metric("Coût total estimé",fcfa(total)); b.metric("Coût unitaire",fcfa(total/qty)); c.metric("Frais indirects",fcfa(indirect))
        breakdown=pd.DataFrame({"Poste":["Matières","Main-d'œuvre","Machine","Finition","Frais indirects"],"Montant":[material,labor,machine,finish,indirect]})
        st.plotly_chart(px.bar(breakdown,x="Poste",y="Montant"),use_container_width=True)
        st.metric("Écart par rapport au prévu",fcfa(total-planned),delta_color="inverse")
        st.caption("Produit : "+product+" — estimation uniquement.")
    limits("Coût de revient")

def simple_page(page):
    header(page, {
      "Infographie":"Préparation des fichiers, BAT et passage en production",
      "Finition":"Contrôle qualité, assemblage, emballage et préparation de sortie",
      "Livraison":"Planification, expédition, réception client et retours",
      "Comptabilité clients":"Facturation, encaissements et suivi des créances",
      "Comptabilité fournisseurs":"Factures fournisseurs, échéances et paiements",
      "Direction d'exploitation":"Pilotage des délais, de la qualité, des coûts et de la capacité",
      "Administration & sécurité":"Rôles, validations, journalisation et conformité",
      "Référentiel":"Produits, machines, fournisseurs, unités et règles métier",
      "Informatique & maintenance":"État des machines, maintenance préventive et incidents"
    }.get(page,"Module de démonstration"))
    if page=="Infographie":
        df=st.session_state.orders[["Commande","Client","Produit","Quantité","Statut"]].copy()
        df["État fichier"]=["À vérifier","BAT envoyé","Validé"][:len(df)] if len(df)<=3 else "À vérifier"
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.selectbox("Statut du fichier",["À recevoir","En préparation","BAT envoyé","Validé client","Correction demandée"])
        st.text_area("Commentaire infographie")
        st.button("Enregistrer le suivi (simulation)")
    elif page=="Finition":
        st.dataframe(st.session_state.orders[["Commande","Produit","Quantité","Statut"]],use_container_width=True,hide_index=True)
        st.selectbox("Résultat contrôle qualité",["En attente","Conforme","Conforme avec réserve","Non conforme"])
        st.number_input("Quantité conforme",min_value=0,value=100)
        st.number_input("Quantité rejetée / à reprendre",min_value=0,value=0)
        st.button("Enregistrer le contrôle (simulation)")
    elif page=="Livraison":
        st.dataframe(st.session_state.orders,use_container_width=True,hide_index=True)
        st.selectbox("Commande",st.session_state.orders.Commande.tolist())
        st.selectbox("Statut livraison",["À préparer","Prête à expédier","En route","Livrée","Livraison partielle","Échec / retour"])
        st.date_input("Date de livraison",value=date.today())
        st.text_input("Réceptionnaire")
        st.button("Enregistrer le suivi (simulation)")
    elif page=="Comptabilité clients":
        df=pd.DataFrame([{"Facture":"FAC-DEMO-001","Client":"Client Démo A","Montant":425000,"Payé":200000},{"Facture":"FAC-DEMO-002","Client":"Client Démo B","Montant":180000,"Payé":0}])
        df["Reste dû"]=df.Montant-df.Payé; st.dataframe(df,use_container_width=True,hide_index=True)
        st.metric("Créances affichées",fcfa(df["Reste dû"].sum()))
        st.selectbox("Mode de règlement",["Espèces","Virement","Mobile money","Chèque","Autre"])
        st.number_input("Montant du règlement",min_value=1,value=25000)
        st.button("Simuler encaissement")
    elif page=="Comptabilité fournisseurs":
        st.dataframe(pd.DataFrame([{"Facture":"FF-DEMO-001","Fournisseur":"Fournisseur A","Montant":130000,"Statut":"À valider"},{"Facture":"FF-DEMO-002","Fournisseur":"Fournisseur B","Montant":85000,"Statut":"Approuvée"}]),use_container_width=True,hide_index=True)
        st.text_input("Fournisseur"); st.text_input("N° facture"); st.number_input("Montant FCFA",min_value=0,value=50000)
        st.date_input("Échéance",value=date.today()); st.button("Ajouter facture simulée")
    elif page=="Direction d'exploitation":
        a,b,c=st.columns(3); a.metric("Ordres de fabrication",len(st.session_state.production)); b.metric("Quantité prévue",int(st.session_state.production.Prévu.sum())); c.metric("Quantité réalisée",int(st.session_state.production.Réalisé.sum()))
        st.dataframe(pd.DataFrame([{"Indicateur":"Respect des délais","Définition":"Livré à temps / livraisons"},{"Indicateur":"Taux de rebut","Définition":"Rejets / quantité produite"},{"Indicateur":"Utilisation machine","Définition":"Temps productif / temps disponible"},{"Indicateur":"Ruptures stock","Définition":"Références au seuil ou en dessous"}]),use_container_width=True,hide_index=True)
    elif page=="Administration & sécurité":
        st.dataframe(pd.DataFrame([{"Rôle":"Commercial","Accès cible":"Clients, devis, commandes"},{"Rôle":"Magasinier","Accès cible":"Mouvements de stock"},{"Rôle":"Production","Accès cible":"Ordres de fabrication"},{"Rôle":"Comptable","Accès cible":"Factures et règlements"},{"Rôle":"Direction","Accès cible":"Indicateurs et validations"},{"Rôle":"Administrateur","Accès cible":"Paramétrage"}]),use_container_width=True,hide_index=True)
        st.info("Le prototype ne protège pas réellement les accès. Les rôles affichés sont illustratifs.")
    elif page=="Référentiel":
        st.dataframe(pd.DataFrame([{"Code":"PRD-001","Produit":"Cabas personnalisé","Unité":"pièce"},{"Code":"PRD-002","Produit":"Affiche A2","Unité":"pièce"},{"Code":"MCH-001","Machine":"Presse A","Unité":"—"}]),use_container_width=True,hide_index=True)
        st.text_area("Règles à définir","Unités, conversions, seuils, taux de perte, identifiants uniques, règles d'approbation")
    elif page=="Informatique & maintenance":
        st.dataframe(pd.DataFrame([{"Machine":"Presse A","État":"Disponible","Priorité":"Normale"},{"Machine":"Imprimante B","État":"En production","Priorité":"À surveiller"},{"Machine":"Traceur C","État":"À contrôler","Priorité":"Élevée"}]),use_container_width=True,hide_index=True)
        st.selectbox("Type d'intervention",["Préventive","Corrective","Contrôle qualité","Incident informatique"])
        st.selectbox("Priorité",["Faible","Normale","Élevée","Critique"])
        st.text_area("Description du ticket")
        st.button("Créer ticket simulé")
    limits(page)

with st.sidebar:
    st.title("🖨️ ERP DigiPrint")
    st.caption("Prototype de présentation • v0.1")
    page=st.radio("Navigation",PAGES)
    st.divider()
    st.warning("Données fictives en mémoire. Les saisies peuvent disparaître à la fermeture de la session.")

if page=="Tableau de bord": dashboard()
elif page=="Commercial": commercial()
elif page=="Stock": stock()
elif page=="Achats": purchases()
elif page=="Production": production()
elif page=="Coût de revient": costing()
else: simple_page(page)

st.divider()
st.caption("ERP DigiPrint — prototype pédagogique. Aucune donnée affichée n'est certifiée ni destinée à la gestion réelle.")
