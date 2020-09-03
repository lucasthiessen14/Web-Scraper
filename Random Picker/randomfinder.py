#import required libraries
import random
import pygame
import requests
import sys
from bs4 import BeautifulSoup

#initialize pygame
pygame.init()

#set the screen size
width = 700
height = 394
screen = pygame.display.set_mode((width,height))

#Top Movies
movie_url = 'https://www.imdb.com/chart/top/'

#Top Tv
tv_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'

#import required photos
pygame.display.set_caption("Random Finder")
background = pygame.image.load(".\\images\\randombackground.jpg")
background2 = pygame.image.load(".\\images\\background2.jpg")

#set required fonts
myFont2 = pygame.font.SysFont("Mitga",100)
myFont = pygame.font.SysFont("Mitga",60)
myFont3 = pygame.font.SysFont("Mitga",35)
myFont4 = pygame.font.SysFont("Mitga",25)

#function to create a button on the screen
def botton(a,b,c,d, color1, color2):
    mouse = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, (color1), (a, b, c, d))
    if a+c > mouse[0] > a and b+d > mouse[1] > b:
        pygame.draw.rect(screen, (color2), (a, b, c, d), 2)
        if clicked[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, (color1), (a, b, c, d), 2)

#function to print the movie or tv show that was picked
def print_name(item, item2, item3, x, y):
    a = item
    b = item2
    c = item3
    print = True
    while print:

        #sets what the screen is going to look like
        screen.blit(background2, (0,0))
        text = myFont3.render("Press enter for another option", 1, (255,255,255))
        text2 = myFont3.render("Press escape for main menu", 1, (255,255,255))
        screen.blit(text, (180,300))
        screen.blit(text2, (190,350))

        for event in pygame.event.get():

            #Exits the game when the game window is closed
            if event.type == pygame.QUIT:
                sys.exit()

        #registers when different keys are pushed
        if event.type == pygame.KEYDOWN:

            #returns a new movie or tv show when pressed
            if event.key == pygame.K_RETURN:
                main(x,y)

            #returns to main menu is escape key is pressed
            if event.key == pygame.K_ESCAPE:
                mainmenu()

        screen.blit(a, (5, 15))
        screen.blit(b, (0, 55))
        screen.blit(c, (0, 100))
        pygame.display.update()

#function to create the main menu
def mainmenu():
    menu = True
    while menu:

        #create what the main menu looks like
        screen.blit(background, (0,0))
        title = myFont2.render("Random Finder", 1, (255,255,255))
        botton1 = myFont.render("Movie", 1, (0,0,0))
        botton2 = myFont.render("Tv", 1, (0,0,0))
        screen.blit(title, (90, 100))
        pygame.draw.rect(screen, (255,50,50), (355, 200, 200, 50))
        pygame.draw.rect(screen, (255,50,50), (145, 200, 200, 50))

        for event in pygame.event.get():

            #Exits the game when the game window is closed
            if event.type == pygame.QUIT:
                sys.exit()

        #creates a botton on the screen
        if botton(355,200,200,50,(255,50,50),(0,0,0)):
            main(True, False)

        #creates a botton on the screen
        if botton(145,200,200,50,(255,50,50),(0,0,0)):
            main(False, True)

        screen.blit(botton1, (390, 205))
        screen.blit(botton2, (220, 205))

        pygame.display.update()

#scrapes the web for the top 250 movies and tv shows
def main(x,y):

    if x:
        URL = movie_url

    if y:
        URL = tv_url

    #gets the website information
    response = requests.get(URL)
    #cleans up the website code to make it easier for the program
    soup = BeautifulSoup(response.text, 'html.parser')

    #selects the sections needed from the website info
    movies = soup.select('td.titleColumn')
    in_movie = soup.select('td.titleColumn a')
    ratings = soup.select('td.posterColumn span[name=ir]')

    def get_year(movie_tag):
        moviesplit = movie_tag.text.split()
        year = moviesplit[-1] # last item
        return year

    #gets the different information that is going to be displayed
    year = [get_year(tag) for tag in movies]
    actors_list =[tag['title'] for tag in in_movie]
    titles = [tag.text for tag in in_movie]
    rating = [float(tag['data-value']) for tag in ratings]

    #gets the total number of movies
    num_movies = len(titles)

    while(True):

        #randomly picks a movie or tv show from the website
        a = random.randrange(0, num_movies)
        result = myFont3.render(f'{titles[a]} {year[a]}', 1, (0,0,0))
        result2 = myFont3.render(f' Rating: {rating[a]:.1f}', 1, (0,0,0))
        result3 = myFont4.render(f' Starring: {actors_list[a]}', 1, (0,0,0))
        print_name(result, result2, result3, x, y)

#calls the functions
mainmenu()
main()
print_name()
