import pandas as pd
import matplotlib.pyplot as plt
"""
1 - Chargement et exploration des données :
    Charger le fichier Excel contenant les données des transactions à l'aide de pandas.
    Explorer le jeu de données pour comprendre sa structure et ses principaux attributs.
    S'assurer de bien gérer les champs de date et d'heure (Date_Règlement, Heure_Règlement).
"""

# Charger le fichier Excel contenant les données des transactions à l'aide de pandas.
data_frm = pd.read_csv('/home/abdeljalil/Downloads/REGLEMENTS_CARTES_PREPAYEES_FAST_FOOD.csv')
"""
Créer une copie des données pour s'assurer que l'original ne soit pas modifié.
"""
data_cpy = data_frm.copy()

def exploration_donnees(data_cpy):
    # Explorer le jeu de données pour comprendre sa structure et ses principaux attributs.
    print(data_frm.columns)  # Affiche les colonnes du DataFrame
    print(data_frm.duplicated().sum())  # Affiche le nombre de doublons
    print(data_frm['Prenom User'].duplicated())  # Vérifie les doublons dans la colonne 'Prenom User'
    print(data_frm.isnull().sum())  # Affiche les valeurs manquantes par colonne
    print(data_frm['Prenom User'])  # Affiche toutes les valeurs de la colonne 'Prenom User'
    print(data_frm['Prenom User'].unique())  # Affiche les valeurs uniques de 'Prenom User'
    print(data_frm['Prenom User'].nunique())  # Affiche le nombre de valeurs uniques dans 'Prenom User'
    print(data_frm.head())  # Affiche les 5 premières lignes des données

    print(data_frm.info())  # Informations sur la structure des données (colonnes, types, valeurs manquantes)
    print(data_frm.describe())  # Statistiques descriptives des colonnes numériques

    # Gérer les champs de date et d'heure (conversion des champs texte en format datetime)
    data_cpy['Date_Règlement'] = pd.to_datetime(data_cpy['Date_Règlement'], errors='coerce')
    data_cpy['Heure_Règlement'] = pd.to_datetime(data_cpy['Heure_Règlement'], format='%H:%M:%S', errors='coerce')
    print(data_cpy['Date_Règlement'].head())  # Vérification des premières valeurs après conversion
    print(data_frm['Heure_Règlement'].head())  # Vérification des premières valeurs après conversion

# exploration_donnees(data_cpy)

"""
2 - Analyse des tendances des transactions :
    Grouper les données par jour, semaine et mois pour analyser les tendances des montants de transactions (Montant_Rgl).
    Générer des graphiques linéaires pour les tendances journalières, hebdomadaires et mensuelles.
"""

