# Layout Accelerometer



Then we have some filtering networks, the whole power section, and the USBC pull down resistors. Let's keep the power section, the pull down resistors for the end. And now let's look at the accelerometer briefly. There's not terribly much. We've already placed the accelerometer itself. We need the bypass capacitor. That's our first order of criticality. And then the pull-up resistors.

These are of course important, but they're not as critical as the bypass and decoupling capacitors. So clicking on C13, moving to the PCB design. We want to take this part and see where it needs to go for our accelerometer. Now we can see we've got three different pads. And this can of course be misleading. Which which pad do we place the capacitor closest to? pin four, pin 7, pin 8.

Well, if you remember back to the schematic video, pin four is the chip select pin. That definitely does not need a decoupling capacitor. VDDIO, if we looked at the data sheet again, this did not need a decoupling capacitor. That simply sets the IO logic level voltage. What needs a decoupling capacitor and where C13 needs to be closest to is pin 8 of U4.

So, that's where we want to put it. And again, that's why you should always cross reference back to the schematic and see where to actually place components. Similarly for all the ground pads, we've got pin 3, 9, 10, 11, 12, 13, 14, and all ground. Which one is the actual power ground? Back to the schematic, it's pin 9.

So ideally, we want to short connections between pin 8 and the capacitor and pin 9 and the capacitor. Luckily, pin 8 and pin 9, as their numbers suggest, are right next to each other. So it would make sense to have our capacitor placed somewhat symmetrically. And of course, the grid isn't aligned to these pads.

But something like this might be reasonable because now we can route out pin 9 through the capacitor and pin 8 through the capacitor coming from a power source. And that might look something like this in the 3D viewer like so. There's two things I don't like about it. One, which might be more critical than other. I think for my personal liking for this board, we've got a bit more space that C13 is a bit maybe too close.

Let's say we want to resolder or refflow U4 because some connection didn't connect properly when when soldering. If we try to hot air U4, C3, C13 might come off as well. It might be more difficult to access the pads of U4. So therefore, I might want to move C13 a bit further away. Give myself some clearance. You don't have to pack components that tightly.

Another thing is again just for the sake of aesthetics and satisfying my OCD, I probably want to just center C13 with U4. Again, if I center this, it's only one click up. One click in this case being 0.25 mm based on my grid settings. It's a small enough change that is absolutely going to make no difference into the decoupling performance of this, but it just satisfies my need for making things nice and symmetrical and aligned.

Then moving the capacitor also one unit out, that gives me just a tiny bit more space between U4 and C13. It might not seem like much, but when you actually come down to having this under microscope, trying to reflow, resolder this, it could make a world of difference. So that's the easiest way we can then place C13 and U4. The next thing are the I squed C connections. And for I squed C.

Now we could think about, okay, we've got the UART RTS CTS signals. We're going to have to figure out how to route them past the crystal oscillator into the pads of U2. And these of course will be crossing with the SCCl SDA connections. So we could go to code go back to code composer studio to see can we maybe use pins 18 to 24.

Are there any I squed C pins we could use there? That might make our lives quite a bit easier. So just having a quick look at look at code composer studio. I've just got the pin out view on the right hand side open. If I just hover over some of the pins, so we're looking at the bottom side, of course, we can see actually pin 18 seems to have I squed C0.
