# import vlc
#
# def play_video(video_path):
#     # Create a VLC instance
#     instance = vlc.Instance()
#
#     # Create a media player
#     player = instance.media_player_new()
#
#     # Load the video file
#     media = instance.media_new(video_path)
#     player.set_media(media)
#
#     # Set the window to play the video
#     player.set_hwnd(0)  # Pass 0 for Windows OS, use the appropriate value for other platforms
#
#     # Play the video
#     player.play()
#
#     # Wait for the video to finish or exit with 'q' key press
#     while player.get_state() != vlc.State.Ended:
#         pass
#
#     player.stop()
#
# if __name__ == "__main__":
#     video_path = r'C:\python\NLP\content_searcher\data\videos\Schwarm von Golden Retriever Welpen.mp4'
#     play_video(video_path)

import pygame
from pyvidplayer import Video

def intro(video_path):

    vid = Video(video_path)
    vid.set_size((900, 900))


    # Initialize Pygame
    pygame.init()

    # Set the screen dimensions (width, height)
    screen_width = 800
    screen_height = 600

    # Create the Pygame screen
    SCREEN = pygame.display.set_mode((screen_width, screen_height))

    print(vid.get_file_data())
    # vid.seek(1034 // 25)
    while True:
        vid.draw(SCREEN, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()


# Set the window title
pygame.display.set_caption("Pygame Screen")

intro()

# Run the main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen with a white color
    SCREEN.fill((255, 255, 255))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