def tendances_des_transactions(data_cpy):
    """Convertir la colonne 'Montant_Rgl' en type numérique pour s'assurer que seules les valeurs numériques sont utilisées."""
    data_cpy['Montant_Rgl'] = pd.to_numeric(data_cpy['Montant_Rgl'], errors='coerce')

    """Convertir la colonne 'Date_Règlement' en type datetime pour s'assurer que seules les valeurs de date sont utilisées."""
    data_cpy['Date_Règlement'] = pd.to_datetime(data_cpy['Date_Règlement'], errors='coerce')

    """Créer de nouvelles colonnes pour stocker les jours, semaines et mois extraits de 'Date_Règlement'."""
    data_cpy['jour'] = data_cpy['Date_Règlement'].dt.day  # Extraire le jour
    data_cpy['semain'] = data_cpy['Date_Règlement'].dt.isocalendar().week  # Extraire la semaine ISO
    data_cpy['mois'] = data_cpy['Date_Règlement'].dt.month  # Extraire le mois
    print("Colonne 'jour': \n", data_cpy['jour'].head())  # Vérification des premières valeurs
    print("Colonne 'semain': \n", data_cpy['semain'].head())  # Vérification des premières valeurs
    print("Colonne 'mois': \n", data_cpy['mois'].head())  # Vérification des premières valeurs

    # Grouper les données par jour, semaine et mois pour analyser les montants totaux par période
    transaction_day = data_cpy.groupby('jour')['Montant_Rgl'].sum()  # Grouper par jour
    transaction_week = data_cpy.groupby('semain')['Montant_Rgl'].sum()  # Grouper par semaine
    transaction_month = data_cpy.groupby('mois')['Montant_Rgl'].sum()  # Grouper par mois
    print("Montant total par jour: \n", transaction_day)
    print("Montant total par semaine: \n", transaction_week)
    print("Montant total par mois: \n", transaction_month)

    # Générer des graphiques linéaires pour les tendances journalières
    plt.figure(figsize=(10, 10))
    transaction_day.plot(kind='line', color='green', linewidth=2, marker='o')
    plt.title("Graphique des tendances journalières des transactions")
    plt.xlabel("Jours")
    plt.ylabel("Montants des transactions (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Générer des graphiques linéaires pour les tendances hebdomadaires
    plt.figure(figsize=(10, 10))
    transaction_week.plot(kind='line', color='darkorange', linewidth=2, marker='s')
    plt.title("Graphique des tendances hebdomadaires des transactions")
    plt.xlabel("Semaines")
    plt.ylabel("Montants des transactions (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Générer des graphiques linéaires pour les tendances mensuelles
    plt.figure(figsize=(10, 10))
    transaction_month.plot(kind='line', color='blue', linewidth=2, marker='^')
    plt.title("Graphique des tendances mensuelles des transactions")
    plt.xlabel("Mois")
    plt.ylabel("Montants des transactions (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# tendances_des_transactions(data_cpy)

"""
3 - Analyse des tendances d'utilisation des cartes prépayées :
    Analyser les tendances des soldes des cartes prépayées au fil du temps en groupant les données par date et en calculant la moyenne du solde (Solde_CPP).
    Créer un graphique linéaire pour visualiser les tendances des soldes journaliers des cartes prépayées.
"""

def tendances_dutilisation_cartes_prepayees(data_cpy):
    """Convertir 'Solde_CPP' en type numérique car il peut contenir des valeurs non numériques."""
    data_cpy['Solde_CPP'] = pd.to_numeric(data_cpy['Solde_CPP'], errors='coerce')

    # Grouper les données par date et calculer la moyenne des soldes des cartes prépayées
    groupant_par_date_moy_solde = data_cpy.groupby('Date_Règlement')['Solde_CPP'].mean()
    print("Groupement par date et calcul de la moyenne des soldes: \n", groupant_par_date_moy_solde)

    # Créer un graphique linéaire pour visualiser les tendances des soldes journaliers des cartes prépayées
    plt.figure(figsize=(20, 10))
    groupant_par_date_moy_solde.plot(kind='line', color='brown', linewidth=1, marker='o')
    plt.title('Tendances des soldes journaliers des cartes prépayées')
    plt.xlabel('Date')
    plt.ylabel('Solde moyen des cartes prépayées (€)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# tendances_dutilisation_cartes_prepayees(data_cpy)

"""
4 - Analyse du comportement des clients :
    Identifier les plus gros dépensiers en groupant les transactions par client (Nom User) et en calculant le montant total dépensé (Montant_Rgl).
    Calculer la dépense moyenne par transaction pour chaque client.
    Analyser les tendances du solde des cartes prépayées pour les clients les plus dépensiers.
    Créer des graphiques en barres pour visualiser :
        1 - Les 10 clients les plus dépensiers par montant total dépensé.
        2 - Les 10 clients avec la dépense moyenne par transaction la plus élevée.
        3 - Les 10 clients avec le solde moyen de carte prépayée le plus élevé.
"""

def comportement_clients(data_cpy):
    # Identifier les plus gros dépensiers en groupant les transactions par client (Nom User) et en calculant le montant total dépensé (Montant_Rgl).
    client_plu_gro_dep = data_cpy.groupby('Prenom User')['Montant_Rgl'].sum().sort_values(ascending=False)
    top_10_client = client_plu_gro_dep.head(10)  # Sélectionner les 10 plus gros dépensiers
    print(client_plu_gro_dep)  # Afficher tous les clients et leurs dépenses totales
    print(top_10_client)  # Afficher les 10 clients avec le montant total le plus élevé

    # Calculer le montant total dépensé par tous les clients
    total_montant_depense = client_plu_gro_dep.sum()
    print("Montant total dépensé par tous les clients :\n", total_montant_depense)

    # Analyser les tendances du solde des cartes prépayées pour les clients les plus dépensiers.
    depense_moyenne_client_plus_dépensiers = data_cpy.groupby('Bénéficiaire_CPP')['Solde_CPP'].mean().sort_values(ascending=False)
    top_10_depense_moyenne_client_plus_dépensiers = depense_moyenne_client_plus_dépensiers.head(10)
    print("Solde moyen des cartes prépayées des clients les plus dépensiers : \n", depense_moyenne_client_plus_dépensiers.head(10))

    # Créer des graphiques en barres pour visualiser :
    
    # 1. Les 10 clients les plus dépensiers par montant total dépensé.
    plt.figure(figsize=(10, 10))
    top_10_client.plot(kind='bar', color='forestgreen')
    plt.title('Top 10 Clients les Plus Gros Dépensiers (Total Dépenses)', fontsize=14)
    plt.xlabel('Client', fontsize=14)
    plt.ylabel('Montant Total Dépensé (€)', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Assurer une disposition correcte des éléments graphiques.
    plt.show()

    # 2. Les 10 clients avec la dépense moyenne par transaction la plus élevée.
    avg_spent_per_transaction = data_cpy.groupby('Bénéficiaire_CPP')['Montant_Rgl'].mean().sort_values(ascending=False)
    top_10_avg_spenders = avg_spent_per_transaction.head(10)
    print(top_10_avg_spenders)  # Afficher les clients avec la dépense moyenne par transaction la plus élevée

    plt.figure(figsize=(10, 6))
    top_10_avg_spenders.plot(kind='bar', color='darkorange')
    plt.title('Top 10 Clients par Dépense Moyenne par Transaction', fontsize=14)
    plt.xlabel('Client', fontsize=12)
    plt.ylabel('Dépense Moyenne par Transaction (€)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 3. Les 10 clients avec le solde moyen de carte prépayée le plus élevé.
    plt.figure(figsize=(10, 10))
    top_10_depense_moyenne_client_plus_dépensiers.plot(kind='bar', color='mediumblue')
    plt.title('Top 10 Clients avec Solde Moyen des Cartes Prépayées', fontsize=14)
    plt.xlabel('Client', fontsize=14)
    plt.ylabel('Solde Moyen des Cartes Prépayées (€)', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Assurer une bonne disposition des éléments du graphique.
    plt.show()

# comportement_clients(data_cpy)

"""
5 - Analyse des montants restants et des soldes à zéro :
    1 - Filtrer les transactions avec des montants restants impayés (Montant_Rst > 0) et grouper par client pour identifier les clients avec les soldes impayés les plus élevés.
    2 - Filtrer les transactions avec des soldes de carte prépayée égaux à zéro (Solde_CPP == 0) et analyser ces clients.
    3 - Créer des graphiques en barres pour visualiser les clients avec les montants restants impayés les plus élevés.
"""

def montants_restants_soldes_a_zero(data_cpy):
    # 1 - Filtrer les transactions avec des montants restants impayés (Montant_Rst > 0) et grouper par client pour identifier les clients avec les soldes impayés les plus élevés.
    montants_restants_impayes = data_cpy[data_cpy['Montant_Rst'] > 0]  # Filtrer les transactions impayées
    grp_client_restt_impayes = montants_restants_impayes.groupby('Bénéficiaire_CPP')['Montant_Rst'].sum().sort_values(ascending=False)
    top_10_client_restt_impayes = grp_client_restt_impayes.head(10)  # Sélectionner les 10 clients avec les montants impayés les plus élevés

    # 2 - Filtrer les transactions avec des soldes de carte prépayée égaux à zéro (Solde_CPP == 0) et analyser ces clients.
    soldes_carte_prépayée_égaux_zéro = data_cpy[data_cpy['Solde_CPP'] == 0]  # Filtrer les transactions avec solde égal à zéro
    print(soldes_carte_prépayée_égaux_zéro)  # Afficher les clients avec des soldes de carte prépayée égaux à zéro

    # 3 - Créer des graphiques en barres pour visualiser les clients avec les montants restants impayés les plus élevés.
    plt.figure(figsize=(10, 10))
    top_10_client_restt_impayes.plot(kind='bar', color='tomato')
    plt.title('Top 10 Clients avec Montants Restants Impayés', fontsize=14)
    plt.xlabel('Client', fontsize=14)
    plt.ylabel('Montant Restant Impayé (€)', fontsize=14)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Assurer une bonne disposition des éléments du graphique.
    plt.show()

# montants_restants_soldes_a_zero(data_cpy)

"""
6 - Analyse des heures de pointe et des lieux les plus performants :
    Analyser les lieux les plus performants en groupant les transactions par restaurant (Restaurant) et en calculant les revenus totaux (Montant_Rgl).
    Identifier les heures de pointe en groupant les données par Heure_Règlement (heure).
    Créer des graphiques en barres pour visualiser les restaurants les plus performants par chiffre d'affaires et les heures de pointe des transactions.
"""

def plus_performants(data_cpy):
    """ 
    1 - Convertir la colonne Montant_Rgl en type numérique si ce n'est pas déjà fait. 
    Ensuite, grouper les données par restaurant pour calculer le chiffre d'affaires total de chaque restaurant.
    """
    data_cpy['Montant_Rgl'] = pd.to_numeric(data_cpy['Montant_Rgl'], errors='coerce')
    lieux_plus_performants = data_cpy.groupby('Restaurant')['Montant_Rgl'].sum().sort_values(ascending=False)
    top_10_lieux_plus_performants = lieux_plus_performants.head(10)  # Sélectionner les 10 restaurants les plus performants

    """
    2 - Convertir la colonne Heure_Règlement en format datetime et extraire l'heure.
    Ensuite, grouper les données par heure pour analyser les heures de pointe des transactions.
    """
    data_cpy['Heure_Règlement'] = pd.to_datetime(data_cpy['Heure_Règlement'], errors='coerce').dt.hour
    heures_pointe_transactions = data_cpy.groupby('Heure_Règlement')['Montant_Rgl'].sum().sort_values(ascending=False)
    heures_pointe_transactions = heures_pointe_transactions.head(10)  # Sélectionner les 10 heures de pointe avec le plus de transactions
    print(heures_pointe_transactions)  # Afficher les heures avec le plus de transactions

    # Créer un graphique en barres pour les 10 restaurants les plus performants
    plt.figure(figsize=(12, 10))
    top_10_lieux_plus_performants.plot(kind='bar', color='darkblue')
    plt.title('Top 10 Restaurants par Chiffre d\'Affaires', fontsize=14)
    plt.xlabel('Restaurant', fontsize=14)
    plt.ylabel('Chiffre d\'Affaires Total (€)', fontsize=14)
    plt.tight_layout()  # Assurer la bonne disposition des éléments graphiques
    plt.show()

    # Créer un graphique en barres pour les heures de pointe des transactions
    plt.figure(figsize=(10, 10))
    heures_pointe_transactions.plot(kind='bar', color='darkgreen')
    plt.title('Heures de Pointe des Transactions', fontsize=14)
    plt.xlabel('Heure de la Journée', fontsize=14)
    plt.ylabel('Nombre de Transactions', fontsize=14)
    plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des x pour plus de lisibilité
    plt.tight_layout()  # Assurer une disposition correcte
    plt.show()

# plus_performants(data_cpy)

"""
7 - Détection des anomalies (outliers) :
    Détecter les anomalies dans les montants des transactions (Montant_Rgl) en utilisant la méthode de l'écart interquartile (IQR).
    Grouper les anomalies par client, restaurant et heure de la journée pour identifier les motifs.
    Créer des graphiques (scatter plots et graphiques en barres) pour mettre en évidence les clients, les restaurants et les moments de la journée avec le plus d'anomalies.
"""

def function_anomalies(data_cpy):
    """ 
    1 - Calculer l'écart interquartile (IQR) pour détecter les anomalies dans les montants des transactions.
    Une anomalie est définie comme une transaction en dehors des limites inférieure et supérieure définies par IQR.
    """
    data_cpy['Montant_Rgl'] = pd.to_numeric(data_cpy['Montant_Rgl'], errors='coerce')
    Q1 = data_cpy['Montant_Rgl'].quantile(0.25)  # Premier quartile (25%)
    Q3 = data_cpy['Montant_Rgl'].quantile(0.75)  # Troisième quartile (75%)
    IQR = Q3 - Q1  # Calcul de l'écart interquartile
    limite_inferieure = Q1 - 1.5 * IQR  # Limite inférieure pour détecter les outliers
    limite_superieure = Q3 + 1.5 * IQR  # Limite supérieure pour détecter les outliers
    anomaliees = data_cpy[(data_cpy['Montant_Rgl'] < limite_inferieure) | (data_cpy['Montant_Rgl'] > limite_superieure)]  # Transactions anormales
    print("Anomalies détectées :\n", anomaliees.head())

    """
    2 - Grouper les anomalies par client, restaurant et heure de la journée pour identifier les motifs.
    """
    data_cpy['Heure_Règlement'] = pd.to_datetime(data_cpy['Heure_Règlement'], format='%H:%M:%S', errors='coerce')
    anomaliees_client = anomaliees.groupby('Bénéficiaire_CPP').size().sort_values(ascending=False)
    anomaliees_restaurant = anomaliees.groupby('Restaurant').size().sort_values(ascending=False)
    anomaliees_heure = anomaliees.groupby('Heure_Règlement').size().sort_values(ascending=False)
    print(anomaliees_client)  # Afficher les anomalies par client
    print(anomaliees_restaurant)  # Afficher les anomalies par restaurant
    print(anomaliees_heure)  # Afficher les anomalies par heure

    """
    3 - Visualiser les anomalies à l'aide de graphiques.
    """
    # Créer un scatter plot pour visualiser les anomalies dans Montant_Rgl
    plt.figure(figsize=(10, 6))
    plt.scatter(data_cpy.index, data_cpy['Montant_Rgl'], color='lightblue', label='Transactions Normales')
    plt.scatter(anomaliees.index, anomaliees['Montant_Rgl'], color='red', label='Anomalies')
    plt.title('Détection des Anomalies dans les Montants des Transactions', fontsize=14)
    plt.xlabel('Index de Transaction', fontsize=12)
    plt.ylabel('Montant des Transactions (€)', fontsize=12)
    plt.legend()  # Ajouter une légende pour identifier les anomalies
    plt.show()

    # Créer un graphique en barres pour les 10 clients avec le plus d'anomalies
    plt.figure(figsize=(10, 6))
    anomaliees_client.head(10).plot(kind='bar', color='darkblue')
    plt.title('Top 10 Clients avec le Plus d\'Anomalies', fontsize=14)
    plt.xlabel('Client', fontsize=12)
    plt.ylabel('Nombre d\'Anomalies', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Créer un graphique en barres pour les 10 restaurants avec le plus d'anomalies
    plt.figure(figsize=(10, 6))
    anomaliees_restaurant.head(10).plot(kind='bar', color='darkgreen')
    plt.title('Top 10 Restaurants avec le Plus d\'Anomalies', fontsize=14)
    plt.xlabel('Restaurant', fontsize=12)
    plt.ylabel('Nombre d\'Anomalies', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Créer un graphique en barres pour les heures avec le plus d'anomalies
    plt.figure(figsize=(10, 6))
    anomaliees_heure.head(10).plot(kind='bar', color='darkorange')
    plt.title('Heures avec le Plus d\'Anomalies dans les Transactions', fontsize=14)
    plt.xlabel('Heure de la Journée', fontsize=12)
    plt.ylabel('Nombre d\'Anomalies', fontsize=12)
    plt.tight_layout()
    plt.show()

# function_anomalies(data_cpy)

"""
8 - Analyse des performances des caissiers :
    Grouper les données par caissier (Prenom User) pour analyser le montant total traité et le nombre de transactions effectuées.
    Créer des graphiques en barres pour visualiser les performances des caissiers en fonction du montant total traité et du nombre de transactions.
"""

def performances_caissiers(data_cpy):
    """ 
    1 - Convertir la colonne 'Montant_Rgl' en type numérique si ce n'est pas déjà fait.
    Ensuite, grouper les données par caissier (Prenom User) pour calculer le montant total traité 
    et le nombre de transactions effectuées par chaque caissier.
    """
    data_cpy['Montant_Rgl'] = pd.to_numeric(data_cpy['Montant_Rgl'], errors='coerce')  # Convertir Montant_Rgl en type numérique
    cashier_performance = data_cpy.groupby('Prenom User').agg(
        Total_Processed=('Montant_Rgl', 'sum'),  # Calculer le montant total traité par chaque caissier
        Transaction_Count=('Montant_Rgl', 'size')  # Calculer le nombre total de transactions par caissier
    ).sort_values(by='Total_Processed', ascending=False)  # Trier les caissiers par montant total traité
    print(cashier_performance.head())  # Afficher les performances des premiers caissiers

    """ 
    2 - Créer un graphique en barres pour les 10 caissiers ayant traité le plus de montants.
    """
    plt.figure(figsize=(10, 6))
    cashier_performance['Total_Processed'].head(10).plot(kind='bar', color='darkblue')  # Top 10 des caissiers par montant traité
    plt.title('Top 10 Caissiers par Montant Total Traité', fontsize=14)
    plt.xlabel('Caissier', fontsize=12)
    plt.ylabel('Montant Total Traité (€)', fontsize=12)
    plt.xticks(rotation=45)  # Rotation des étiquettes pour une meilleure lisibilité
    plt.tight_layout()  # Assurer une bonne disposition des éléments graphiques
    plt.show()

    """ 
    3 - Créer un graphique en barres pour les 10 caissiers ayant effectué le plus de transactions.
    """
    plt.figure(figsize=(10, 6))
    cashier_performance['Transaction_Count'].head(10).plot(kind='bar', color='darkgreen')  # Top 10 des caissiers par nombre de transactions
    plt.title('Top 10 Caissiers par Nombre de Transactions', fontsize=14)
    plt.xlabel('Caissier', fontsize=12)
    plt.ylabel('Nombre de Transactions', fontsize=12)
    plt.xticks(rotation=45)  # Rotation des étiquettes pour une meilleure lisibilité
    plt.tight_layout()  # Assurer une bonne disposition des éléments graphiques
    plt.show()

# performances_caissiers(data_cpy)

"""
9 - Analyse de la corrélation :
    Analyser la relation entre le solde des cartes prépayées et les dépenses des clients en utilisant des corrélations et des scatter plots.
    Calculer la corrélation entre le solde des cartes prépayées (Solde_CPP) et les dépenses totales (Montant_Rgl) pour chaque client.
"""

def correlation(data_cpy):
    """
    1 - Convertir les colonnes 'Montant_Rgl' et 'Solde_CPP' en types numériques si ce n'est pas déjà fait.
    """
    data_cpy['Montant_Rgl'] = pd.to_numeric(data_cpy['Montant_Rgl'], errors='coerce')  # Conversion en type numérique
    data_cpy['Solde_CPP'] = pd.to_numeric(data_cpy['Solde_CPP'], errors='coerce')  # Conversion en type numérique

    """
    2 - Grouper les données par client (Prenom User) pour calculer les dépenses totales et le solde moyen des cartes prépayées de chaque client.
    """
    client_correlation_data = data_cpy.groupby('Prenom User').agg(
        Total_Expenses=('Montant_Rgl', 'sum'),  # Dépenses totales par client
        Avg_Balance=('Solde_CPP', 'mean')  # Solde moyen des cartes prépayées par client
    )
    print(client_correlation_data.head())  # Afficher les premières lignes des données groupées

    """
    3 - Calculer la corrélation entre les dépenses totales des clients et le solde moyen des cartes prépayées.
    """
    correlation = client_correlation_data['Total_Expenses'].corr(client_correlation_data['Avg_Balance'])  # Calcul de la corrélation
    print(f"Corrélation entre le solde des cartes prépayées et les dépenses totales des clients : {correlation}")

    """
    4 - Créer un scatter plot pour visualiser la relation entre les dépenses totales et le solde moyen des cartes prépayées.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(client_correlation_data['Total_Expenses'], client_correlation_data['Avg_Balance'], color='steelblue')  # Créer un scatter plot

    plt.title('Corrélation entre le Solde des Cartes Prépayées et les Dépenses des Clients', fontsize=14)
    plt.xlabel('Dépenses Totales des Clients (€)', fontsize=12)
    plt.ylabel('Solde Moyen des Cartes Prépayées (€)', fontsize=12)
    plt.tight_layout()  # Assurer une disposition correcte des éléments graphiques
    plt.show()

# correlation(data_cpy)
