import ConfigParser
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
import pymysql
pymysql.install_as_MySQLdb()


application = Flask(__name__)

# Read config file
config = ConfigParser.ConfigParser()
config.read('immob_db.conf')

#MySQL configurations
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + config.get('DB', 'user') + \
                                     ':' + config.get('DB', 'password') + '@' + \
                                     config.get('DB', 'host') + '/' + config.get('DB', 'db')

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

pymysql = SQLAlchemy()
pymysql.init_app(application)

@application.route("/")
def hello():
  return "Hello World!"


class Biens_immo(pymysql.Model):
    __tablename__ = 'biens_immo'
    id = pymysql.Column(pymysql.Integer, primary_key=True)
    nom = pymysql.Column(pymysql.String(128), nullable=False)
    description = pymysql.Column(pymysql.String(128), nullable=False)
    type_de_bien = pymysql.Column(pymysql.String(128), nullable=False)
    ville = pymysql.Column(pymysql.String(128), nullable=False)
    pieces = pymysql.Column(pymysql.Integer, nullable=False)
    carac_pieces = pymysql.Column(pymysql.String(128), nullable=False)
    proprietaire = pymysql.Column(pymysql.String(128), nullable=False)


    def __repr__(self):
        return '<Biens_immo (%s, %s, %s, %s, %i, %s, %s) >' \
               % ("Eric","appart ancien 17eme 100m2" , "appartement", "Paris", 3, "Spatieuses et parquet","Erico")
              #(self.nom, self.description, self.type_de_bien, self.ville, self.pieces, self.carac_pieces,
              # self.proprietaire)


class Users(pymysql.Model):
    __tablename__ = 'users'
    id = pymysql.Column(pymysql.Integer, primary_key=True)
    nom = pymysql.Column(pymysql.String(128), nullable=False)
    prenom = pymysql.Column(pymysql.String(128), nullable=False)
    date_naissance = pymysql.Column(pymysql.Date, nullable=False)


    def __repr__(self):
        return '<Users (%i, %s, %d) >' % (self.nom, self.prenom, self.date_naissance)


@application.route('/bien/create', methods=['POST'])
def createBien():

    # fetch nom, description, type_de_bien, ville, pieces, carac_pieces, proprietaire from the request

    nom = request.get_json(silent=True)["nom"]
    description = request.get_json(silent=True)["description"]
    type_de_bien = request.get_json(silent=True)["type_de_bien"]
    ville = request.get_json(silent=True)["ville"]
    pieces = request.get_json(silent=True)["pieces"]
    carac_pieces = request.get_json(silent=True)["carac_pieces"]
    proprietaire = request.get_json(silent=True)["proprietaire"]

    bien = Biens_immo(nom=nom, description=description, type_de_bien=type_de_bien, ville=ville, pieces=pieces,
                      carac_pieces=carac_pieces, proprietaire=proprietaire) #prepare query statement

    #bien = Biens_immo(nom=nom, description="Grand appart", type_de_bien="Appartement", ville="Paris", pieces="3",
                   #carac_pieces="Grandes", proprietaire="Ali Azzouz") #prepare query statement

    curr_session = pymysql.session #open database session
    try:
       curr_session.add(bien) #add prepared statment to opened session
       curr_session.commit() #commit changes
       print(bien)
    except:
       curr_session.rollback()
       curr_session.flush() # for resetting non-commited .add()

    bienId = bien.id #fetch last inserted id
    data = Biens_immo.query.filter_by(id=bienId).first() #fetch our inserted product

    config.read('immob_db.conf')

    result = [data.nom, data.description, data.type_de_bien, data.ville, data.pieces, data.carac_pieces,
             data.proprietaire] #prepare visual data

    return jsonify(session=result)



@application.route('/bien', methods=['GET'])
def getBien():
    data = Biens_immo.query.all() #fetch all biens on the table

    data_all = []

    for bien in data:
        data_all.append([bien.id, bien.nom, bien.description, bien.type_de_bien, bien.ville, bien.pieces,
                         bien.carac_pieces, bien.proprietaire]) #prepare visual data

    return jsonify(biens=data_all)

