# Remapping MCU Pins



SDA and pin 19 is I squed C0.CL, which actually might be a good thing because then we can simply route out pin 16 17 to the left of the accelerometer and we move pins 14 to the right hand side and we don't have that awkward crossing which we have to sort out with layer transitions and jumps and all of that nonsense.

So let's actually make that change. So I squed C, we're not going to use I squed C1 anymore anymore. We're going to use I squed C 0 on pins 18 is SDA, pin 19 is. So let's make that change in the schematic. Okay, I've made some changes in the schematic to reflect the changed pin out of the microcontroller as we just figured out from Code Composer Studio.

Because I ran out of space on the right hand side, I would have had to increase the schematic page sheet. I thought I'd show you something different. And I moved the accelerometer which is previously in the right hand side of the schematic to the bottom left. And to indicate that I'm jumping within a schematic or across schematic pages, what I typically do is do global labels as they're called in Keycat. So for instance, we have now pin 18 is SDA, pin 19 is.

And I've hooked these up with global ports. On the right hand side, I can pressR plus L, place global label. You can give the label name just like the net, but also a shape. So it's input, output, birectional, whatever. And that's what I put for pin 8, pin 19 to indicate that I'm jumping somewhere else.

If I just had a net label there, it looks like, okay, I've labeled the nets, but actually it's not connected to anything else. By placing a global label or one of these ports, I can indicate, at least to me, a jump. I also like to place some text around those ports or labels and say where's it coming from? Where's it going to? So here I'm saying two from accelerometer. This is I squed C0 SDA, I squed C 0Cl.

And that indicates, okay, we have to look for the same color, same net label. And we can see bottom left the accelerometer. That's the remaining space I had. Of course, you could could clean this up quite a bit. And here I have the same thing. I have the ports. I have two from MCU. And I've also changed the port directions appropriately. So SDA is birectional.

Cl is from the microcontroller to the accelerometer. The mic controller is the master in this case. Similarly for the interrupt signals because I've moved the accelerometer away. I have my interrupts which are two output pins, pin six and five, which go to the MCU. So we just have to look on the schematic. Uh-huh. They're in the same place as before. They ain't one and two, but these are inputs to the microcontroller.

And I'm writing here from the accelerometer just to make the schematic a bit more clear. And I didn't didn't want to cramp anything as much as it was before as well. You could also add, you know, some graphical elements, some boxes, labels around all this to make it a bit neater. But just to show you another schematic drawing technique also because this accelerometer and parts of the schematic have changed, moved around. I've also changed my annotation.

Previously, I believe these pre-op resistors were R six R7. The bypass capacitor was C13 rather than C14. So I've adjusted my designators to fit the flow of the schematic. So it's left to right, top to bottom. That's why the accelerometer and its panic components are last. Now if we go back to the PCB, I haven't imported those changes yet.

And what we have to do is either press F8 or go to the top toolbar and click update PCB from schematic as we did to get the components in in the first place. So click on that update from schematic. Update PCB. And we can see here our changes are now reflected on the on the printed circuit board. Now we can see our 16 1617 signals RTSCTS.

We can route through this passage here. I squ C SDA and SCCl look easier to route out as well. It looks like actually we don't have to do any crossings anymore. And our int one and in two we can just come around the C14 decoupling capacitor into the pins of the microcontroller. So this already seems a lot better.

And this is again trying to emphasize the point that a microcontroller is a flexible thing. If you have free pins, if if you have free peripherals, don't just stick to whatever you chose in the first place when you are creating the schematic. The schematic in a loose sense isn't terribly concerned with the actual physical placement.

Of course, you can think of that ahead of time and derive that from the schematic symbols, but it's something you can adjust and should adjust on the fly. Also, when it comes to PCB design, this is why I suggest doing it like so. Now, after all of that talk of adjusting pins and pin outs, we also have to, of course, add in the pull-up resistors. And because our colors are all nice, we can see that our polar resistors are R7 and R8.
