# Power & Ground Routing



After having completed essentially all of the signal routting, let's move now over to routting the power. And we'll first do the more straightforward route and we'll add in V jumps as we need to going on the bottom layer with small cuts as is appropriate. And we'll just follow the path of power flow simply speaking. Essentially we have our host connected via the USBC connector which provides the power.

We go through our Pi filter into our LDO regulator and its appropriate capacitors input and output which forms our 3.3 volt net. And that then needs to distribute through essentially the right half of this board. For power routting for these types of boards, having wide traces is pretty much sufficient.

We don't have particularly fast switching frequencies in this design. We don't have particularly high current draws in this design. So fairly beefy trace widths are sufficient. You could of course also do this with a polygon pore, but we will be doing this with trace widths. And I do do this in a lot of designs unless they're very high speed, very high current designs. So somewhere this is completely fine.

We will start off with pin A4 of our USB connector. We of course have pin A9 as well, which we'll take care of just a bit later. We could go out with the 0.5 trace width. Typically for power routing, I like to make the traces as wide as the pads themselves. So the B9 pad happens to be 0.6 mm.

And these 0603 pads have a width of 0.8 and a height of 0.95. So we could go with a 0.8 mm wide pad and always neck down to whatever pad widths we need. So let's add some more predefined track widths. So we come out of B9. I'm using 0.6 mm track width. I'm going to go to the capacitor first of this PI filter.

Then through my series element out of my series element into the second part, second capacitor of this PI filter. From this PI filter, I come out. I'm just going to go with a 0.6 mm trace width. This is sufficient. We could also go with 0.8 to match the width of the pad. But from that, then we go straight into our input capacitor.

So not into pin one of U1 first. We want to go through the input capacitor first. So input capacitor first. C3. And from the input capacitor, we then neck down a tiny bit to go into pad one of our regulator. And pad one actually happens to be 0.6 as well. And remember, pad 3 is actually our enable signal. We'll take care of that in just a second.

So we can go back to 0.3 mm trace width and try and squeeze past into our power net here. Just cleaning up the connection tiny bit. Remember pin 3, it's enable pin. It's high impedance. This trace doesn't need to carry any power or any current. And that's why we give this a smaller trace width.

And we're just about to squeeze it past these two grand pads like so. We could of course move the capacitor left a tiny bit, give ourselves a tiny bit more clearance, but this seems okay for now. Before we do our 3.3 volt net, we'll just quickly do this pad 4.

And this is just a bypass pin to reduce the noise by attaching external capacitor C4 in this case to that pin. And for this again, we can just use a 0.6 mm trace width. This is going to be nice and short like so. That's really all we have to do. We could also make the entry maybe a tiny bit cleaner like so, but that's okay. Then the output of our LDO, that's pin five, then feeds into the output capacitor C5.

From C5, now we have to distribute all across the board our 3.3 volt net. So there's many ways of doing this. We can try and move components around a bit more to make it easier, but the general idea for rooted power for these types of board is you want to come from your power trace for instance like so.

We we have our power trace which is a fairly wide trace. We route our trace. We go through a capacitor first and then through the capacitor into the relevant power pad. We don't want to go from our trace into the pad and then into the capacitor. That's a slightly unoptimized filtering element.

We want to use the inductance and resistance of the trace in combination with the essentially shunt capacitor to form a filter that then feeds our reent power pin. Otherwise, we have worse decoupling. And that's the strategy we're going to use for the rest of these components as well. So we need to try and get to all of these power pins.

So similar to the strategy where we have trace, capacitor, then input power pad, I'd like you to try on your own, I suggest pausing this video trying finishing the routting of the power yourself and see how our solutions compare. So for instance, a possible way of connecting up the 3.3 volt nets would be like so at least for this rooted power very simple board.

We started off coming out of the LDO regulator with a wide trace about 0.6 mm and then rooted in for instance to C7 which was one of the decoupling capacitors for for U2 our USB to UD converter. However, we also of course had to supply the MCU and this MCU 3.3 volt net was a tiny bit hidden. Okay, we could of course come through pin 7.

So for instance an a possible option to routting out 3.3 volt power would be like so we started off coming out of the output capacitor of our LDO regulator using a fairly wide trace about 0.6 mm rooting into our first decoupling capacitor into the power pin and this network then distributes out. We're necking out, necking down as we can.

