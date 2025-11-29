# Design Rules Check



If we open that, we want to keep refill all zones before performing DRC checked just in case we haven't report our polygon pors after editing them or after laying new tracks and vas. We want to show both errors and warnings. Then click run DRC and this checks the way we've rooted and laid out our board with the design rule setup we did right at the start of this video.

So click run DRC and don't be shocked there are a lot of errors and warnings. certain errors here. We can see there's a clearance violation between netclass default clearance 0.152 and actuals 1.52. And if we click on these various design rule errors, we can see on the right hand side, Keycad is actually jumping to it and showing us with a little red arrow where these errors are. We can see we have a couple of clearance violations.

We've got a whole clearance violation because of this rather peculiar footprint. more of these clearance violations, incomplete thermal relieves. And the majority of these errors are front solder mask aperture bridges between items with different nets. And for instance, those are the bulk of the areas.

So we can see most of these red arrows are because our solder mask expansion. If we go to the front mask layer, keycat is complaining saying this is an error that our solder mask openings are so wide that they span across pads of different nets. And for components such as this one, fairly fine pitched LQFP packages, you can't really get the solder mask to be just around the pad due to manufacturing constraints. So your solder mask openings for these type of components.

Also, for instance, for the IMU or fine pitch components such as U2, that's pretty much unavoidable. So in that case, I see this not as an error, but rather as a warning or just a completely ignore. And we can change the severity of these errors. The way you can do that is either in the design rules check window, right click on one of these errors and just say ignore all of these errors or edit the violation severity.

So I click on edit violation severity and we can see under the design for manufacturing section right at the bottom solder mask aperture bridges items with different nets. That to me we want to ignore. Click okay and then run DRC again. And you can see we have significantly dropped the number of errors. We do of course have to take care of all of these.

You should when you're done with the board and you've really checked it, you should have zero errors and ideally zero warnings. Quickly just looking at the warnings themselves, the warnings are actually fairly simple. We can see why. It's because I changed some of the properties of these pads manually to not have spokes as thermal relieves and just do solid connections.

And that's why we can see, okay, the footprint does not match the copy in the library. So, this is fairly safe to ignore. So, I'm going to do the same thing. I'm going to ignore all of these and get rid of my warnings. So now we just have to take care of these various errors and clearance violations are of course concerning but you can see actually the difference is 0.152 mm to 0.15 mm.

So we need to see what's going on there. So let's close that. Go to the board setup again and in our design rule constraints we said our minimum clearance is 0.152. But if we go to the neck classes 0.152 and this is because of this weird mills to millimeter conversion. So actually we can drop that to 0.

15 also in the net classes default net class just change that to 0.15 and that's completely fine. That's the simplest way of fixing this because remember at the start of this video we actually define the design rule constraints to be well above the manufacturing minimums. So going down by 0.02 mm is completely fine in this particular scenario because we already have that buffer in place. So click okay.

Let's just press B to rebuild all the zones. Go to the design rule checker. Click run DRC again. And we've already gotten less errors here as well. So we have a couple of these thermal relief incomplete. Let's check those out first. So again, we can click on this and then see what's actually going on. So this seems to be these connections.

We can see here, yeah, this thermal relief connection is not complete. The way we can change that here, because we don't have terribly much of a thermal mass, it's probably okay just to make these solid connections. Alternatively, we can just do polygon port cutout in this area. and then just do manual connections. So we could just do that.

So I can take one of my predefined cutouts we created before, move that over here, and then actually change the dimensions of it. So I can get rid of this polygon pole just around this component. Press B to repaw. And now we just have to do manual connections. I've added that polygon pout, done manual connections.

I've rerun the design rule check, but we still have two of these issues. And that's actually a J1. So, we have to seem to have a similar issue right here of pad B12 and pad A1, it seems. So, let's try and fix that. The way I'm going to do that is actually I'm going to change this to a solid connection because the connection width is pretty small anyway.

So, I'm just going to change that to solid. Also for B12 because that's right underneath. And also do the same thing for A12 and B1. Open the design rule checker. Click run DRC. There we go. We've gotten rid of those thermal relief errors. Now we just have these whole clearance violations.

And we can see the whole clearance violations are because of this slightly awkward footprint for this USB connector. So actually this mounting pin is too close to these pads both for the top here and for the bottom here. So one option would be okay let's just check our manufacturing guidelines from the manufacturer.

Could the manufacturer even manufacture this? Do we just have to relax our design rules or do we actually have to adjust the footprint to make sure that these pads for example B4 A9 and and A12 B1 are further away or shorter that they're further away from this mounting pad. Both are of course viable options. Let's go with editing the footprint.

So I can click on the component J1, press E, go to general, and we're going to edit the footprint but not the library footprint. We want the library footprint to stay the same. We saw this in the schematic editor. We can do the same thing. We just want to edit this one instance of the footprint. And this will also show you the footprint editor.

So what we want to actually do is make these two pads, the power and ground pads shorter and move them up, but still that the edge aligns with the edge of all these other pads. And we'll do the same for A9 A12. So one option of doing that is selecting the pad, pressing E, going to general and the pad properties. We can see the pad length is 1.15. So we could change the pad length, let's say, to one.

So, we're taking off.15 mm, which means we need to move this pad up by half of that by 0075 mm. Click okay. And you can see this is exactly what it's done here. We've taken off.15 mm, moved it away from this mounting pin, but still aligned the top edge with other pads. So, let me do that for the rest of the pads.

And that's now what I've done. So, now we should hopefully have gotten rid of that design rule error. I've saved the component. And again, this is just saved for this particular PCB. And we can see it's updated in the board as well. So I can go back to the design rule check, click run DRC, and we have zero errors and zero warnings.

But keep in mind, this might have seemed like a bit of a cheat, relaxing the design rules, moving the pads. There are, of course, other options. You could use a different connector. You could check your manufacturer capabilities. We could really move the design rules, relax them down to the absolute minimum the manufacturer can produce and hopefully it'll go all right.

I try to sort out these design rule errors fairly logically, fairly systematically based on experience. We pretty much have a finished board now. You could go ahead and just produce the manufacturing files, produce the Gerber files, pick and place and bill of materials. That's the bare minimum. Ship them off to your preferred manufacturer of choice and be done with it. However, there's a couple things I would like to add.
