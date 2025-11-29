# Layout for MCU Supporting Components



And typically for PCB design I'd suggest going in order of criticality. You might want to do slower speed connections last. You might want to do critical components such as the mic controller and crystal USB connections first. Prioritize those. Prioritize those components before you put in less critical components. For example, capacitors on reset lines, pull-up resistors somewhere.

It really depends on criticality. But of course, there's always going to be a compromise, always going to be a trade-off there. There's not going to be a single opt most optimal design. There many paths that lead to Rome as they say. For us, what I'd like to start with is the micro controller. This has the main bulk of supporting components. We have various bypass decoupling capacitors.

We've got the whole crystal circuit. We've got these trimming resistors, Reref connections, and so on. Once we have all those around the microcontroller, the rest is actually fairly straightforward. A couple bypass the coupling capacitors, some filter networks, some power, and so on. So, let's just get started with that.

What I'd suggest doing again is an order of criticality. The pull-up resistors for the I squed C accelerometer aren't that critical. Similarly to the end reset pullup resistor as well as this filtering capacitor. Okay, we might need it for this device to work. But in terms of proximity to to the device, what is most important? That's typically the bypass decoupling capacitor. It might be keeping the crystal oscillator loops short and small or trimming resistors.

So those are the components we should be prioritizing. And again, it's an iterative process. So for instance, we have C12, which is our Vcore capacitor. I can take that and just by looking at the rat's nest, I don't even have to have the schematic open. We can see at least for this case, we only have one Vcore net.

We want to have the Vcore capacitor fairly close. We don't want it too close that it interferes with the courtyards. That our copper clearances are too small. We want it reasonably close. Close enough, but not too far away. Somehow, this might be okay. Something like this might not be. It really just depends.

We want it as close as is feasible, but also not to interfere with any future routting and future component placements. For instance, if I place this capacitor like so, let's say we had to route out signals for for pins 47 down to 44. we can't really get past this capacitor. An option might be, okay, let's rotate this capacitor like so.

Now, we can at least fan out pins 47 to 44 if we need those pins. But it's not just the connection between, for example, this forward power path, this 1.35V signal. It's the overall loop area that matters with bypassing and decoupling. We have to take into account also our ground pad. And our ground has to go from pad 2 somehow, and we'll see later how that some is to pin 7. That is the ground.

the only ground connection actually for this microcontroller. So this entire loop area could be critical. So a way maybe to optimize that to also help with if we route out pins 47 to 44 is take this capacitor, press R to rotate and move it like so. Now the ground and 1.35V nets are fairly close.

And I'll show you how to connect all the ground pads later. And actually just as a little hint, we'll be using the bottom copper layer to facilitate that with a large hopefully solid ground plane. For this board, of course, all of the components are on the top layer. And that's what I'd strongly suggest doing unless you have a reason otherwise too is if you can use one primary layer for all of your components and that's exactly what we're doing here. So for instance to start off with a capacitor placement like so might be okay.

It's reasonably close to the 1.35V pad. The ground connection we will see is probably as short as we can get it. Okay. We we could move the capacitor in like so. But if we look at the 3D view in terms of assembly, if we want to get to this component, it makes a bit harder because of the LQFP edge at the top left of this package. Therefore, let's say let's keep the component like this for now. We of course also have our 3.

3 capacitor. Going back to the schematic, that's C11. If I click on this, go back to the PCB design, we've already jumped to it. And this is a larger component package. It's 0805. Press M. Move this to 3.3 volts. So, this already is a bit maybe, let's say, a bit more challenging. If I press R to rotate again a couple times, ideally the connection would be something like this.

Let me just click on this silk screen designator. Move this a tiny bit of way so we can see it a bit better. We want to consider both the forward and the return path. So 3.3 volts. We could think of a nice short connection between these two pads and pins 2 and 7 is our ground connection. Again, a short path.

Now, while this would be great in theory for bypassing the coupling, how are we going to get our osque pin 8 out to a resistor down here? How are we going to get reset out? N reset. Okay, it might be a bit easier because we can slip out of the top here, but ours is going to be difficult. So, we probably have to move this capacitor away a tiny bit. This way, we can come out of pin 8, move past the capacitor down to the bottom.

Again, thinking ahead to your routting, your layout choices will significantly impact how you route out this PCB. So, something like this might be okay. In case you're rooting out pin 5, you might have to rotate your capacitor like so. Again, not entirely optimal, but it could be an option.

But for us, because we are not that constrained in terms of how many pins we're actually using, some placement like this might be okay. Bypass decoupling capacitors as close as is feasible to the relevant power and ground pins. Other than that, C11, C12. What's also important, ROS, and of course the crystal oscillator because we just saw the ROS pin. Let's just do that. R4 M to move. And keep in mind again, we're still with these fairly fixed grids. So, we can't place it terribly close to pin 8.

Ideally, we want something like this. But of course, our capacitor is in the way. So, we might want to put our ROS resistor somewhere like here, which means we have to carry out of pin 8 into pin 2 of the ROS resistor. And it looks like we should be able to fan out pins 11, pins 12 of a high frequency external crystal oscillator, which sits down here.

So, again, we might have to move these capacitors and resistors out a bit further, but this might be a good starting point. If you can, and if you want to while you're rooting, of course, we'll have to adjust the silk screen later on. I always like to also move the silk screen out of the way just to make things a bit easier to see, a bit easier to read like so. But of course, we'll adjust that later on.