Again, going into capacitors first and into the relevant power pins. And every time we can, we'd widen out our traces and follow the same pattern of trace, capacitor, pad all the way through. If I do have to do jumps, and I do have to do a couple of jumps, I could have, of course, also rooted around, maybe made it a tiny bit better rather than rooting through all of these pads. There, of course, many options, but this will work sufficiently fine for this case.

But when I do have to do jumps, I try to do as little jumps as I can. So you can see my bottom layer is still predominantly just a ground plane. I do have about four cuts in it, though. And I try to keep those cuts as small as reasonable. The way I do my cuts is, for instance, if I look at this one here, I route with X and I press V on my keyboard to jump to the next layer. And then Keycat already automatically roots on the next layer.

I keep my track width, route over, press V again to get to the top layer. And then I can continue rooting on the top layer. So that's how I would do those jumps. The via nets are then automatically assigned to the net you are routing to. And this way we can connect up all of the 3.3 volt nets. I still have to connect these imu nets here.

And for that I will just use a narrow trace because these are just essentially logic level signals. Something as simple as that will do for these 3.3 volt nets. Remember the large wide pads and traces are only for actually the power and current consuming nets and pads. But this is one way of doing it. This is completely fine.

You could of course pour polygon paw over the top layer and have the polygon pore do this for you. But we will actually be pouring a ground polygon paw the top to actually do all these ground connections. Now you've probably already spotted it, but we still have the VOS connections left. So for example, to the ESD protection, it's the same principle as before wide trace going to the pad.

And here I'm doing this kind of 45° entry, which is also fine for the most part. So what we could do for the Vbus pin A9 to A4 is we could of course route out, jump to the bottom layer, jump to the top layer up here, connect together, but that then creates a cut under a somewhat critical USB differential pair.

An alternative is we route back and just do a cut under the USB CC1 pin. We do also have a fairly narrow area at the back of the A4 pin because of this mounting pin, but we could do that. That of course destroys the symmetry of this a tiny bit. We could rotate R2 for instance, come out of R2 and just route USBC like so. Move my VA around.

And then I that means I can escape B4V bus, drop a V and go to A4V bus for example. Then I don't have to do a cut under the USBC differential pair. That would be an option. Both are fine to be honest. Could look something like this. It's not the prettiest. These are not the prettiest pad escapes either, but again this will work just fine. The key concepts are for this rooted power is fine. Widen your traces when you can.

Shortcuts on the bottom layer and try to keep the bottom layer as a solid ground plane as possible. And this is done by thinking a bit more about the layout before you go over to routting. Again, press B to repour all of your polygon pores. And that would then show all these clearance areas on the polygon paw on the bottom side. With that being said, we're nearing completion.

All we have to do now is also add a polygon paw on the top layer and that's also assigned to ground. The way we can do that is select the polygon pole and double click on it on the bottom layer and simply check top layer as well. Click okay. Press B to repool. And now we can look at the top layer as well.

And we can see we now have a ground polygon pole on the top layer as well. And for us this has made quite a few of the ground connections. But we can see we probably have to move some VAS around because of our clearance constraints. So either we could change our clearance constraints to make our thermal relieves smaller. That's one option.

So I could double click on the polygon paw and change the thermal relief gap to let's say 0.25 mm. Press B to repour and that improves at least the connections that the VA are kind of outside of the thermal relief zone. That improves that a bit more. That would be an option. Or I can simply take my VA and just move them out away from the thermal relief zone manually.

And that's typically what I would do. So changing my grid now going to a 0.1 mm grid. I want my VA just outside that thumb relief zone. So you can adjust your VA as necessary and make sure they are all within the polygon pore is also what I'd suggest doing and then go around and fixing all of that.

Now I've moved my VA outside of the regions of the thermal reliefs, but there are still areas which aren't connected or not optimal. For example, looking at the pin 7 of the MCU, this is actually not connected. the rules we set up for the polygon pause and our design rules are not enough to make this connection. So we could also just do that manually.

So we can just do a track X connect that up and we can also connect that up for instance on other side of the capacitor just to complete these connections that are not reachable by the polygon pore for instance. Keep in mind we can adjust our clearances and trace width and so to make this a type optimized but this is the general principle.

