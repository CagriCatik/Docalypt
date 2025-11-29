# Rough Layout



The routting once you've done a good job of layout will for the most cases fall nicely into place. If we do a rubbish job at laying out, we're going to have a much harder time. We might need more layers. We might need more view transitions and whatnot if we don't do our layout properly. So lay out properly first. This is a large part of the work.

And then we can simply connect things together. Often times you will of course have a predefined board outline that you might get from a mechanical engineer which are based on certain enclosure dimensions where you need to put the mounting holes, what the board outline should be, where you need certain keepout areas. And of course, you have to keep all of that in mind originally also through the layout phase as well.

For us, this is just a simple death board. We have none of these requirements. We're just going to make it, I guess, as small as it's somewhat feasible. We don't want to cramp things together. Components should be accessible. We should be able to add in test points, add in probe blades, and so on. We don't have particular conraints, but keep that in mind when you're designing for a proper product.

With that being said, let's get over to doing the layout. And layout is very much, in my opinion, about sectioning. We have a microcontroller section where we have the microcontroller as our centerpiece. And we have various bypass decoupling capacitors and maybe pull pull down resistors, configuration resistors around it, and that forms its section. We've got USB with the USB connector.

We have the ESD protection and some filtering that forms its little section. We have a power supply with the LDR regulator in this case. input out capacitors those all form sections we put those sections together and then we put the whole PCB together very simply speaking the way I typically do that is take the center piece of the section and for this particular board we are working rather simply just with a microcontroller and it has its peripherals so what I'll grab is I'll take the mic controller click on it and press M to move then I can freely move

if I press escape I can cancel command and it's important when you're doing layout and also in my opinion when you're doing routing is to stick to fixed grids same as we did with the schematic where we used 100 mil grids for the PCB design. Now, if you're working in the US or if you're working other parts of the world, you might be using mills, but we're going to be using millimeters.

And the grid selection drop down is at the top. My ass cursor is just circling this, and it's currently set to 0.25 mm. For rough layout, typically I would not go below 0.25 mm grid for laying out. Typically, I might even go to 0.5 or 1 mm just to get a rough placement.

We can always fine-tune later, but I find it very important to always stick to grids. Even when you're placing smaller components such as bypass decoupling capacitors, I would never really go to 0.025 mm grid. There are of course accuracies and precisions of the various assembly pick and place machines and so on. So 0.25 or 0.1 as an absolute minimum is typically sufficient, but I would suggest going with 0.25 as the absolute minimum.

So I'll select 0.25. If I don't want to use my mouse to cycle through the various grid sizes, I can press N on my keyboard to cycle down and shift N to cycle up. So, that's a quick way of cycling through the grids. So, I'm going to start with the 0.5 mm grid. Click on the component or just hover over it and press M.

And we see we snap to the component center. Let's just move that somewhere on the grid. You can see the grid lines on the background and key card just somewhere away from the other components that we have some space to place components around it. Now that we have a component placed also if you hover over the component or select it press M and then R we can rotate the component by 90° counterclockwise.

But with the component orientation as we had before let's have a look at the pin out because the pin out at least for this particular board we don't have particular other constraints will determine for a large part how we place the surrounding components.

If we zoom in we can see that pin one and pin 2 as we designated in the schematic belong to UART TX and UART RX. UT TX and RX go to the USB UAD converter IC which then subsequently goes to the USBC connector. So it might make sense given the pin out of this microcontroller to have on the left hand side the CH340 as well as the USBC connector.

Now of course we can move the pins to other locations as we saw with code compar studio. So we could move them to the top, bottom, right, wherever we can find a UR peripheral. And often times it really pays off to move pins around because microcontrollers and FPJs are very flexible in terms of their pin out to locations that make your PCB design life easier. For us, it'll probably be okay at the top left pins.

It could be that later on as we progress through layout and routing, we say actually it's a bit cramped on the left hand side. We've got a lot of free free pins on the right hand side. So it could very well be that we want to move some components around. If we move on, we can also see that we have the crystal pins, pins 11 and pins 12.

So we want that crystal probably on the bottom left of the microcontroller. We have I squed C on the bottom. So we might want our little accelerometer at the bottom here. On the right hand side, we can see we have the serow wire clock and serow wire debug pins. So we might want to have our tag connect TC2030 programming header on the right hand side. Scattered around. Again, we have some free pins.

So we could move things around. We can't move pins 34 35 around. Certain pins are fixed of course such as also the power pins. So we have 1.35 volts. We've got a VF plus those pins will be fixed for most part but do keep in mind microcontrollers are flexible. Adjust your pin out.

