##Ce module a pour but de me fournir un accÃ¨s a des fonctions mathÃ©matiques dont j'ai besoin


#Fonction d'interpolation linÃ©aire. Permet de donner la valeur entre deux points
def lerp(start, end, percentage) :
    return (start + percentage * (end - start));