Sometimes also we have these kind of poorly paused polygon regions, let's call them, where we actually don't have too much of a thermal mass imbalance. For instance, pin one doesn't have a lot of copper connected to it, but pin two doesn't either. And normally we would use thermal reliefs to improve the copper balance and improve the solderability at least for through hole parts.

So here we actually might want a a solid connection rather than a thermal relief spow connection. So I can click on the pad, press E, go to connections, and we've seen this before, and change the pad connection to solid. Click okay. Press B to repour. And now I have a solid connection, which for this part here doesn't change the thermal mass differences between pad one and pad 2 considerably. So this is what I'd suggest doing when you don't need those thermal spokes.

You can go in individually and change specific pads to solid connections. And I'll just go through and do that. And I'll also connect up the various unconnected pads that haven't been addressed by the polygon pore. That's exactly what I've completed now. But there's still some optimizations we can do. First of all, you can see here, for example, we have this one singular via.

And this via is just connected to this tiny tiny little island or this little planelet. So this acts basically just a tiny little antenna, a very high frequency antenna. But this isn't great. We don't really want something like this. So what we could do is either join up this little segment under the MCU or let's just get rid of this via press B again. That gets rid of this island as well.

We also have these little necks of polygon paw that kind of just float off. And again, these can create high frequency antennas as well. And for that to get rid of those, I know this is terribly manual, but what I typically do is create a rule area or a copper polygon pore clear out where I just define a little box segment on the top copper layer, for example.

So, I'm going to give this a somewhat sensible name. I'm going to select keep out zone fills, click okay, and start drawing just a little box. Close the box. Press escape. Press B. And you can see now we've cut away this bit of essentially an unnecessary segment of ground film. I can take that rule, copy that and then move that wherever I need to.

So for example here I could just do it the same thing. Press B and this how I can then chop away. I know a terribly man manual procedure how I can chop away these little unused segments for segments where I have a larger area where I could use some vas. This is where I can then do via stitching.

So I can take one of these vas, copy it, paste it, crl +v, and just stitch this whole plane to the bottom polygon pore to make sure this little plane that doesn't resonate at too low frequencies that we fail EMI testing, for instance. We don't want to turn all of these structures into little antennas. And that's what I typically would do all across the board.

Now the the spacing between these VAS depends on the maximum frequency content or the bandwidth of frequency content within your PCB design. And you want to then space the VA based on a certain fraction of the wavelength. For example, a 10th wavelength or 20th wavelength. And this is what's known as stitching VA. And it really depends on the design.

But for us, we are just going to spread these VA around to make sure we don't have any loose ends simply speaking. So one here, one here. And I'm doing it just by eye, just eyeballing it for now. There are far more scientific methods of doing this, but for a board like this, I just simply like to stitch for example the corners.

Make sure I have stitching v all across the board that tie the top and bottom polygon paws together. Not only does this help with EMI, but it also can help because a two-layer board actually has a very comparatively very wide distance between the top and the bottom layer.

So often times if we pour a co-planer ground a polygon porn adjacent to our signal and power traces this actually this adjacent ground paw actually could serve as a better reference. Again stitching helps with lowering the inductance. So that's exactly what I'm doing. I'm just stitching around the board. And for example this is then what a stitched board could look like. It's fairly arbitrary in this case. I've eyealled it based on previous experiences.

This seems to be fairly reasonable for this board. VAS are essentially free for PCB design. And of course, you shouldn't go overboard and completely make this border to Swiss cheese. Of course, this comes with experience. And of course, you can calculate and simulate exactly what the stitching via placement should be.

For other e-cut tools, there are actually stitching tools that you can use that simplifies this process. And I believe there probably are plugins for key cut as well. But with that being said, we are pretty much at the end for the main part of the PCB design process. What we need to do now is clean up. We need to do a design rule check to make sure the way we've rooted this board actually follows our design rules and can be manufactured.

We need to add some text, clean up the silk screen, and so on before we can proceed to generating manufacturing files. before we run a design rule check. And it's incredibly important that you do run design rule checks. And typically, it's also a good idea to run design rule checks as you progress through a board, especially if it's a more complicated board because that lets you pick out errors early and solve those errors early before at the end of the board, you might have 200 hundreds of errors there which you have to figure out.