These are fine tuning things. They're not terribly important for now. That being said, we have our osk in place and now we have our crystal that we need to put in place. Now, ideally, our crystal, we are missing the load capacitors for now. Should be as close as is feasible to the pins. So, something like this might be okay. But keep in mind, we still have load capacitors left and right of this.

And also we want to keep our crystal and crystal oscillator circuitry away if we can from other aggressive signals. Aggressive signals might be fast rise and fall time digital signals. For example, we wouldn't want to put our crystal oscillator far away from the component next to these USB signals. That wouldn't be great. So we want to keep the distances reasonably short. It doesn't have to be terribly short.

There are somewhat forgiving, but maybe a component placement like so might be right. We will looks like we have fairly short traces for HFX in and HX out. We have place for our load capacitors and we can route our I squed C lines somewhat away from the crystal. So picking up C8 and C9, I'm just dragging over pressing M to move both.

What I want to do is place my load capacitors fairly close. If I place them close like so, this still looks okay that I could, for example, desolder C8 and replace it with a different capacity if I need to tune the load capacitor values. So keep them close, not too close, not too far away. Something like this seems okay.

And again, I'm relying on the grid settings to make sure I'm vertically aligned. But for instance, also X1 to R4. I quite like when the components are also aligned horizontally like so. So, always checking with all three looking at the 3D view. Again, this comes from experience, just seeing just by visually being able to tell, is this close enough? Is this is this too far? And so on.

Is it away from signals? An iterative process. And of course, it takes some time to get familiar with how these circuits work. But somehow this might be okay. If you want to live a bit more aesthetically, you could of course move down X1 and C8C9 to be in line with U4. Now, that's a sacrifice that the pins 11, pins 12 have a longer trace length to go in here. So, it might not be reasonable to do so.

So, that's why you might want to keep your crystal oscillator section just a bit closer like so. Other than that, what's left in terms of critical circuitry? Well, I would immediately jump to the VRF minus VF plus pins. If you are using the integrated or an external voltage reference, you will have to place those.

So C10 and R5 would be the next critical components. And after that, we can then finally move on to the end reset. And by that time, we've pretty much done a rough layout just for the microcontroller section. So you can see just following some basic simple rules, it isn't that difficult, at least for of course a very simple demo board like this. C10 is our VRF capacitor, and I'm just following the rat's nest.

You can see the rat's nest are twisted. That's our crossing. That's why I have to rotate the component by 180°. Let me move the silk screen out of the way because it's a bit irritating. And now we can see okay maybe we want to place it centrally between pads 43 VF plus and pad 39 VF minus. And I'm also placing it in line with my 1.35V capacitor.

So we have nice short distances to VF plus VF minus and our bypass decoupling capacitor. And now we can also grab that grounding resistor. And again if you're using VF minus you should in theory tie this directly straight to ground. We've just used this 0M resistor as a short link. So I'll take this resistor press M to move as usual.

Rotate it 180 degrees by pressing R and place it close again. Not too close that the courtyards overlap, but just that the courtyards align like so. And I can move the silk screen just to make it a tiny bit neater like so. Crl S to save. Alt three to view in 3D. And you can see like so this is a pretty nice tight placement of decoupling and bypass capacitors.

Again, C11 is a bit further away because it's a larger package and because we have pins to route out and past these components. That's why we place C11 a bit further away. In any case, this is a rough layout for our mic controller. Very simple, and we've already thought ahead to the routting stage, which will make our lives quite a bit easier later on, as we'll see.

Of course, now we can't forget the end reset lines. So, we have this pull-up resistor and this filtering capacitor, C14 and R8. So, we are going to do C14 first. Take C14 and let's see where this needs to go. C14 looks like it has to be here at pin 4.

Now unfortunately if we place for example our reset and reset capacitor like so when we place iron reset pull-up resistor left of this for instance our URX RX lines will have to go over this capacitor over the resistor and into our U2 USB to UR converter not great and also the actual location of the N reset capacitor resistor doesn't terribly matter at least it doesn't matter as much as for instance the bypass and decoupling capacitors where else does this N reset signal go to well following rat nest it goes to our serial debug our tag connectet connector so we could say okay the location of these components

isn't terribly critical let's place it if in the vicinity of something that belongs to this component group so I could move it like so close to the tag connect connector that means later on we'd route out of pin 3 through this spacing into the reset capacitor and then we'll route into our in reset pin like so again for something that's less critical this placement might be okay we of course also need the restor That's R8.

And we'll just place that adjacent to our capacitor. Something like so. Now, for my liking, we're getting a bit close to the mounting hole. So, if we go to all three again, 3D view. Okay. This pad for the mounting hole is fairly generous. So, it's probably still okay, but you might want to move these components a bit further away given that we have the space.

So, for instance, we could take this grouping of components and we could move it like so. for instance, we still can route out in a nice clean fashion to the end reset pin and this still gives us some space away from our mounting hole. Keep in mind also now the T connector footprint and actual connector is fairly small even with this legged version.

But you will have these prongs for lack of better word that have to go through these mounting holes. So that's why you might also want to keep clearance away also indefinitely on the bottom side. Keep clearance away from these holes for the legged version of this connector. But again, just to show how you can be fairly flexible or more flexible by not with these less critical components.

Again, just moving the silk screen out of the way, clicking on it, making sure it's highlighted, and pressing M to move. Making sure the order is right as well. So, something like this, for example, and I've just aligned it also on the X-axis, horizontal axis, like so. All right. So, this is the main part of our microcontroller.
