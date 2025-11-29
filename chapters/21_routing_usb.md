# Routing USB



And I'll show you of course how to do that as well. But for now, we've so far just considered single-ended signals. So for example, URX, RX, and so on. But now we're moving over to rooting a differential pair. Now there's not terribly much to this other than using a different rooting command. So far we've been pressing X to root.

If I press X here, I can route each of these parts individually. But we specifically told Keycad or rather implicitly that with these minus and plus symbols that these same net names form a differential pair. And the way you do that is actually going to root and then root differential pair. Or we can press six on our keyboard.

And if we press six and hover over either one, either over minus or plus, you can see keycad now because we've named this appropriately starts routting out a differential pair. And we can see the track width at the bottom and also the differential pair gap is at the bottom because it's assuming the default differential pair net class. So I press escape to cancel.

Go back to the board setup. We can see that actually for the default net class, we can see there's a differential pair width, DP width, and DP gap defined here. Now, because we've already defined our USB net classes, we could also define that we want a differential pair width and differential pair gap. Now, typically for USB, you want controlled impedance.

However, for short segments, and especially in this case, we're only running USB full speed, which is up to or even slower than SPI, we will not worry about controlled impedance. We're just going to take a somewhat standard track width and track spacing, something that works for these short segments that enables us to route in and out of these rather small pads here. So, we could just route with a default differential pair net class.

But the trace width is a tiny bit small for my liking. So, I'm just going to change that to 0.25 rather than.3. The reason being we need to get in and out of these rather narrow pads given our design rule constraints. So, I've just slightly relaxed the constraints here. I can hover over either one of these differential pair parts. Press six.

And you can see now because we're using the default net class, we're not doing any controlled impedance or different differential pair parameters. I've simply updated the track width to be 0.25 and the differential pair gap to be 0.25. And I can start routting except now I have a diff differential pair rather than a single ended signal. But there's nothing really to be worried about.

You can see here I'm having a bit difficulty getting past the ground via. So I'm going to press escape and I'm just going to move this via up and out of the way. and press six again on the end of these tracks to continue. I'm going to move away this ground via for now as well. We'll rearrange this a tiny bit later on. And I want to route out of this pair.

And you can see I'm rooting underneath the component because we need to do this little flip in D minus D plus. And this is one way we can achieve that. So once you've rooted out the tracks, it could look something like this. We have really short connections. We've used fairly generic differential pair parameters. It really doesn't matter in this case as long as you can do the routting.

And we've kept clear of other signals. We've kept clear of the VA. Given ourselves ample bit of space and we've avoided using any V, any crossings on the left hand side, this D1 diode, these sets of diodes within this D1 component actually they have connections internally between pin one and pin six and pin three and pin four.

That's why we don't actually have to route underneath and through this component. We can simply come out of simply speaking pins one and three and go into the USBC connector. The USBC connector itself again has two sets of differential pairs, two sets of differential pair pins because again we have this 180° shift in in plugging in the cable.

These two options again this is USB full speed. It's really not critical. I'm just going to click on pin one and I'm going to go into the top set of pins B7 and A6. And unfortunately you might end up with something like this. It's not the prettiest.

It's not terribly differential but again we've kept these trace length these distances so short. This is USB 2.0 full speed that this really really does not matter for this particular scenario of this development board. This will work completely fine. We don't have to do any delay matching between the D minus and D plus pairs. We've kept our trace length short. This is a very slow interface. This is a comparatively slow interface.

So you can avoid this differentialness of it. You can if you want of course try and make it prettier on your end. But for now this will absolutely do. What I can then do rather than rooting a single-ended pair because we have to connect D minus and D plus. A simple trick is to route them single-ended. So I'm going to change to 0.25 to match my differential pair width.

But I'm going to route a single-ended signal. So I'm going to hover over B6 and press X. And I'm just going to meet this A6 connection like so. And I'm going to do the same thing for A7. I'm going to come out the back side like so. And this is how I then connect my D minus D plus differential pair pins like so. It's okay.

Not terribly pretty, but it's very convenient, very simple for what we actually need this to do. And this actually even works also for USB highspeed as well, as long as you keep these stubs, these segments comparatively short. We only have two of the USB pins left before we can move over to power, and that's CC1 and CC2. For this, I'm going to go back to 0.

3 mm track width. These are again single-ended signals. And keep in mind, we talked about this previously, but we're going to actually route underneath the USB connector. In this case, this is okay for reasons we talked about earlier. Come out and into this resistor. We're going to adjust the traces in just a second. I'm going to do the same thing on the bottom side.

Like so. I don't really like how close we are to the mounting hole. Again, we have some clearance because this is a fairly wide pad, but I'm just going to drag this a bit. Give myself a tiny bit of space that we're not too close with these traces from the mounting hole. Something like this seems okay. I guess this looks fairly symmetrical.

But here we go. We've rooted out pretty much all of the signals. Now what is left is simply just to do the power connections as well as the ground connections. Then we can clean up the board a tiny bit. We'll add some silk screen. We'll add some text, maybe revision ID and so on. And then we can get this ready for manufacturing.
