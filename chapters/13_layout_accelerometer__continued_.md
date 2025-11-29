# Layout Accelerometer (Continued)



And these should be in the vicinity of the I squed C devices. So I'll move them together first of all. So a thought could be that we either route into a U4 then out and into the polar resistors or we do them somewhat in line. So for instance, I could move U4 and C4 down a bit.

So I could place my polar resistor somewhat in line that I route into SDA into the SDA pincccl through the polar resistor into U4 for instance. It it doesn't really matter in this particular case. I could even have for the pull-up resistors over here route into U4 first and then to the pull-up resistors for I squed C such a slow bus such a slow interface it isn't critical but of course you should make a reasonable effort reasonable attempt of making your routing layout fairly clean and fairly sensible.

If we place U4 and C14 that far at the bottom it's quite close to the board edge and also we'll probably have difficulty rooting out in one and in two. You might want to move U4 and C4 up a bit or moving your pull-up resistors up a bit as well. We're iterating again because now UR RTS CTS will have difficulties passing past R7, R8 and C9.

So that means we might have to move our crystal section just a bit to the left to make sure we have a channel for RTS CTS to route past the crystal. Now again, it might not be as aesthetic as before, but we want to prioritize the actual function over the aesthetics. So something like this might be in a reasonable first attempt at the layout for these particular components.

Finally, we really only have things that are to do with the power section. We have the USBC pull down resistors as well as a filtering pi network and the input output capacitors for U1, which is our LDO regulator. So you could start left or right. You can say, okay, let's put R2R3 down. Let's do a PI filter that goes into our LDO regulator.
