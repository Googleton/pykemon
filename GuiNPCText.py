import pygame as pg;
import GuiBase;

class GuiNPCText(GuiBase.GuiBase) :

    def __init__(self, text, name, npc):
        GuiBase.GuiBase.__init__(self, 0, 400, 800, 200);
        self.image = pg.image.load("resources/gui/npc_text.png");
        self.image.set_colorkey((255, 0, 255));
        self.text = text;
        self.name = name;
        if npc is not None :
            self.npc = npc;

            self.multiLine = npc.hasMultiDialog;
            if self.multiLine :
                self.lines = npc.dialog_multi;
                self.lines_images = [];
        else :
            self.multiLine = False;

        self.textImg = 0;
        self.livingTime = 0;

    def render(self, display, font):
        self.image.set_colorkey((255, 0, 255));
        display.blit(self.image, (100, 400));



        if self.multiLine and len(self.lines_images) > 0 :
            for number, image in enumerate(self.lines_images) :
                display.blit(image, (120, 440 + (20 * number)));
        else :
            display.blit(self.textImg, (140, 440));

    def update(self, game, events, font):
        self.livingTime += 1;

        if self.textImg == 0 :
            self.textImg = font.render(self.name + " : " + self.text, 0, (0, 0, 0));


        if self.npc.quest_involved == game.player.questProgress :
            if self.multiLine and len(self.lines_images) == 0 :
                for number, line in enumerate(self.lines) :
                    print(line, number);
                    if number == 0 :
                        self.lines_images.append(font.render(self.name + " : " + line, 0, (64, 64, 64)));
                    else :
                        self.lines_images.append(font.render(line, 0, (64, 64, 64)));
            else :
                self.textImg = font.render(self.name + " : " + self.npc.quest_dialog, 0, (0, 0, 0));

        if self.npc.name == "Maman" :
            for pokemon in game.player.team :
                pokemon.dealDamage(-9999);

        if self.livingTime >= 30 :
            for event in events :
                if event.type == pg.KEYDOWN :
                    if event.key == pg.K_SPACE :
                        self.nextStep(game);

    def nextStep(self, game) :
        self.handleQuestProgress(game, game.player, self.npc);
        game.guiHandler.closeGui();

    def handleQuestProgress(self, game, player, npc) :
        print("Quest info : ", player.questProgress, " NPC quest involvement :" , npc.quest_involved);
        if npc.quest_involved == player.questProgress :
            player.questProgress += 1;
            npc.onDefeated(player, game);
            print("Quest progressed to stage", player.questProgress);

