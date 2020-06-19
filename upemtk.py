from tkinter import *
from tkinter import font
import subprocess
import sys

__all__ = ['ignore_exception', 'auto_update', 'cree_fenetre',
           'ferme_fenetre', 'mise_a_jour', 'ligne', 'fleche',
           'polygone', 'rectangle', 'cercle', 'point', 'marque',
           'image', 'texte', 'longueur_texte', 'hauteur_texte',
           'efface_tout', 'efface', 'efface_marque', 'attente_clic',
           'attente_touche', 'attente_clic_ou_touche', 'clic',
           'capture_ecran', 'donne_evenement', 'type_evenement',
           'clic_x', 'clic_y', 'touche', 'TypeEvenementNonValide',
           'FenetreNonCree', 'FenetreDejaCree']

class CustomCanvas:

    def __init__(self, width, height):
        
        self.width = width
        self.height = height
    
        self.root = Tk()
      
        self.canvas = Canvas(self.root, width=width,
                             height=height, highlightthickness=0)
        
        self.root.protocol("WM_DELETE_WINDOW", self.event_quit)
        self.canvas.bind("<Button-1>", self.event_handler_button1)
        right_button = "<Button-3>" 
        if sys.platform.startswith("darwin"):
            right_button = "<Button-2>"
        self.canvas.bind(right_button, self.event_handler_button2)
        self.canvas.bind_all("<Key>", self.event_handler_key)
        self.canvas.bind("<Motion>", self.event_handler_motion)
        self.canvas.pack()
     
        self.eventQueue = []
      
        self.set_font("Purisa", 24)
    
        self.tailleMarque = 5

        self.root.update()

    def set_font(self, _font, size):
        self.tkfont = font.Font(self.canvas, font=(_font, size))
        self.tkfont.height = self.tkfont.metrics("linespace")

    def update(self):
        # sleep(_tkinter.getbusywaitinterval() / 1000)
        self.root.update()

    def event_handler_key(self, event):
        self.eventQueue.append(("Touche", event))

    def event_handler_button2(self, event):
        self.eventQueue.append(("ClicDroit", event))

    def event_handler_button1(self, event):
        self.eventQueue.append(("ClicGauche", event))

    def event_handler_motion(self, event):
        self.eventQueue.append(("Deplacement", event))

    def event_quit(self):
        self.eventQueue.append(("Quitte", ""))


__canevas = None
__img = dict()

class TypeEvenementNonValide(Exception):
    pass


class FenetreNonCree(Exception):
    pass


class FenetreDejaCree(Exception):
    pass


def ignore_exception(function):
    def dec(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            exit(0)
    return dec

def auto_update(function):
    def dec(*args, **kwargs):
        global __canevas
        retval = function(*args, **kwargs)
        __canevas.canvas.update()
        return retval
    return dec

def cree_fenetre(largeur, hauteur):

    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
            'La fenêtre a déjà existe deja "cree_fenetre".')
    __canevas = CustomCanvas(largeur, hauteur)


def ferme_fenetre():

    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'est pas crée avec la fonction \"cree_fenetre\".")
    __canevas.root.destroy()
    __canevas = None


def mise_a_jour():

    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'est pas crée avec la fonction \"cree_fenetre\".")
    __canevas.update()


def ligne(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):

    global __canevas
    return __canevas.canvas.create_line(
        ax, ay, bx, by,
        fill=couleur,
        width=epaisseur,
        tag=tag)


def fleche(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):

    global __canevas
    x, y = (bx - ax, by - ay)
    n = (x**2 + y**2)**.5
    x, y = x/n, y/n    
    points = [bx, by, bx-x*5-2*y, by-5*y+2*x, bx-x*5+2*y, by-5*y-2*x]
    return __canevas.canvas.create_polygon(
        points, 
        fill=couleur, 
        outline=couleur,
        width=epaisseur,
        tag=tag)


def polygone(points, couleur='black', remplissage='', epaisseur=1, tag=''):

    global __canevas
    return __canevas.canvas.create_polygon(
        points, 
        fill=remplissage, 
        outline=couleur,
        width=epaisseur,
        tag=tag)


