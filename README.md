# OSCVideo
Turns your Raspberry Pi into a OSC-controlled videoplayer


## Supported methods:  
**/background_on** - Adds a black bottom layer and removes the command line.  
**/background_off** - Removes the bottom layer and reverts to the command line.  
**/load** - Preloads a video to a specific player.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): Load the file to this player (1..10)*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*layer (int): The video layer of the player - currently not used*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*fileName (String): The file name*  
**/opacity** - Set the opacity of a specific player.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): The number of the player to set the opacity on*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*opacity (float): The transparency (0..255)*  
**/setPosition** - Sets the posistion of a specific player.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): The number of the player to set the opacity on*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*x1 (int): Top left x coordinate (px)*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*y1 (int): Top left y coordinate (px)*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*x2 (int): Bottom right x coordinate (px)*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*y2 (int): Bottom right y coordinate (px)*   
**/play** - Starts a specific player.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): The number of the player to start.*  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*fileName (String): If file not preloaded then specific the file name (optional)*.   
**/pause** - Pauses a specific player.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): The number of the player to pause.*  
**/stop** - Stops a specific player.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): The number of the player to stop.*  
**/loop** - Loops a specific player. Should be called before loading a player  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*playerNumber (int): The number of the player to loop.*  
**/quit** - Terminates the program loop.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Args:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*QuitProcedure (String): Use one of thees keywords ['shutdown', 'reboot', 'quit']*  
