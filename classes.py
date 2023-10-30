# regions of interest of the front of the ID card
class RegionFront():
    class CCCD(object):
        # coordinates are of the form (y, x , h , w )
        ROIS = {
            "surname": [(250, 140, 600, 200)],  # done
            "given_names": [
                (250, 220, 600, 250),
            ],  # done
            "birth_date": [(250, 300, 600, 330)],  # done
            "birth_place": [(250, 350, 600, 380)],  # done
            "sex": [(250, 400, 600, 430)],  # done
            "height":  [(250, 400, 600, 430)],  # done
            "occupation": [(250, 450, 600, 480)],  # done
            "signature": [(250, 450, 550, 700)],
        }
        
        
# regions of interest of the back of the ID card       
class RegionBack():
    class CCCD(object):
        # coordinates are of the form (y, x , h , w )
        ROIS = {
            "father": [(40, 50, 200, 100)],  # done
            "mother": [
                (40, 100, 200, 200),
            ],  # done
            "address": [(40, 250, 200, 350)],  # done
            "identification_post": [(650, 240, 850, 270)],  # done
            "signature": [(250, 200, 550, 400)],
        }