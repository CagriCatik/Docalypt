# Routing Decoupling/Bypass Caps



all these vis. We're not going to hook them up yet. I typically do my ground and power connections right at the end. Again as it did with the layout process my routing process is also in order of criticality. So I might do the short connections for my decoupling and bypass capacitors.

I might do my crystal oscillators first and then I might do USB and so on. And only at the end I will then hook up all these ground connections and also the overall power routting across the board. And that's a method that's worked fairly well for me. Again, order of criticality I think is important to keep in mind. So with that being said, let's actually start with rooting out.

And the first thing I like to do as we just talked about is do these bypass decoupling capacitor connections. And for this ideally you want the shortest lowest impedance that is widest shortest lowest impedance connection you can between the power pins of these of the capacitor and the relevant device that needs to be decoupled or bypassed.

I can choose my track width at the top left with this drop down and this is where we can find our predefined sizes. So for instance 0.3 mm and then I can hover over a pad and press X to start routting. And you can see why I chose 0.3 millimeters because this is exactly the width of one of these MCU pads.

So I could simply start on this pad, go into this capacitor and call it done. What I prefer doing, however, is necking down rather increasing the width as soon as I can to meet the capacitor pad width itself. And that way I increase my trace width or the or just slightly. But that gives me a slightly low impedance, slightly low inductance connection.

So for instance, I could cycle through my track widths. So for some reason, keycat is being a pain in the neck. For example, if I do a trace width starting at 0.3 mm, route out a tiny bit, then press W to increase the trace width and try and place that. That is I'm necking down or necking in and up to that capacitor pad.

So increasing my width, then key card for some reason will make the entire trace that last width. Whereas if I route up here, then press W to increase my trace width. Everything seems fine. So, you see what I'm trying to do? The way I'm going to get around this for now is change my trace width back to 0.3 mm mters. Root out a tiny bit.

I'm going to copy that segment, rotate it, place it, change that segment to 0.5 or 0.6. And this is now how I'm going to do it for now. And I'm just going to trim that end. And you see what I'm trying to do. Maybe there's someone who knows why this is happening. Keycad only in certain areas. It's incredibly irritating. it.

Anyway, just to illustrate the point, as I come into or out of the pad, I want to maximize the width as far as is reasonable to a wider trace width to meet in essence the capacitor pad width. Later on, we will also be adding teardrops, which helps with this this kind of necking down. But for now, this is what I kind of want to achieve.

Now, for these short distances of this particular board, it doesn't matter terribly much if we do this. For instance, I could just route out a 0.3 mm trace width, go directly into the pads of VREF. If you want to make it slightly nicer, again, we'll add teardrops later on. Or we can do this kind of adjusting track width idea that I just showed you.

Similarly, for the 3 and 3 volt net, I want to do something similar. So, ideally, I want to come out here. Really, I want to increase my trace width. Now, keycode won't let me for some reason. This is the kind of shape I would want to do. So, as soon as I come out of the pad, I want to widen the track. So, I'll see if I can do this. So, after some manual readjustment and dragging, this is what I came up with just again to illustrate the point.

this kind of structure. We also need to keep this widing away a bit from pin 7 because we also want to have this connection, this ground connection which we'll be doing later on with a polygon pore on the top layer. We want to make sure that the polygon pore can connect pin 2 and pin 7.

Yes, we do have v left and right of these pads but ideally we want a solid straight connection here as well. Now whether we've rooted out at least the critical bypass decoupling capacitors, we want to do that across the entire board as well. So ideally short wide connections increasing in trace width as you can.

So I'd strongly suggest now following this along for all the bypassing decoupling capacitors doing that on your end as well. I've added some more of these bypass decoupling capacitor connections for the USB to odd converter. And here I've actually decided to move C7 and C6 not centrally but to the right because we also have the USB D minus D plus lines that look like they need to be flipped and I'd like to avoid using VAS.

So one way we can do that is simply route around underneath the component and into the pads from the back side and the C7 was in the way and just to make it symmetrical I move C6 to the right hand side as well. And I'm doing exactly the same tactic if I need to come out left and right for example pin 7 I'm starting with a narrow track and then widening out widening out coming in to the decoupling capacitor here at the top.

I've simply choose a wide trace and I've just adjusted the trace length to meet the end of the pad here pad 10 like so. So this is a nice short wide connection. I did have to adjust my track size here. I actually had to start out with a 0.25 mm track based on our design rules. Otherwise, Keycad wouldn't let me root this out. So, I added some more predefined sizes such as 0.15 and 0.

25 in the predefined sizes for the IMU at the bottom. These pads are very very close together. If I try and route out, if I press X above the pad, you can see here tells me the routting starting point violates DRC. Now, you could go back to the board setup in the top left hand side.

go to constraints and check the constraints and these constraints actually seem in order. What the actual issue is is if we go to net classes and scroll down the default clearance track with via size and so on those are somewhat different at least the clearance is different to our design rule.

So actually we need to match the clearance to the constraints or we actually need to fill in this information for example for the power nets and so on. But for now I'm going to do it very quickly just change the clearance to.152. Click okay. And this now lets us root out of that pad and we don't get that DRC error anymore. We do have to use a fairly small track width. So if I use 0.25, you can see I can't route out. So that's why I also added it to 0.15.

Again, pin 8 is our main power pin. So that's what we want to root out. And we do the same procedures before. Short segments widen out as soon as we can. And I believe the issue was why Keycad wasn't letting me actually increase the trace width. If I just go straight into the pad, it suddenly snaps and makes all traces the same.

uh width of that segment. If I stop just before, you can see it actually doesn't do that. So, for some reason, only when snapping to a pad, it'll be annoying and uh try and make all the traces the same width. So, not the prettiest, but a structure like this might be okay. It's the general principle of widing out.
