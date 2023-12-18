import pygame
import time
import string
import math as m

pygame.init()
screen = pygame.display.set_mode((720,720))
clock = pygame.time.Clock()
running = True

def draw_background():
    screen.fill("white")

    White_colour = ("#DAC0A7")
    Black_colour = ("#532915")

    #White_colour = ("#FFFFFF")
    #Black_colour = ("#000000")

    Colours = [White_colour, Black_colour]

    start_x = 40
    x = 40
    y = 40
    colour = 0

    while y <= 620:
        if x > 620:
            x = start_x
            y += 80
            if colour == 1:
                colour = 0
            else:
                colour = 1
        else:
            pygame.draw.rect(screen, Colours[colour], pygame.Rect(x,y,80,80))
            x += 80
            if colour == 1:
                colour = 0
            else:
                colour = 1

def init():
    global turn 
    
    turn = "White"

    global all_pieces_list
    global en_passant_list

    draw_background()

    piecesList = [
    ("pawn", "A7", False, "Black"),
    ("pawn", "B7", False, "Black"),
    ("pawn", "C7", False, "Black"),
    ("pawn", "D7", False, "Black"),
    ("pawn", "E7", False, "Black"),
    ("pawn", "F7", False, "Black"),
    ("pawn", "G7", False, "Black"),
    ("pawn", "H7", False, "Black"),
    ("rook", "A8", False, "Black"),
    ("rook", "H8", False, "Black"),
    ("knight", "B8", False, "Black"),
    ("knight", "G8", False, "Black"),
    ("bishop", "C8", False, "Black"),
    ("bishop", "F8", False, "Black"),
    ("queen", "D8", False, "Black"),
    ("king", "E8", False, "Black"),
    ("pawn", "A2", False, "White"),
    ("pawn", "B2", False, "White"),
    ("pawn", "C2", False, "White"),
    ("pawn", "D2", False, "White"),
    ("pawn", "E2", False, "White"),
    ("pawn", "F2", False, "White"),
    ("pawn", "G2", False, "White"),
    ("pawn", "H2", False, "White"),
    ("rook", "A1", False, "White"),
    ("rook", "H1", False, "White"),
    ("knight", "B1", False, "White"),
    ("knight", "G1", False, "White"),
    ("bishop", "C1", False, "White"),
    ("bishop", "F1", False, "White"),
    ("queen", "D1", False, "White"),
    ("king", "E1", False, "White")
    ]

    all_pieces_list = pygame.sprite.Group()
    en_passant_list = pygame.sprite.Group()

    for x in piecesList:
        if x[0] == "pawn":
            all_pieces_list.add(pawn(x[1], x[2], x[3]))
        elif x[0] == "rook":
            all_pieces_list.add(rook(x[1], x[2], x[3]))
        elif x[0] == "knight":
            all_pieces_list.add(knight(x[1], x[2], x[3]))
        elif x[0] == "bishop":
            all_pieces_list.add(bishop(x[1], x[2], x[3]))
        elif x[0] == "queen":
            all_pieces_list.add(queen(x[1], x[2], x[3]))
        elif x[0] == "king":
            all_pieces_list.add(king(x[1], x[2], x[3]))
        else:
            raise ValueError("That piece is not valid, maybe try lower case?")

class enPawn(pygame.sprite.Sprite):
    def __init__(self, square, colour):
        self.square = square
        self.colour = colour
        pygame.sprite.Sprite.__init__(self)

        if self.colour == "Black":
            colour = "Dark"
        elif self.colour == "White":
            colour = "Light"

        self.image = pygame.image.load(colour + "Pawn.webp")

        self.new_image = self.image.copy()

        alpha = 10
        
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        self.image = pygame.transform.scale(self.image, (80, 80))

        self.GetCoords()

    def GetCoords(self):
        try:
            Xval = string.ascii_lowercase.index(self.square[0])
        except ValueError:
            try:
                Xval = string.ascii_uppercase.index(self.square[0])
            except ValueError:
                raise ValueError("The coordinate does not appear to be valid")
        if Xval <= 7:
            self.xcoord = 40 + (Xval) * 80
        else:
            raise ValueError("The coordinate does not appear to be valid")
        try:
            Yval = int(self.square[1])
            if Yval <= 8:
                self.ycoord = 720 - (40 + (Yval) * 80)
        except:
            raise ValueError("The coordinate does not appear to be valid")

        self.rect = self.image.get_rect(topleft = (self.xcoord,self.ycoord))

        return self.xcoord, self.ycoord

    def on_mouseclick(self):
        return self.square