Don't just stick with the first thing you said in your schematic. If you can move it around if it helps you with the PCB design. So an approach now could be that we have the microcontroller placed in our current center. We can of course move the grid origin and then place components around this microcontroller.

for example, the decoupling capacitors, the ROS resistor, the peripherals we need for this mic controller to even boot up. And then we do the same thing for other sections. An alternative approach might be that okay, we've placed our centerpiece. Let's not worry about the surrounding local components for now. Let's just get a rough idea of the other components we might want to place.

So, we might want to take U2, which is our U to USB converter. Press M. Move that to the left hand side. And we can see already the rat's nests seem to line up quite well. So I can just place it somewhat to the left of it. We can see ULTX seems to flow nicely and U RX seems to flow nicely as well.

And on the left hand side of the USB to U converter you have the D minus D plus pins which then go to the left hand side to the SUV connector. So that would be one approach of doing it before you start placing local bypass and supporting components around these various centerpieces let's call them. Another point is that here you can see I only have the PCB design window open.

What I simply do is I have one screen which has the schematic view open and one screen that has the PCB window open. Of course, I'm recording this on a single screen at a lower resolution. So, everything would be rather cramped. But let me just show you quickly. This is a split that could look like this. Of course, it's rather cramped because this because the resolution is fairly low again and is a single screen.

But on the schematic, if I click on one component, for example, click on J2, our programming header, there's cross referencing built into Keycad. So immediately in the PCB window, we jump to the relevant component. And this works both ways.

If I click on, for example, C3 on the schematic, it jumps to show us that this is the input capacitor for the LD regulator. And this is a super useful feature that I suggest you keep on pretty much at all times. And if you have two screens available, put one screen the schematic and on the other screen, put the PCB design. Then you don't have to always all tab or switch between windows to see what you're actually rooting. Now for us, we have a very simple PCB.

We've colored and labeled our nets fairly appropriately. So, we can probably get away with just looking at the PCB window. But imagine for larger schematic, multi-page schematics, it's it's really good to have these various windows open at all times so you can quickly cross reference. But in our case, again, this is a very simple board.

I'm just going to go with placing the components as they are because we know the structure of the schematic quite well. We know that for U2 on the right hand side, same as on the schematic, we connect to the mic controller. On the left hand side, we go through some ESD protection to us to a USB type-C connector.

And the same thing we can then reflect on the PCB design because things seem to flow quite nicely. We take D1, press M to move, and move it just to the left hand side. We won't worry about exact placement just now. We can tidy things up as we go. It's an iterative process layout and routing. So, we can take this. Of course, we'll have to take care of the orientations and alignments.

You can see for instance, the minus and plus terminals seem to be flipped. at least if we we can't read them just directly. So, we might have to sort something out later. But we can take the USB type-C connector, M to move, R to rotate, and just place it all nicely aligned on a grid. And you can see everything's aligned on this X-axis in one line.

I find this very visually appealing as we'll see later on. Sticking to a grid, aligning things that there's some sort of symmetry if possible, of course. Doesn't have to be, but I find it quite nice. Now, we're just starting with a rough layout.

We might want to of course reduce trace lengths and we can do that by placing placing components closer together. You don't want to place them too close as you can see kit get will show you that they interfere but you don't want to place them too far away either. There's always going to be a happy medium. Keep in mind we have to fan out and route out a lot of these pins. We might have to place some filtering and bypass capacitors around these components.

So you don't just want to scrunch all of these components together like this. You still need to leave space for surrounding components. So I can control Z to undo all that. Again, this is just a very rough layout and placement. From that, we can then define a board edge. We can put down the mounting holes and then we can get into details of the layout.

We only really have the tag connect programming header on the right hand side. That's this component. And you can see here as I hover it over and I hover over a pad. If I press M, it'll actually snap to the pad. And the pad isn't the component center.

You can see the component center is indicated by this little plus, this little cross in the right in between pin four and three. So, I actually want to hover over that and then press M. And now we can see we're snapping to the component center. That's why we suggest you do that. Keep in mind, don't hover over pins. Hover over component center before you press M. And you can see here that a rat's nest in blue are moving around as we move the component.

And this is a great visual indication of where approximately we should be placing our components. Over here wouldn't terribly make much sense unless you have a mechanical reason to do so or you don't have space. For us, we want to put the component again in line but on the right hand side maybe. Again, while you're doing your layout, keep your rooting in mind. you want to make your own life far easier.