def rectangle(ax, ay, bx, by,
              couleur='black', remplissage='', epaisseur=1, tag=''):

    global __canevas
    return __canevas.canvas.create_rectangle(
        ax, ay, bx, by,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def cercle(x, y, r, couleur='black', remplissage='', epaisseur=1, tag=''):

    global __canevas
    return __canevas.canvas.create_oval(
        x - r, y - r, x + r, y + r,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def arc(x, y, r, ouverture=90, depart=0, couleur='black', remplissage='',
        epaisseur=1, tag=''):

    global __canevas
    return __canevas.canvas.create_arc(
        x - r, y - r, x + r, y + r,
        extent=ouverture,
        start=init,
        style=ARC,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)



def point(x, y, couleur='black', epaisseur=1, tag=''):

    return ligne(x, y, x + epaisseur, y + epaisseur,
                 couleur, epaisseur, tag)




def marque(x, y, couleur="red"):

    global __canevas
    efface_marque()
    __canevas.marqueh = ligne(
        x - __canevas.tailleMarque, y,
        x + __canevas.tailleMarque, y, couleur, tag='marque')
    __canevas.marquev = ligne(
        x, y - __canevas.tailleMarque,
        x, y + __canevas.tailleMarque, couleur, tag='marque')


# Image

def image(x, y, fichier, ancrage='center', tag=''):

    global __canevas
    global __img
    img = PhotoImage(file=fichier)
    img_object = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=img, tag=tag)
    __img[img_object] = img
    return img_object


# Texte

def texte(x, y, chaine,
          couleur='black', ancrage='nw', police="Purisa", taille=24, tag=''):

    global __canevas
    __canevas.set_font(police, taille)
    return __canevas.canvas.create_text(
        x, y,
        text=chaine, font=__canevas.tkfont, tag=tag,
        fill=couleur, anchor=ancrage)


def longueur_texte(chaine):

    global __canevas
    return __canevas.tkfont.measure(chaine)


def hauteur_texte():

    global __canevas
    return __canevas.tkfont.height


def efface_tout():
    """
    Efface la fenêtre.
    """
    global __canevas
    global __img
    __img.clear()
    __canevas.canvas.delete("all")


def efface(objet):

    global __canevas
    if objet in __img:
        del __img[objet]
    __canevas.canvas.delete(objet)


def efface_marque():

    efface('marque')





def attente_clic():

    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "ClicDroit" or type_ev == "ClicGauche":
            return clic_x(ev), clic_y(ev), type_ev
        mise_a_jour()


def attente_touche():

    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "Touche":
            break
        mise_a_jour()


def attente_clic_ou_touche():

    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if "Clic" in type_ev:
            return clic_x(ev), clic_y(ev), type_ev
        elif type_ev == "Touche":
            return -1, touche(ev), type_ev
        mise_a_jour()


def clic():

    attente_clic()


def capture_ecran(file):

    global __canevas
    __canevas.canvas.postscript(file=file + ".ps", height=__canevas.height,
                                width=__canevas.width, colormode="color")
    subprocess.call(
        "convert -density 150 -geometry 100% -background white -flatten",
        file + ".ps", file + ".png", shell=True)
    subprocess.call("rm", file + ".ps", shell=True)



def donne_evenement():

    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenêtre n'a pas été crée avec la fonction \"cree_fenetre\".")
    if len(__canevas.eventQueue) == 0:
        return "RAS", ""
    else:
        return __canevas.eventQueue.pop()


def type_evenement(evenement):

    nom, ev = evenement
    return nom


def clic_x(evenement):

    nom, ev = evenement
    if not (nom == "ClicDroit" or nom == "ClicGauche" or nom == "Deplacement"):
        raise TypeEvenementNonValide(
            'On ne peut pas utiliser "clic_x" sur un évènement de type', nom)
    return ev.x


def clic_y(evenement):

    nom, ev = evenement
    if not (nom == "ClicDroit" or nom == "ClicGauche" or nom == "Deplacement"):
        raise TypeEvenementNonValide(
            'On ne peut pas utiliser "clic_y" sur un évènement de type', nom)
    return ev.y


def touche(evenement):

    nom, ev = evenement
    if not (nom == "Touche"):
        raise TypeEvenementNonValide(
            'On peut pas utiliser "touche" sur un évènement de type', nom)
    return ev.keysym