@application.route('/bien/<string:strVille>', methods=['GET'])
def getBienVille(strVille):
    data = Biens_immo.query.filter_by(ville=strVille).all()

    data_all = []

    for bien in data:
        data_all.append([bien.id, bien.nom, bien.description, bien.type_de_bien, bien.ville, bien.pieces,
                         bien.carac_pieces, bien.proprietaire]) #prepare visual data

    return jsonify(biens=data_all)

@application.route('/bien/update/<int:bienId>/<string:attribute>', methods=['PATCH'])
def updateBien(bienId, attribute):
    if attribute == "nom":
        nom = request.get_json()["nom"] #fetch rate
    if attribute == "description":
        description = request.get_json(silent=True)["description"]
    if attribute == "type_de_bien":
        type_de_bien = request.get_json(silent=True)["type_de_bien"]
    if attribute == "ville":
        ville = request.get_json(silent=True)["ville"]
    if attribute == "pieces":
        pieces = request.get_json(silent=True)["pieces"]
    if attribute == "carac_pieces":
        carac_pieces = request.get_json(silent=True)["carac_pieces"]
    if attribute == "proprietaire":
        proprietaire = request.get_json(silent=True)["proprietaire"]

    curr_session = pymysql.session

    try:
        bien = Biens_immo.query.filter_by(id=bienId).first() #fetch the product do be updated
        if attribute == "nom":
            bien.nom = nom #update the column nom with the info fetched from the request
        if attribute == "description":
            bien.description = description
        if attribute == "type_de_bien":
            bien.type_de_bien = type_de_bien
        if attribute == "ville":
            bien.ville = ville
        if attribute == "pieces":
            bien.pieces = pieces
        if attribute == "carac_pieces":
            bien.carac_pieces = carac_pieces
        if attribute == "proprietaire":
            bien.proprietaire = proprietaire

        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush()

    config.read('immob_db.conf')

    result = [bien.nom, bien.description, bien.type_de_bien, bien.ville, bien.pieces, bien.carac_pieces,
              bien.proprietaire] #prepare visual data

    return jsonify(session=result)


@application.route('/bien/delete/<int:bienId>', methods=['DELETE'])
def deleteBien(bienId):

    curr_session = pymysql.session #initiate database session

    Biens_immo.query.filter_by(id=bienId).delete() #find the product by bienId and deletes it
    curr_session.commit() #commit changes to the database

    return getBien() #return all create products


@application.route('/user/create', methods=['POST'])
def createUser():

    nom = request.get_json(silent=True)["nom"]
    prenom = request.get_json(silent=True)["prenom"]
    date_naissance = request.get_json(silent=True)["date_naissance"]

    user = Users(nom=nom, prenom=prenom, date_naissance=date_naissance)#prepare query statement

    curr_session = pymysql.session #open database session
    try:
       curr_session.add(user) #add prepared statment to opened session
       curr_session.commit() #commit changes
       print(user)
    except:
       curr_session.rollback()
       curr_session.flush() # for resetting non-commited .add()

    userId = user.id #fetch last inserted id
    data = Users.query.filter_by(id=userId).first() #fetch our inserted product


    config.read('immob_db.conf')

    result = [data.nom, data.prenom, data.date_naissance] #prepare visual data

    return jsonify(session=result)


@application.route('/user/update/<int:userId>/<string:attribute>', methods=['PATCH'])
def updateUser(userId, attribute):
    if attribute == "nom":
        nom = request.get_json()["nom"] #fetch rate
    if attribute == "prenom":
        prenom = request.get_json(silent=True)["prenom"]
    if attribute == "date_naissance":
        date_naissance = request.get_json(silent=True)["date_naissance"]

    curr_session = pymysql.session

    try:
        user = Users.query.filter_by(id=userId).first() #fetch the product do be updated
        if attribute == "nom":
            user.nom = nom #update the column nom with the info fetched from the request
        if attribute == "prenom":
            user.prenom = prenom
        if attribute == "date_naissance":
            user.date_naissance = date_naissance

        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush()

    config.read('immob_db.conf')

    result = [user.nom, user.prenom, user.date_naissance] #prepare visual data

    return jsonify(session=result)


if __name__ == "__main__":
    application.run()