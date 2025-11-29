# Board Outline



And of course, we just want to define it around these mounting holes. So, close that view. Go on the right hand side appearance. Click on layers. And then we want to go to the edge cut layer. Edge cut layer is our board outline layer. And for this, we will be drawing lines on the board. I'll show you first of all how to do rectangular corners. And then we'll do rounded corners.

So, I can press control shift L on the right or all on the right toolbar. Just click on this draw lines tool. Again, I might want a larger grid. So, I'm going to do shift N to increase the grid to 1 millmter. And I can just click on one point and start drawing around these mounting holes, for example, like so. Double clicking to end, and then press escape, escape to cancel the command.

And now I can press alt3 again to open the 3D viewer. And we can see now this board outline error or warning has disappeared. And we actually have a board outline that follows what we defined with these straight lines. Now this board outline again is somewhat arbitrary. It's just based on a very very rough placement. There's no particular goal here other than making a dev board.

No particular minimum size or mechanical constraints. That's why you might think okay yeah there's quite a lot of space. It's quite empty. But for the sake of our videos, for the sake of demonstration, I think this is this is sufficient. What we can also do is of course make rounded corners. The way we can do that is not by using the straight line tool. We can use the draw arcs tool.

If I click on the draw arcs tool or I can press control shift A or I can for instance go to the center one of these mounting holes and click once click twice to define one vertex and then I can define the angle 90° in this case. Press escape. Then I can take my straight lines and just drag them to the edge points of this 90° arc.

Press Alt 3. And now we can see we have a rounded corner on one of these on one of the corners of the boards. And of course we can repeat that. We can simply copy that corner, that rounded corner over to all of the other corners. There's some things to keep in mind, however.

Rounded corners require a routing tool rather than uh rather than using Vcuts or Vcoring for when depanalyzing or panelizing the PCBs. Sometimes Vcuts can be cheaper, less work inensive and but in any case for Vcut or Vcoring as well as routing, you will have to keep a certain distance clearance away from the board outline. That's for any components, that's for copper and so on.

So that's why for instance here if I use the measure tool again ctrlM just as a crude measurement tool from about the copper to the board edge I have about8 mm and I'd suggest for most boards unless you have very very tight constraints keeping at least about 0.5 mm of board 0.5 mm of clearance to the edge that's for components that's for copper that's for silk screen things like that we want to keep this kind of area of 0.

5 mm around the perimeter of the board clear from component silk screen as we said before and this again just ensures manufacturability. So let me copy over these corners just by Ctrl + Cing by selecting the corner Ctrl Ctrl +V press R to rotate and I can move them to the centers of all my other mounting holes and do exactly the same thing by dragging these lines around. So I'll see you in just a second once I finish that.

So this for instance is what the board would look like in its very rough state just with rounded corners. And again for now it's just a visual aesthetic preference just to show you how you can do that.

And of course, you can make fairly arbitrarily shaped board shapes using these simple primitives on the edge cuts layer with a very rough outline in place. The mounting holes placed somewhat sensibly. You might also want to adjust the outline to have nice round integer numbers. You know, in the steps of 5 mm, but of course that's not an absolute must. Again, we are very free in the way we define our board outline here.

But what I have now is a board of around 53x 28 mm, which for us is completely fine. I've moved the mounting holes to be nice and symmetrical around the board. But what we also have to take care of is of course now the grid placement. So the grid placement is something you could do right at the start. We could have said okay the grid we originate at our microcontroller and that's our center.

But it often times makes sense and also the IPC recommends that the grid origin is at the bottom left of the board. So that would be essentially the intersection if we extend the vertical and horizontal lines. That's where we want to place our grid origin. The reason for that is that if we go up or right, so anything that's on the board or within the board within the board area has positive x and y coordinates.

We have no negative x and y coordinates. If we want to move component more north, we simply have to add. If we want to move it to the right, we simply have to add a number and so on. So that's why you would typically choose the bottom left as your grid origin. So the way to place then our origin if we want to place at the bottom left is go to place grid origin at the bottom and we can just place that right at the intersection of the horizontal and vertical lines like so. And now we can see the grid is realigned to that point

bottom left. So that is our grid origin. You might have already seen if we go to the place drop down again there's also a drill and place file origin and that I'd suggest also putting on the same origin as the grid origin. So I can place that here and we can see now in red we have the drill and drill origin aligned there as well.

So everything is referenced the bottom left corner we have positive x and y coordinates for all the components. Now this is great but if when it comes to alignment especially if you want to for example align components distribute them distribute them equally across the board align them horizontally vertically having the grid origin bottom left isn't particularly helpful.

So often times I might start out and say okay I'm actually going to have my grid origin in the center of the board. that allows me to do symmetrical placements. So, we could do that because we already know the dimensions of the board. So, it's 53x 28 mm. So, we need to do half of that and place our grid origin there. We can see on the bottom as I move my cursor, the x and y coordinates change.

So, if I hover over the grid origin, that's 0 0. And as I move to the right and top, we can see the grid origin change. But we also have the dx and dy. dx dy tells us the relative or the deltas between wherever we set a starting point. And the starting point we set by tapping space. So we want a starting point or reference point to be on the grid origin.

I can hover over that and press space. And you can see the dxdy at the bottom has reset. And now I can do it relative to a certain position that I designate by pressing space. So if I want to go if I want to do it relative to the center of the board, I can go to position 26.5 and 14 because that's exactly the center of the board. Press space.

And now our deltas are relative to the board origin. Or of course you can set the grid origin there which we could do now. But this might be sufficient for us. So I can take for example the USB connector. Press M and we can see it's already aligned centrally with the board because our DY is zero. If we do the same thing for the microcontroller, we can do that and so on.

Of course, it might be easier just to place the grid origin because then you can press E on the component and we can simply change the XY position relative to a centered origin. But at the end of the day, you should have your grid origin, your draw file origin at the bottom left of the board. That is my suggestion. Now that we've got a lot of the basics out of the way, we can fine-tune our layout a bit.
