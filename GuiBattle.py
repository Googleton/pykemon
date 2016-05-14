import pygame as pg;
import random;
import GuiBase;
import MathUtils;
import GuiTeam;

class GuiBattle(GuiBase.GuiBase) :

    def __init__(self, text, opponent, player):
        GuiBase.GuiBase.__init__(self, 0, 400, 800, 200);
        self.image = pg.image.load("resources/gui/arena_menu.png").convert();
        self.arrow_image = pg.image.load("resources/gui/ge_arrow.png").convert();
        self.player = player;

        #Images joueur et adversaire
        self.player_image = pg.sprite.Sprite();
        self.player_image.image = pg.transform.scale2x(pg.image.load("resources/gui/player_back.png"));
        self.player_image.rect = self.player_image.image.get_rect();
        self.player_image.rect.topleft = (-120, 180)
        self.player_image.image.set_colorkey((255, 0, 228));

        self.opponent_image = pg.sprite.Sprite();
        self.opponent_image.image = pg.transform.scale2x(pg.image.load("resources/gui/trainers/"+opponent.trainerTex));
        self.opponent_image.rect = self.opponent_image.image.get_rect();
        self.opponent_image.rect.topleft = (880, 80)
        self.opponent_image.image.set_colorkey((112, 192, 160));

        #Status
        self.showStatus = False;

        self.status_opponent = pg.transform.scale2x(pg.image.load("resources/gui/opponent_status.png"));
        self.status_opponent_text = ["Pokemon", "Level"];
        self.status_opponent_text_images = [];

        self.status_player = pg.transform.scale2x(pg.image.load("resources/gui/player_status.png"));
        self.status_player_text = ["Pokemon", "Level", "Health", "MaxHealth"];
        self.status_player_text_images = [];

        self.image.set_colorkey((255, 0, 255));
        self.step = 0;
        self.textImg = 0;
        self.livingTime = 0;
        self.opponnent = opponent;
        self.currentText = self.opponnent.name + " veut se battre !";

        self.arrow_show = True;
        self.arrow_selected = 0;
        self.arrow_coords = [(180, 352), (280, 352), (180, 402), (280, 402)];

        self.stepDone = True;
        #animation
        self.animationTimer = 0;
        self.animationActive = False;
        self.currentAnimation = "none";

        #combat
        self.opponent_pokemon = 0;
        self.opponent_pokemon_x = 440;

        self.player_pokemon = 0;
        self.player_pokemon_x = 232;


        self.selectStep = False;
        self.buttons = ["Attaque", "Inventaire", "Equipe", "Fuir"];
        self.button_images = [];
        self.attackStep = False;
        self.player_attacks = ["atk1", "atk2", "atk3", "akt4"];

    def render(self, display, font):
        if self.textImg == 0 :
            self.textImg = font.render(self.currentText, 0, (64, 64, 64));
        self.image.set_colorkey((255, 0, 255));
        display.blit(self.image, (0, 0));
        display.blit(self.textImg, (140, 340), self.textImg.get_rect());


        self.player_image.image.set_colorkey((255, 0, 228));
        display.blit(self.player_image.image, (self.player_image.rect.x, self.player_image.rect.y));

        self.opponent_image.image.set_colorkey((112, 192, 160));
        display.blit(self.opponent_image.image, (self.opponent_image.rect.x, self.opponent_image.rect.y));

        if self.opponent_pokemon != 0 :
            self.opponent_pokemon.draw_front(display, self.opponent_pokemon_x, 80)
        if self.player_pokemon != 0 :
            self.player_pokemon.draw_back(display, self.player_pokemon_x, 160)

        if self.showStatus :
            self.status_opponent.set_colorkey((255, 0, 255));
            display.blit(self.status_opponent, (170, 100));
            display.blit(self.status_opponent_text_images[0], (180, 105));
            display.blit(self.status_opponent_text_images[1], (332, 105));
            pg.draw.rect(display, (112, 248, 168), (249, 134, (self.opponent_pokemon.currentHealth / self.opponent_pokemon.maxHealth ) * 95, 4));

            self.status_player.set_colorkey((255, 0, 255));
            display.blit(self.status_player, (430, 220));
            display.blit(self.status_player_text_images[0], (455, 225));
            display.blit(self.status_player_text_images[1], (607, 225));
            display.blit(self.status_player_text_images[2], (553, 261));
            display.blit(self.status_player_text_images[3], (587, 261));
            pg.draw.rect(display, (112, 248, 168), (524, 254, (self.player_pokemon.currentHealth / self.player_pokemon.maxHealth ) * 95, 4));

        if self.selectStep or self.attackStep :
            display.blit(self.button_images[0], (200, 350));
            display.blit(self.button_images[1], (300, 350));
            display.blit(self.button_images[2], (200, 400));
            display.blit(self.button_images[3], (300, 400));
            display.blit(self.arrow_image, self.arrow_coords[self.arrow_selected]);


    def update(self, game, events, font):
        self.livingTime += 1;
        if self.livingTime % 30 == True :
            self.arrow_show = not self.arrow_show

        if self.livingTime == 50 :
            self.startAnimation("trainer_in");

        if self.animationActive :
            self.animationTimer += 1;
            self.runCurrentAnimation(font, game);

        if self.livingTime >= 130 :
            for event in events :
                if event.type == pg.KEYDOWN :
                    if event.key == pg.K_SPACE :
                        if self.stepDone and not self.selectStep and not self.attackStep :
                            self.nextStep(game, font);
                            self.step += 1;
                        elif self.selectStep or self.attackStep :
                            self.handleButtons(self.buttons[self.arrow_selected], game, font);
                    if event.key == pg.K_RIGHT and self.selectStep == True :
                        if self.arrow_selected == 0 or self.arrow_selected == 2 : self.arrow_selected += 1;
                    if event.key == pg.K_LEFT and self.selectStep == True :
                        if self.arrow_selected == 1 or self.arrow_selected == 3 : self.arrow_selected -= 1;
                    if event.key == pg.K_DOWN and self.selectStep == True :
                        if self.arrow_selected == 0 or self.arrow_selected == 1 : self.arrow_selected += 2;
                    if event.key == pg.K_UP and self.selectStep == True :
                        if self.arrow_selected == 2 or self.arrow_selected == 3 : self.arrow_selected -= 2;


    def handleButtons(self, button, game, font) :
        if self.selectStep and not self.attackStep :
            if button == "Attaque" :
                self.attackStep = True;
                for i in range (0, 4) :
                    if self.player_pokemon.attacks[i] != None :
                        self.player_attacks[i] = self.player_pokemon.attacks[i].name;
                    else :
                        self.player_attacks[i] = "------";
                self.buttons = self.player_attacks;
                self.button_images = [];
                for button in self.buttons :
                    self.button_images.append(font.render(str(button), 0, (32, 32, 32)));
            elif button == "Fuir" :
                game.guiHandler.closeGui();
            elif button == "Equipe" :
                game.guiHandler.openGui(GuiTeam.GuiTeam(self.player, self));
            elif button == "Inventaire" :
                print("Pas encore implemente");
        elif self.attackStep :
            attack = game.pokemonManager.getAttack(self.player_attacks[self.arrow_selected]);
            if attack != None :
                self.updateText(self.player_pokemon.name + " attaque " + attack.name, font);
                modifier = self.generateModifier(self.player_pokemon, self.opponent_pokemon, attack, game);
                total_damage = int((((2 * self.player_pokemon.level + 10) / 125) * (self.player_pokemon.currentAttack / self.opponent_pokemon.currentDefense) * attack.damage + 2) * modifier);
                if not self.opponent_pokemon.dealDamage(total_damage) :
                    self.startAnimation("player_attack");
                    self.updateStatus("player", self.player_pokemon, True, font);
                else :
                    self.runStep(7, game, font);


    def nextStep(self, game, font) :
        print(self.step);
        if self.step == 0 :
            self.updateText(self.opponnent.name + " : " + self.opponnent.dialog, font);
        elif self.step == 1 :
            self.updateText(self.opponnent.name + " :  " + self.opponnent.getPokemon(0).name + " je te choisis!", font)
        elif self.step == 2 :
            self.startAnimation("opponent_exit");
            self.stepDone = False;
        elif self.step == 3 :
            self.startAnimation("player_exit");
            self.updateText("Joueur : " + self.player.getFirstPokemonAlive() + ", a toi de jouer !", font);
            self.stepDone = False;
        elif self.step == 4 :
            self.selectStep = True;
            self.stepDone = False;
            self.startSelectStep(font)
        elif self.step == 5 :
            self.stepDone = False;
            self.opponentAttack(font, game);
        elif self.step == 6 :
            if self.opponent_pokemon.currentHealth > 0 :
                self.step = 4;
                self.runStep(4, game, font);
            else :
                self.nextStep(game, font);
        elif self.step == 7 :
            self.updateText("Le pokemon enemi est KO ! Vous gagnez ce combat!", font);
            self.selectStep = False;
            self.attackStep = False;
            self.stepDone = True;
            self.opponnent.beaten = True;
            print(self.opponnent.beaten);
        elif self.step == 8 :
            self.updateText(self.opponnent.name + " : " + self.opponnent.defeat_text, font);
            self.stepDone = True;
        elif self.step == 9 :
            self.opponnent.onDefeated(self.player, game);
            self.handleQuest(self.player, self.opponnent);
            game.guiHandler.closeGui();
        elif self.step == 10 :
            self.updateText("Votre " + self.player_pokemon.name + " est KO ! Vous perdez ce combat!", font);
        elif self.step == 11 :
            game.guiHandler.closeGui();
        elif self.step == 101:
            self.updateStatus("player", self.player_pokemon, True, font);
            self.updateText("Votre " + self.player_pokemon.name + " est KO!", font);
            self.stepDone = True;
        elif self.step == 102 :
            game.guiHandler.openGui(GuiTeam.GuiTeam(self.player, self));
            self.updateStatus("player", self.player_pokemon, True, font);
            self.step = 4;

    def runStep(self, step, game, font) :
        self.step = step;
        self.nextStep(game, font);

    def startSelectStep(self, font) :
        self.updateText("", font);
        self.button_images = [];
        for button in self.buttons :
            self.button_images.append(font.render(str(button), 0, (32, 32, 32)));


    def updateText(self, text, font) :
        self.currentText = text;
        self.textImg = font.render(self.currentText, 0, (64, 64, 64));



    ###
    ## Methodes d'animation
    ###

    def startAnimation(self, anim) :
        self.currentAnimation = anim;
        self.animationActive = True;
        if anim == "trainer_in" :
            self.player_image.rect.x = -120;
            self.opponent_image.rect.x = 880;

    def runCurrentAnimation(self, font, game) :
        if self.currentAnimation == "trainer_in" :
            if self.animationTimer <= 80 :
                self.player_image.image.set_alpha(MathUtils.lerp(0, 255, self.animationTimer / 80));
                self.player_image.rect.x = MathUtils.lerp(-120, 240, self.animationTimer / 80);

                self.opponent_image.image.set_alpha(MathUtils.lerp(0, 255, self.animationTimer/80));
                self.opponent_image.rect.x = MathUtils.lerp(880, 440, self.animationTimer/80);
            else :
                self.animationActive = False;
                self.animationTimer = 0;
                self.currentAnimation = "none";
        elif self.currentAnimation == "opponent_exit" :
            if self.animationTimer <= 40 :
                self.opponent_image.image.set_alpha(MathUtils.lerp(255, 0, self.animationTimer/40));
            if self.animationTimer == 41 :
                self.opponent_pokemon = self.opponnent.getPokemon(0);
            if self.animationTimer > 41 :
                self.animationActive = False;
                self.animationTimer = 0;
                self.currentAnimation = "None";
                self.stepDone = True;
        elif self.currentAnimation == "player_exit" :
            if self.animationTimer <= 40 :
                self.player_image.image.set_alpha(MathUtils.lerp(255, 0, self.animationTimer/40));
            if self.animationTimer == 41 :
                self.player_pokemon = self.player.getFirstPokemonAlive();
            if self.animationTimer > 41 :
                self.animationActive = False;
                self.animationTimer = 0;
                self.currentAnimation = "None";
                self.stepDone = True;
                self.updateStatus("opponent", self.opponent_pokemon, True, font);
                self.updateStatus("player", self.player_pokemon, True, font);
        elif self.currentAnimation == "player_attack" :
            if self.animationTimer <= 10 :
                self.player_pokemon_x = MathUtils.lerp(232, 280, self.animationTimer/10);
            elif self.animationTimer > 10 and self.animationTimer <= 20 :
                self.player_pokemon_x = MathUtils.lerp(280, 232, (self.animationTimer-10)/10)
            elif self.animationTimer == 21 :
                self.animationActive = False;
                self.animationTimer = 0;
                self.currentAnimation = "None";
                self.stepDone = True;
                self.selectStep = False;
                self.attackStep = False;
                self.buttons = ["Attaque", "Inventaire", "Equipe", "Fuir"];
                #self.nextStep(game, font);
        elif self.currentAnimation == "opponent_attack" :
            if self.animationTimer <= 10 :
                self.opponent_pokemon_x = MathUtils.lerp(440, 398, self.animationTimer/10);
            elif self.animationTimer > 10 and self.animationTimer <= 20 :
                self.opponent_pokemon_x = MathUtils.lerp(398, 440, (self.animationTimer-10)/10)
            elif self.animationTimer == 21 :
                self.animationActive = False;
                self.animationTimer = 0;
                self.currentAnimation = "None";
                self.selectStep = False;
                self.attackStep = False;
                self.stepDone = True;


    def updateStatus(self, character, pokemon, create, font) :
        if create == True :
            self.showStatus = True;
        if character == "opponent" :
            self.status_opponent_text[0] = pokemon.name;
            self.status_opponent_text[1] = pokemon.level;
            self.status_opponent_text_images = [];
            for text in self.status_opponent_text :
                self.status_opponent_text_images.append(font.render(str(text), 0, (32, 32, 32)));
        if character == "player" :
            self.status_player_text[0] = pokemon.name;
            self.status_player_text[1] = pokemon.level;
            self.status_player_text[2] = pokemon.currentHealth;
            self.status_player_text[3] = pokemon.maxHealth;
            self.status_player_text_images = [];
            for text in self.status_player_text :
                self.status_player_text_images.append(font.render(str(text), 0, (32, 32, 32)));

    def opponentAttack(self, font, game) :
        chosen_attack_number = random.randrange(0, 4);
        chosen_attack = self.opponent_pokemon.attacks[chosen_attack_number];
        while chosen_attack is None :
            chosen_attack_number = random.randrange(0, 4);
            chosen_attack = self.opponent_pokemon.attacks[chosen_attack_number];
        modifier = self.generateModifier(self.opponent_pokemon, self.player_pokemon, chosen_attack, game);
        total_damage = int((((2 * self.opponent_pokemon.level + 10) / 125) * (self.opponent_pokemon.currentAttack / self.player_pokemon.currentDefense) * chosen_attack.damage + 2) * modifier);
        if not self.player_pokemon.dealDamage(total_damage) :
            self.startAnimation("opponent_attack");
            self.updateText("Le " + self.opponent_pokemon.name + " ennemi utilise " +chosen_attack.name + " !", font);
            self.updateStatus("player", self.player_pokemon, True, font);
        else:
            if self.player.stillHasPokemonAlive():
                #game.guiHandler.openGui(GuiTeam.GuiTeam(self.player, self));
                #self.updateStatus("player", self.player_pokemon, True, font);
                self.runStep(101, game, font);
            else :
                self.updateStatus("player", self.player_pokemon, True, font);
                self.runStep(10, game, font)


    def handleQuest(self, player, opponent) :
        print("Quest info : ", player.questProgress, " NPC quest involvement :" , opponent.quest_involved);
        if opponent.quest_involved == player.questProgress :
            player.questProgress += 1;
            print("Quest progressed to stage", player.questProgress);

    def generateModifier(self, attacker, opponent, attack, game):
        STAB = 1;
        if attacker.type == attack.type :
            STAB = 1.5;
        typeMod = game.pokemonManager.getEffectiveModifier(attacker.type, opponent.type);
        randomMod = round(random.uniform(0.85, 1.0), 2);

        return STAB * typeMod * randomMod;