# Routing Crystal & ROSC



Once again, having done these somewhat critical power decoupling caps first, we of course want to do the next critical segments. And for instance, for the microcontroller, we talked about previously that we have this trimming resistor, which is fairly important, and of course, our crystal oscillator. We can do the trimming resistor first. And typically I will stick to one unless I have unless I have specific requirements.

I for PCB design will try to just stick with one trace width for my signals. If it's controlled impedance then of course I'll adjust that. But typically to make something fairly manufacturable that fits most pad sizes unless you need to go very small. At 0.3 mm track is pretty good. So I selected 0.3 mm. I'm going to start on pad 8. Go out. I've changed my grid to 0.25 mm.

keeping clearance away from all of the pads and components and going into the pad like so. You see, I was very deliberate of how I did my pad entries. Keycad tried to suggest different pad entries, but I would strongly suggest entering your pads at 90° angles rather than doing something like this. You don't want these kind of sharp angles because in manufacturing, many people say they aren't an issue, but I've spoken to several manufacturers that acid traps are still an issue. So, overetching of certain areas by having

these rather sharp angles. So that's why I try to avoid that by having nice clean pad entries and exits like so with these 90° angles. We'll add teardrops later which also smooths out these sharp 90° angles. But for this this this could be an okay starting point. We also have to route out pin 11 and pin 12. Now pin 12 we can break out quite easily.

Pin 11 looks like we're going to get into problems with this iros trace. So what I can do I can select one of the segments and hold my mouse button and press shift sometimes also helps. And then drag this trace up a bit. Now I've got the right angle here and I can just fine-tune manually my traces like so.

I still have a somewhat okayish pad entry, but now I've given myself space to route out pin 11. So I've made a short ROS connection. Now I can do HFX in. I come out of the pad. Try to stay away from other components. Click to set certain points. Go around into the capacitor and then straight into the crystal. And I do something similar for pad 12.

HFX out again. Forward slash to change the routing direction into the capacitor first, then into the crystal. Again, I can drag the traces manually afterwards. I can also hold shift to change the grid a tiny bit. Just making sure I'm staying away from any digital signals.

The crystal oscillator is a fairly sensitive circuit, so you don't want to route it and hug it next to, for example, USB or UA or something. So, just an additional starting point, this might be okay for this fairly sensitive area. What you can also do and in certain cases this can help is do a bit of via stitching in terms of guard traces. So I can place a couple of vas around this fairly sensitive section.

This can help as long as the stitching is close enough. So the via spacing is close enough for the aggressor signals. So you could add that in place. The issue is we'll have to be rooting the RTS CTS signals next to the crystal anyway. So here we can't really add these VAS for the most part. So that's why I'm just going to add them vaguely around this area.

And I do do this ahead of time because then I know I can't get close with my RTSC signals close to this signal. So for me, this is also visual indication of okay, stay a bit further away from this crystal because I've already put this kind of guardish fence up. Now, is this needed? Probably not.

But I think it's a nice addition to this and also just a visual addition for yourself to say, okay, stay away from this crystal. You can remove these VAS later on. Not a necessity. But in any case, now we've rooted out the essentially sensitive components around the microcontroller. We still have this VEF connection up here. For this, I'm going to go with a 75 trace width. Just make this nice and wide because essentially this is a ground connection.

So, we want to reduce the inductance. So, for these power connections, decoupling connections, we want to have as wide as is reasonable. But that's pretty much it for the microcontroller. Again, ground connections we'll be doing later on. We now can go to the actual signal connections.