So I could also take this component rotated by 180°. Okay, layout wise it look might look very similar. But now you can see pin 35 the clock pin has to route a longer way into pin 4 and pin 34 serow DIO has to go all the way around into pin 2. So as we had it before, let's rotate the component back. We have a shorter distance like so. We can immediately see we have probably easier ways of routting this if we keep it like so.

Again, pre-plan, pre-plan, pre pre-plan. For a board like this, it's very simple, but for more complicated boards, you might want to write this down some or sketch it out on a piece of paper or whatever your preferred method is. We have a crystal. I'm going to take the crystal, and we already saw at the bottom left of the microcontroller.

This is somewhat where the where the component needs to be. I'm just going to put it in the vicinity. Again, rough layout first. The last two major parts are the I squared C accelerometer. That's U4. And we saw the I squared C pins currently are and the interrupt pins are the bottom of the microcontroller. Again, we can move them around. For instance, we might want to put them at the top on the right hand side.

But for now, let's just place them somewhat centrally below the microcontroller. You can see this part is actually rather small. So, that's going to be interesting to fan out and route out as well, but not terribly difficult. Finally, we have U1. And remember, U1 is our LDL regulator. And it has these various surrounding components.

It gets fed from our 5V supply coming from Vbus from the USB type-C connector and then feeds our various other IC's on this board with 3.3 volts. So it might make sense to take this LDO regulator and not put it on the right hand side anywhere. We could put it just above D1 as we're getting our power from the host that is connected to J1, our USB type-C connector.

So a rough an incredibly rough layout might look something like this. From this, we could do a quick measurement. If we go to inspect and then measure tool, I'm just going to click and just do a diagonal measurement. If I click again, I can see, okay, the board might be around 55 mm in width and the height might be around 20 mm.

So, this could give us an estimate. Okay, we might only need a 50 mm wide board and a 20 mm m tall board. But, of course, we also have our mounting holes. And these are fairly chunky M3 mounting holes. If I click on this and press E, I can open the properties and we can see yes, as we wrote in the schematic as well, this is an M3 mounting hole.

For this board, it might be overkill. I quite like M3 mounting holes. This is a fairly common size. And we can move those in, for example, the four corners of the PCB. Again, fairly rough placement. It could look something like so. And you can now imagine we could draw a rectangular board outline around these mounting holes and say, okay, for this very, very simple demo board, this is a rough layout and outline.

Again, it's you have far more freedom, which sometimes can be a good thing, sometimes can't, to define our board outline and move our components. We could also say, "Yeah, this is actually far too long. I want to make this reasonably smaller." So, what we could do is just move all of our components by clicking, dragging, holding the left mouse button and say, "Actually, we might only need something like this amount of space.

" And again if I do either inspect measure tool or press control shiftm on my keyboard we can see okay now because the mounting holes we've increased in the height height of the board or width whatever you want to call it and the length but is reduced to 45 mm if that's this important for this board probably not I'd rather have the board slightly longer wider desk makes that it makes our routing and layout life easier we don't have a particular constraint to make this board as small as possible so I'm going to press escape a couple times to cancel the command and control zed just to space out the board as we saw

fit. What I would like to do is align the mounting holes so their centers align both horizontally and vertically. So I can control shift M, click the measure tool. We can see it's 45 mm center to center for this one. It's 19.5 mm center to center for this one. I typically prefer round numbers.

So 20 mm, 30 mm, 40 mm, something like that, not these decimal places, so integer numbers. And we can measure M2 to M3. And we can make sure that our hole centers are aligned and symmetrical. To move the mounting holes, I can either hover over these, press E, and then select the footprint, and then change the XY position in this pop-up box, press okay.

Or I can just change my grid by pressing N. So, changing it to 0.25, selecting both, pressing M, and I can just press my arrow key one up to move them 0.25 mm up. Do the same thing for the bottom two. Press M, arrow key down. And now, if I do control shift M, center to center, I now have 20 mm. And I have 45 and 20 placements like so.

So, something like this could be okay. And from this then we can draw our board outline. Again, you might come up with a completely different board outline, different positioning. And I'd strongly suggest spending more time on this, seeing if you maybe optimize a tiny bit more.

Again, we will probably optimize the layout a tiny bit before we add in the other components on the right hand side. You can see we still have to fit all of these in the space we then define. But I'll show you how to create the board outline because now if we go to view 3D viewer or press all three again, the board outline is missing. And Keycad has just stretched out the board outline to contain all the components and also the silk screen on the board.