class pieces(pygame.sprite.Sprite):
    def __init__(self, square, moved, colour, piece):
        self.square = square
        self.moved = moved
        self.colour = colour
        self.piece = piece
        pygame.sprite.Sprite.__init__(self)

        if self.colour == "Black":
            colour = "Dark"
        elif self.colour == "White":
            colour = "Light"
        else:
            raise ValueError("The colour of this piece is not valid")

        self.image = pygame.image.load(colour + piece + ".webp")

        self.image = pygame.transform.scale(self.image, (80, 80))

        self.GetCoords()

    def GetCoords(self):
        try:
            Xval = string.ascii_lowercase.index(self.square[0])
        except ValueError:
            try:
                Xval = string.ascii_uppercase.index(self.square[0])
            except ValueError:
                raise ValueError("The coordinate does not appear to be valid")
        if Xval <= 7:
            self.xcoord = 40 + (Xval) * 80
        else:
            raise ValueError("The coordinate does not appear to be valid")
        try:
            Yval = int(self.square[1])
            if Yval <= 8:
                self.ycoord = 720 - (40 + (Yval) * 80)
        except:
            raise ValueError("The coordinate does not appear to be valid")

        self.rect = self.image.get_rect(topleft = (self.xcoord,self.ycoord))

        return self.xcoord, self.ycoord

    def on_mouseclick(self):
        return self.square

    def UpdateSquare(self, newSquare):
        global turn

        if (self.piece == "Pawn" and (newSquare[1] == str(8) or newSquare[1] == str(1))):
            all_pieces_list.add(queen(newSquare, True, self.colour))
            self.kill()

        else:
            self.square = newSquare
            self.moved = True
            self.GetCoords()
        
        if turn == "White":
            for x in en_passant_list:
                if x.colour == "Black":
                    x.kill()
            turn = "Black"
        else:
            for x in en_passant_list:
                if x.colour == "White":
                    x.kill()
            turn = "White"

    def ValidOrthogonalMove(self, newSquare):
        valid = True

        Xcoord = string.ascii_uppercase.index(self.square[0])
        Ycoord = int(self.square[1])

        horizontal = string.ascii_uppercase.index(newSquare[0]) - Xcoord
        vertical = int(newSquare[1]) - Ycoord

        if horizontal != abs(horizontal):
            A = -1
        else:
            A = 1
        if vertical != abs(vertical):
            B = -1
        else:
            B = 1

        horizontal = abs(horizontal)
        vertical = abs(vertical)

        if horizontal * vertical != 0 or (horizontal == 0 and vertical == 0):
            valid = False

        if horizontal != 0 and valid == True:
            h = range(horizontal)
            for dist in h[1::]:
                for x in all_pieces_list:
                    if (string.ascii_uppercase[A*dist+Xcoord]+self.square[1] == x.on_mouseclick()):
                        valid = False 
            for x in all_pieces_list:
                if (newSquare == x.on_mouseclick() and x.colour != self.colour):
                    captured = x
                if (string.ascii_uppercase[A*horizontal+Xcoord]+self.square[1] == x.on_mouseclick() and x.colour == self.colour):
                    valid = False

        elif vertical != 0 and valid == True:
            v = range(vertical)
            for dist in v[1::]:
                for x in all_pieces_list:
                    if (self.square[0]+str(B*dist+Ycoord) == x.on_mouseclick()):
                        valid = False
            for x in all_pieces_list:
                if (newSquare == x.on_mouseclick() and x.colour != self.colour):
                    captured = x
                if (self.square[0]+str(B*vertical+Ycoord) == x.on_mouseclick() and x.colour == self.colour):
                    valid = False

        if valid == True:
            self.UpdateSquare(newSquare)
            try:
                captured.kill()
            except UnboundLocalError:
                pass 

            return valid 

    def ValidDiagonalMove(self, newSquare):
        valid = True

        Xcoord = string.ascii_uppercase.index(self.square[0])
        Ycoord = int(self.square[1])

        horizontal = string.ascii_uppercase.index(newSquare[0]) - Xcoord
        vertical = int(newSquare[1]) - Ycoord

        if horizontal != abs(horizontal):
            A = -1
        else:
            A = 1
        if vertical != abs(vertical):
            B = -1
        else:
            B = 1

        if abs(horizontal) != abs(vertical):
            valid = False

        else:
            h = range(abs(horizontal))
            v = range(abs(vertical))

            for hdist, vdist in zip(h[1::], v[1::]):
                for x in all_pieces_list:
                    if (string.ascii_uppercase[A*hdist+Xcoord]+str(B*vdist+Ycoord) == x.on_mouseclick()):
                        valid = False
            
            for x in all_pieces_list:
                if (newSquare == x.on_mouseclick() and x.colour != self.colour):
                    captured = x
                if (string.ascii_uppercase[horizontal+Xcoord]+str(vertical+Ycoord) == x.on_mouseclick() and x.colour == self.colour):
                    valid = False

        if valid == True:
            self.UpdateSquare(newSquare)
            try:
                captured.kill()
            except UnboundLocalError:
                pass  

            return valid

