# projet-arc
À l'attention de Monsieur Arnaud de Terline

Pour utiliser le micro-service, effectuer les commandes suivantes :

```
virtualenv venv .
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Description des fonctions

### class Biens_immo(pymysql.Model)

Cette classe définit un bien immobilier selon les caractéristiques demandées dans la consigne

### class Users(pymysql.Model)

Cette classe définit un utilisateur selon les caractéristiques demandées dans la consigne

### @application.route('/bien/create', methods=['POST'])

Cette route permet de lancer la fonction createBien qui permet d'entrer un bien dans la base de données.
On peut l'utiliser avec une commande du type :
```
curl -H "Content-Type: application/json" -X POST -d '{"nom":"Paul","description":"Freakout", "type_de_bien":"appart", "ville":"Paris", "pieces":3, "carac_pieces":"spatieuses", "proprietaire":"Paul Ragot"}' http://localhost:5000/bien/create

```

### @application.route('/bien', methods=['GET'])

Cette route permet d'afficher tous les biens de la base de données avec une commande du type :

```
curl -H "Content-Type: application/json" -X GET  http://localhost:5000/bien

``


### @application.route('/bien/<string:strVille>', methods=['GET'])

Cette route permet d'afficher tous les biens d'une ville entrée en paramètre avec une commande du type (mettre la ville voulue à la fin de l'url):

```
curl -H "Content-Type: application/json" -X GET  http://localhost:5000/bien/Paris

```

### @application.route('/bien/update/<int:bienId>/<string:attribute>', methods=['PATCH'])

Cette route permet de mettre à jour les caractéristiques d'un bien avec une commande du type (entrer dans l'accolade la caracteristique à modifier et mettre l'id puis le nom de la caracteristique à changer dans l'url):

```
curl -H "Content-Type: application/json" -X PATCH -d '{"nom":"Henri"}'  http://localhost:5000/bien/update/2/nom

```

### @application.route('/bien/delete/<int:bienId>', methods=['DELETE'])

Cette route permet de supprimer un bien de la base de données avec une commande du type (mettre l'id du bien à supprimer à la fin de l'url):

```
curl -H "Content-Type: application/json" -X DELETE http://localhost:5000/bien/delete/4

``

### @application.route('/user/create', methods=['POST'])

Cette route permet de créer un utilisateur avec une commande de ce type (mettre les infos dans le formulaire dans l'accolade):

```
curl -H "Content-Type: application/json" -X POST -d '{"nom":"Fattal", "prenom":"Eric", "date_naissance":"1995-11-13"}' http://localhost:5000/user/create

```

### @application.route('/user/update/<int:userId>/<string:attribute>', methods=['PATCH'])

Cette route permet de mettre à jour les caractéristiques d'un utilisateur avec une commande du type :

```
curl -H "Content-Type: application/json" -X PATCH -d '{"prenom":"Eric Antoine"}' http://localhost:5000/user/update/1/prenom

``
