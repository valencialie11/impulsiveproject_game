import arcade
import os

SPRITE_SCALING = 0.5
SPRITE_NATIVE_SIZE = 128
SPRITE_SIZE = int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Games"

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 15
GRAVITY = 0.5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

#NOT SURE ABOUT THE CLASSES BELOW? SINCE SOME DOCUMENTATION REQUIRE IT, SOME DONT?

class Player(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        #change + center = assigned to center
        #move the player around
        self.center_y += self.change_y

        if self.left <0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT -1:
            self.top = SCREEN_HEIGHT - 1

"""
class Enemy(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
"""

class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self):
        #Call the parent class initializer

        #unsure
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        #unsure
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.wall_list = None
        self.bomb_list = None
        self.flag_list = None
        self.coin_list = None
        
        #Set up the player info
        self.player_sprite = None
        self.physics_engine = None
        #unsure
        #self.view_left = 0
        #unsure
        #self.view_bottom = 0
        self.game_over = False

        # If you have sprite lists, you should create them here,
        
        # and set them to None

    def setup(self):
        #Sprite lists AGAIN
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bomb_list = arcade.SpriteList()
        self.flag_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        #Set up a score
        self.score = 0

        #Draw the walls  (using looping)
        for x in range(0, SCREEN_WIDTH, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)

            wall.bottom = 0
            wall.left = x
            self.wall_list.append(wall)
        #range(start, end, multiples)

        #floating platforms
        for x in range(SPRITE_SIZE * 5, SPRITE_SIZE * 9, SPRITE_SIZE):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", SPRITE_SCALING)

            wall.bottom = SPRITE_SIZE * 3
            wall.left = x
            self.wall_list.append(wall)

        #floating blocks
        wall = arcade.Sprite("images/block.png", 0.15)

        wall.bottom = SPRITE_SIZE*5
        wall.left = SPRITE_SIZE*9
        self.wall_list.append(wall)

        #Draw multiple blocks
        wall = arcade.Sprite("images/block.png", 0.15)

        wall.bottom = SPRITE_SIZE*6
        wall.left = SPRITE_SIZE*4
        self.wall_list.append(wall)

        """
        wall = arcade.Sprite("images/block.png", 0.15)

        wall.bottom = SPRITE_SIZE*4
        wall.left = SPRITE_SIZE*1
        self.wall_list.append(wall)
        """

        wall = arcade.Sprite("images/block.png", 0.15)

        wall.bottom = SPRITE_SIZE*1
        wall.left = 40
        self.wall_list.append(wall)

        wall = arcade.Sprite("images/block.png", 0.15)

        wall.bottom = SPRITE_SIZE*1
        wall.left = SPRITE_SIZE*6
        self.wall_list.append(wall)


        #Set up the player
        self.player_sprite = arcade.Sprite("images/soldier.png", 0.2)
        self.player_list.append(self.player_sprite)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 100
        
        #set up the enemy at the ground
        enemy = arcade.Sprite("images/tank.png", 0.1)

        enemy.bottom = SPRITE_SIZE
        enemy.left = SPRITE_SIZE * 3

        #set up initial speed
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        

        # -- Draw a enemy on the platform
        enemy = arcade.Sprite("images/tank.png", 0.1)

        enemy.bottom = SPRITE_SIZE * 4
        enemy.left = SPRITE_SIZE * 7

        # Set boundaries on the left/right the enemy can't cross
        enemy.boundary_right = SPRITE_SIZE * 9
        enemy.boundary_left = SPRITE_SIZE * 5
        enemy.change_x = 2
        self.enemy_list.append(enemy)

        # Draw bombs on the flying blocks
        """
        bomb = arcade.Sprite("images/bomb.png", 0.1)
        bomb.bottom = 250
        bomb.left = SPRITE_SIZE * 5
        self.bomb_list.append(bomb)
        """

        bomb = arcade.Sprite("images/bomb.png", 0.1)
        bomb.bottom = 365
        bomb.left = SPRITE_SIZE * 9
        self.bomb_list.append(bomb)

        flag = arcade.Sprite("images/flag.png", 0.1)
        flag.bottom = SPRITE_SIZE
        flag.left = 750
        self.flag_list.append(flag)

        coin = arcade.Sprite("images/coin.png", 0.1)
        coin.bottom = SPRITE_SIZE*8
        coin.left = 270
        self.coin_list.append(coin)

        coin = arcade.Sprite("images/coin.png", 0.1)
        coin.bottom = SPRITE_SIZE*6
        coin.left = 70
        self.coin_list.append(coin)

        coin = arcade.Sprite("images/coin.png", 0.1)
        coin.bottom = SPRITE_SIZE
        coin.left = SPRITE_SIZE*9
        self.coin_list.append(coin)
        

        # Set up the physics behind the game
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)
        

        #Set background layout
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.player_list.draw()
        self.wall_list.draw()
        self.enemy_list.draw()
        self.bomb_list.draw()
        self.flag_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        
        if not self.game_over:
            # Move the enemies
            self.enemy_list.update()
            #Check the enemy
            for enemy in self.enemy_list:
                # If the enemy hit a wall, reverse
                if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                    #len more than 0 means there is more than 0 collision between the enemy and wall
                    enemy.change_x *= -1
                    # If the enemy hit the left boundary, reverse
                elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                    enemy.change_x *= -1
                # If the enemy hit the right boundary, reverse
                elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                    enemy.change_x *= -1
        
            # Update the player using the physics engine
            self.physics_engine.update()

            # See if the player hit an enemy. If so, game over.
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 0:
                #len more than 0 means there is more than 0 collision between player and enemy
                self.game_over = True

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED

    def on_key_release(self, key, key_modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        #Dont need to specify up because theres gravity programmed alr

    """
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        
        Called whenever the mouse moves.
        

    def on_mouse_press(self, x, y, button, key_modifiers):
        
        Called when the user presses a mouse button.
        

    def on_mouse_release(self, x, y, button, key_modifiers):
        
        Called when a user releases a mouse button.
    
    """

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()