class pawn(pieces):
    def __init__(self, square, moved, colour):
        super().__init__(square, moved, colour, "Pawn")

    def ValidMove(self, newSquare):
        valid = True
        if self.colour == "Black":
            A = -1
        elif self.colour == "White":
            A = 1

        enSquare = newSquare[0]+str(int(newSquare[1])-A)

        attemptedCapture = (string.ascii_uppercase.index(newSquare[0]) - string.ascii_uppercase.index(self.square[0]))**2

        if attemptedCapture == 0:
            pass
        elif attemptedCapture == 1:
            capture = False
            for x in all_pieces_list:
                if (newSquare == x.on_mouseclick() and x.colour != self.colour):
                    capture = True
                    captured = x
            for x in en_passant_list:
                if (newSquare == x.on_mouseclick() and x.colour != self.colour):
                    capture = True
                    enCapSquare = newSquare[0]+str(int(newSquare[1])-A)
                    for x in all_pieces_list:
                        if enCapSquare == x.on_mouseclick():
                            captured = x
            valid = (capture == True)
        else:
            valid = False

        distance = int(newSquare[1]) - int(self.square[1])

        if (self.moved == False and (A*distance) == 2):
            enSquare = newSquare[0]+str(int(newSquare[1])-A)
            for x in all_pieces_list:
                tgt = x.on_mouseclick()
                if newSquare == tgt:
                    valid = False
                elif enSquare == tgt:
                    valid = False
                en_passant_list.add(enPawn(enSquare, self.colour))         

        elif ((A*distance == 1) and (attemptedCapture == 0)):
            for x in all_pieces_list:
                if newSquare == x.on_mouseclick():
                    valid = False

        elif (A*distance > 2 or A*distance <= 0):
            valid = False

        else:
            pass

        if valid == True:
            self.UpdateSquare(newSquare)
            try:
                captured.kill()                
            except UnboundLocalError:
                pass

class rook(pieces):
    def __init__(self, square, moved, colour):
        super().__init__(square, moved, colour, "Rook")      

    def ValidMove(self, newSquare):
        self.ValidOrthogonalMove(newSquare)    

class knight(pieces):
    def __init__(self, square, moved, colour):
        super().__init__(square, moved, colour, "Knight")

    def ValidMove(self, newSquare):
        valid = True

        Xcoord = string.ascii_uppercase.index(self.square[0])
        Ycoord = int(self.square[1])

        horizontal = string.ascii_uppercase.index(newSquare[0]) - Xcoord
        vertical = int(newSquare[1]) - Ycoord

        if abs(horizontal)**2 + abs(vertical)**2 != 5:
            valid = False

        for x in all_pieces_list:
            if (newSquare == x.on_mouseclick()):
                if x.colour == self.colour:
                    valid = False
                elif x.colour != self.colour:
                    captured = x  

        if valid == True:
            self.UpdateSquare(newSquare)
            try:
                captured.kill()
            except UnboundLocalError:
                pass        

class bishop(pieces):
    def __init__(self, square, moved, colour):
        super().__init__(square, moved, colour, "Bishop")

    def ValidMove(self, newSquare):
        self.ValidDiagonalMove(newSquare)

class king(pieces):
    def __init__(self, square, moved, colour):
        super().__init__(square, moved, colour, "King") 

    def ValidMove(self, newSquare):
        valid = True

        Xcoord = string.ascii_uppercase.index(self.square[0])
        Ycoord = int(self.square[1])

        horizontal = string.ascii_uppercase.index(newSquare[0]) - Xcoord
        vertical = int(newSquare[1]) - Ycoord

        if (self.moved == False and abs(horizontal) == 2):
            for x in all_pieces_list:
                if (x.colour == self.colour and x.piece == "Rook" and x.moved == False):
                    if (x.square[0] == "H" and horizontal == 2):
                        Rook = x
                        RookSquare = string.ascii_uppercase[5] + x.square[1]
                    elif (x.square[0] == "A" and horizontal == -2):
                        Rook = x
                        RookSquare = string.ascii_uppercase[3] + x.square[1]
                    else:
                        valid == False
            if valid == True:
                try:
                    valid = self.ValidOrthogonalMove(newSquare)
                except UnboundLocalError:
                    valid = False
            if valid == True:
                Rook.UpdateSquare(RookSquare)
                Rook.UpdateSquare(RookSquare)


        if (horizontal**2 + vertical**2) > 2:
            valid = False
        
        else:
            if (horizontal == 0 or vertical == 0):
                self.ValidOrthogonalMove(newSquare)

            elif abs(horizontal) == abs(vertical):
                self.ValidDiagonalMove(newSquare)

            else:
                pass

class queen(pieces):
    def __init__(self, square, moved, colour):
        super().__init__(square, moved, colour, "Queen")

    def ValidMove(self, newSquare):        
        valid = True

        Xcoord = string.ascii_uppercase.index(self.square[0])
        Ycoord = int(self.square[1])

        horizontal = string.ascii_uppercase.index(newSquare[0]) - Xcoord
        vertical = int(newSquare[1]) - Ycoord

        if (horizontal == 0 or vertical == 0):
            self.ValidOrthogonalMove(newSquare)

        elif abs(horizontal) == abs(vertical):
            self.ValidDiagonalMove(newSquare)

        else:
            pass

init() 

piece_selected = False

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            xpos, ypos = pygame.mouse.get_pos()
            xsq = string.ascii_uppercase[m.floor((xpos-40)/80)]
            ysq = 8-m.floor((ypos-40)/80)

            for x in all_pieces_list:
                if ((xsq+str(ysq) == x.on_mouseclick()) and turn == x.colour):
                    selected_piece = x
                    piece_selected = True
                    
        if event.type == pygame.MOUSEBUTTONUP:
            if piece_selected == True:
                xpos, ypos = pygame.mouse.get_pos()
                xsq = string.ascii_uppercase[m.floor((xpos-40)/80)]
                ysq = 8-m.floor((ypos-40)/80)
                
                if (0 < ysq < 9 and 0 <= string.ascii_uppercase.index(xsq) < 8):
                    selected_piece.ValidMove(xsq+str(ysq))
                piece_selected = False
            else:
                pass

    draw_background()
    all_pieces_list.draw(screen)
    en_passant_list.draw(screen)
    

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
